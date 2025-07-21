import gradio as gr
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from origin.model import (
    preprocess, apply_resampling_and_pca, 
    get_models, evaluate_model, optimize_model,
    save_model_results, list_saved_models, get_best_saved_models, load_model_results
)
import warnings
warnings.filterwarnings('ignore')

plt.ioff()

# Available datasets and models
DATASETS = ["KC1", "KC2", "CM1", "JM1", "PC1"]
MODELS = ["SVM", "KNN", "Decision Tree", "Naive Bayes", "Random Forest", "Stacking"]

def plot_to_base64(fig):
    """Convert matplotlib figure to base64 string for Gradio."""
    try:
        # Save to temporary file instead of base64 for Gradio
        import tempfile
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        fig.savefig(temp_file.name, format='png', dpi=150, bbox_inches='tight', 
                   facecolor='white', edgecolor='none')
        temp_file.close()
        plt.close(fig)
        
        return temp_file.name
        
    except Exception as e:
        print(f"Plot conversion error: {e}")
        plt.close(fig)
        # Return a simple error plot
        try:
            error_fig, error_ax = plt.subplots(figsize=(8, 6))
            error_ax.text(0.5, 0.5, f'Plot Error:\n{str(e)}', 
                         horizontalalignment='center', verticalalignment='center',
                         transform=error_ax.transAxes, fontsize=12, color='red')
            error_ax.set_title('Plot Generation Failed')
            error_ax.axis('off')
            
            temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
            error_fig.savefig(temp_file.name, format='png', dpi=150, bbox_inches='tight')
            temp_file.close()
            plt.close(error_fig)
            
            return temp_file.name
        except:
            return None

def compare_models(dataset_name, use_saved_models=True):
    """Compare all models on selected dataset with option to use saved models."""
    try:
        file_path = f"data/{dataset_name}.csv"
        
        # Preprocess data
        X_raw, y_raw = preprocess(file_path)
        X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        
        results = {}
        best_scores = {}
        used_saved = False
        
        if use_saved_models:
            # Try to load saved models
            best_saved = get_best_saved_models(dataset_name)
            if best_saved:
                for model_name, info in best_saved.items():
                    try:
                        model_dir = f"saved_models/{info['directory']}"
                        model, metadata = load_model_results(model_dir, model_name)
                        results[model_name] = {
                            'accuracy': np.mean(metadata['raw_results']['accuracy']),
                            'precision': np.mean(metadata['raw_results']['precision']),
                            'recall': np.mean(metadata['raw_results']['recall']),
                            'f1': np.mean(metadata['raw_results']['f1'])
                        }
                        best_scores[model_name] = metadata['best_cv_score']
                        used_saved = True
                    except Exception as e:
                        print(f"Failed to load {model_name}: {e}")
                        continue
        
        if not results:
            # Train fresh models
            models = get_models()
            for name, model in models.items():
                try:
                    acc, prec, rec, f1 = evaluate_model(name, model, X_pca, y_processed, epochs=3)
                    results[name] = {
                        'accuracy': np.mean(acc),
                        'precision': np.mean(prec),
                        'recall': np.mean(rec),
                        'f1': np.mean(f1)
                    }
                    
                    # Save the model
                    try:
                        results_dict = {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}
                        save_model_results(name, model, results_dict, {}, None, dataset_name)
                    except Exception as e:
                        print(f"Failed to save {name}: {e}")
                        
                except Exception as e:
                    print(f"Error with {name}: {e}")
                    continue
        
        if not results:
            return "❌ No models could be evaluated", None
        
        # Create comparison plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        models_list = list(results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1']
        x_pos = np.arange(len(metrics))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
        for i, model in enumerate(models_list):
            values = [results[model][metric] for metric in metrics]
            ax.plot(x_pos, values, marker='o', linewidth=3, label=model, 
                   color=colors[i % len(colors)], markersize=10)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([m.capitalize() for m in metrics])
        ax.set_ylabel('Score', fontsize=12)
        ax.set_title(f'{dataset_name} Dataset - Model Comparison', fontsize=16, fontweight='bold')
        ax.legend(fontsize=10)
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        plt.tight_layout()
        plot_data = plot_to_base64(fig)
        
        # Handle plot failure
        if plot_data is None:
            plot_data = "Error generating plot"
        
        # Create results text
        status_text = "📂 **Loaded from saved models**" if used_saved else "🔄 **Trained fresh models and saved them**"
        results_text = f"# 🎯 {dataset_name} Model Comparison Results\n\n{status_text}\n\n"
        
        # Sort by F1 score for better presentation
        sorted_results = sorted(results.items(), key=lambda x: x[1]['f1'], reverse=True)
        
        for i, (model, scores) in enumerate(sorted_results):
            rank_emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📊"
            results_text += f"### {rank_emoji} **{model}**\n"
            results_text += f"- **Accuracy**: {scores['accuracy']:.4f}\n"
            results_text += f"- **Precision**: {scores['precision']:.4f}\n"
            results_text += f"- **Recall**: {scores['recall']:.4f}\n"
            results_text += f"- **F1 Score**: {scores['f1']:.4f}\n\n"
        
        return results_text, plot_data
        
    except Exception as e:
        return f"❌ **Error**: {str(e)}", None

def analyze_single_model(dataset_name, model_name, save_model=True, optimize_hyperparams=True):
    """Analyze a single model with options for saving and hyperparameter optimization."""
    try:
        file_path = f"data/{dataset_name}.csv"
        
        # Preprocess data
        X_raw, y_raw = preprocess(file_path)
        X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        
        # Get and evaluate model
        models = get_models()
        model = models[model_name]
        acc, prec, rec, f1 = evaluate_model(model_name, model, X_pca, y_processed, epochs=5)
        
        # Hyperparameter optimization
        best_params = {}
        best_score = None
        optimized_model = model
        
        if optimize_hyperparams:
            try:
                optimized_model, best_params, best_score = optimize_model(model_name, X_pca, y_processed, n_trials=20)
            except ValueError:
                # Model doesn't support hyperparameter tuning
                pass
        
        # Save model if requested
        model_saved = False
        if save_model:
            try:
                results_dict = {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}
                save_model_results(model_name, optimized_model, results_dict, best_params, best_score, dataset_name)
                model_saved = True
            except Exception as e:
                print(f"Failed to save model: {e}")
        
        # Create performance plot
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'{model_name} Performance on {dataset_name} Dataset', fontsize=16, fontweight='bold')
        
        metrics = [acc, prec, rec, f1]
        names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        axes = axes.flatten()
        epochs = range(1, len(acc) + 1)
        
        for i, (metric, name, color) in enumerate(zip(metrics, names, colors)):
            axes[i].plot(epochs, metric, color=color, marker='o', linewidth=2, markersize=6)
            axes[i].set_title(f'{name}: {np.mean(metric):.4f} ± {np.std(metric):.4f}', fontweight='bold')
            axes[i].set_xlabel('Epoch')
            axes[i].set_ylabel(name)
            axes[i].grid(True, alpha=0.3)
            axes[i].set_ylim(0, 1)
        
        plt.tight_layout()
        plot_data = plot_to_base64(fig)
        
        # Handle plot failure
        if plot_data is None:
            plot_data = "Error generating plot"
        
        # Create stats text
        stats_text = f"# 📈 {model_name} Analysis on {dataset_name}\n\n"
        
        if model_saved:
            stats_text += "💾 **Model saved successfully**\n\n"
        
        if best_params and len(best_params) > 0:
            stats_text += "## 🎯 Optimized Hyperparameters\n"
            for param, value in best_params.items():
                stats_text += f"- **{param}**: {value}\n"
            if best_score:
                stats_text += f"- **Best CV F1 Score**: {best_score:.4f}\n"
            stats_text += "\n"
        
        stats_text += "## 📊 Performance Statistics\n\n"
        stats_text += f"### 🎯 **Accuracy**\n"
        stats_text += f"- **Mean**: {np.mean(acc):.4f} ± {np.std(acc):.4f}\n"
        stats_text += f"- **Range**: {np.min(acc):.4f} - {np.max(acc):.4f}\n\n"
        
        stats_text += f"### 🎯 **Precision**\n"
        stats_text += f"- **Mean**: {np.mean(prec):.4f} ± {np.std(prec):.4f}\n"
        stats_text += f"- **Range**: {np.min(prec):.4f} - {np.max(prec):.4f}\n\n"
        
        stats_text += f"### 🎯 **Recall**\n"
        stats_text += f"- **Mean**: {np.mean(rec):.4f} ± {np.std(rec):.4f}\n"
        stats_text += f"- **Range**: {np.min(rec):.4f} - {np.max(rec):.4f}\n\n"
        
        stats_text += f"### 🎯 **F1 Score**\n"
        stats_text += f"- **Mean**: {np.mean(f1):.4f} ± {np.std(f1):.4f}\n"
        stats_text += f"- **Range**: {np.min(f1):.4f} - {np.max(f1):.4f}\n\n"
        
        return stats_text, plot_data
        
    except Exception as e:
        return f"❌ **Error**: {str(e)}", None

def get_saved_models_info():
    """Get information about saved models."""
    try:
        saved_models = list_saved_models()
        if not saved_models:
            return "📭 **No saved models found**\n\nTrain some models first to see them here!"
        
        info_text = f"# 💾 Saved Models ({len(saved_models)} total)\n\n"
        
        # Group by dataset
        by_dataset = {}
        for model in saved_models:
            dataset = model['dataset_name']
            if dataset not in by_dataset:
                by_dataset[dataset] = []
            by_dataset[dataset].append(model)
        
        for dataset, models in by_dataset.items():
            info_text += f"## 📊 {dataset} Dataset\n\n"
            
            # Sort by F1 score
            models.sort(key=lambda x: x['mean_f1'], reverse=True)
            
            for i, model in enumerate(models):
                rank_emoji = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "📊"
                info_text += f"### {rank_emoji} {model['model_name']}\n"
                info_text += f"- **F1 Score**: {model['mean_f1']:.4f}\n"
                if model.get('best_cv_score'):
                    info_text += f"- **CV Score**: {model['best_cv_score']:.4f}\n"
                info_text += f"- **Saved**: {model['timestamp']}\n\n"
        
        return info_text
        
    except Exception as e:
        return f"❌ **Error loading saved models**: {str(e)}"

def clear_saved_models():
    """Clear all saved models."""
    try:
        import shutil
        import os
        
        if os.path.exists('saved_models'):
            shutil.rmtree('saved_models')
            os.makedirs('saved_models', exist_ok=True)
        
        return "✅ **All saved models have been cleared**"
    except Exception as e:
        return f"❌ **Error**: {str(e)}"

def create_app():
    """Create the Gradio application with improved UI and model management."""
    
    with gr.Blocks(
        title="🔍 ML Model Comparison Tool",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 1200px !important;
        }
        .tab-nav button {
            font-size: 16px !important;
        }
        """
    ) as demo:
        
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🔍 Software Defect Prediction Model Comparison</h1>
            <p style="font-size: 18px; color: #666;">
                Compare ML models with automatic preprocessing, hyperparameter optimization, and model saving
            </p>
        </div>
        """)
        
        with gr.Tab("📊 Compare All Models"):
            gr.HTML("<h2>🚀 Compare all models on a dataset</h2>")
            
            with gr.Row():
                with gr.Column(scale=1):
                    dataset_sel = gr.Radio(
                        choices=DATASETS, 
                        value="KC2", 
                        label="📁 Select Dataset",
                        info="Choose a software defect dataset"
                    )
                    use_saved = gr.Checkbox(
                        value=True, 
                        label="🚀 Use Saved Models",
                        info="Load pre-trained models (faster) or train from scratch"
                    )
                    compare_button = gr.Button(
                        "🔥 Compare All Models", 
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=2):
                    results_text = gr.Markdown(
                        value="Click 'Compare All Models' to start...",
                        label="📈 Results"
                    )
            
            comparison_plot = gr.Image(label="📊 Comparison Plot")
            
            compare_button.click(
                compare_models,
                inputs=[dataset_sel, use_saved],
                outputs=[results_text, comparison_plot]
            )
        
        with gr.Tab("🎯 Single Model Analysis"):
            gr.HTML("<h2>🔬 Detailed analysis of one model</h2>")
            
            with gr.Row():
                with gr.Column(scale=1):
                    dataset_sel2 = gr.Radio(
                        choices=DATASETS, 
                        value="KC2", 
                        label="📁 Select Dataset"
                    )
                    model_sel = gr.Radio(
                        choices=MODELS, 
                        value="Random Forest", 
                        label="🤖 Select Model"
                    )
                    
                    with gr.Row():
                        save_model_check = gr.Checkbox(
                            value=True, 
                            label="💾 Save Model"
                        )
                        optimize_check = gr.Checkbox(
                            value=True, 
                            label="⚙️ Optimize Hyperparameters"
                        )
                    
                    analyze_button = gr.Button(
                        "📈 Analyze Model", 
                        variant="primary",
                        size="lg"
                    )
                
                with gr.Column(scale=2):
                    model_stats = gr.Markdown(
                        value="Select dataset and model, then click 'Analyze Model'...",
                        label="📊 Statistics"
                    )
            
            model_plot = gr.Image(label="📈 Performance Plot")
            
            analyze_button.click(
                analyze_single_model,
                inputs=[dataset_sel2, model_sel, save_model_check, optimize_check],
                outputs=[model_stats, model_plot]
            )
        
        with gr.Tab("💾 Saved Models"):
            gr.HTML("<h2>🗄️ Manage saved models</h2>")
            
            with gr.Row():
                refresh_btn = gr.Button("🔄 Refresh", variant="secondary")
                clear_btn = gr.Button("🗑️ Clear All Models", variant="stop")
            
            saved_models_info = gr.Markdown(
                value="Click 'Refresh' to load saved models...",
                label="📋 Saved Models"
            )
            
            refresh_btn.click(
                get_saved_models_info,
                outputs=[saved_models_info]
            )
            
            clear_btn.click(
                clear_saved_models,
                outputs=[saved_models_info]
            )
            
            # Auto-refresh on tab load
            demo.load(get_saved_models_info, outputs=[saved_models_info])
        
        with gr.Tab("ℹ️ Information"):
            gr.Markdown("""
            # 🎯 About This Tool
            
            This application provides comprehensive comparison of machine learning models for software defect prediction with advanced model management capabilities.
            
            ## 🚀 Key Features
            
            ### 🎯 **Model Comparison**
            - Compare all 6 models side-by-side
            - Automatic performance ranking
            - Visual comparison charts
            
            ### 🔬 **Single Model Analysis**
            - Detailed performance analysis for individual models
            - Cross-validation statistics with error bars
            - Performance visualization across multiple epochs
            
            ### 💾 **Model Management**
            - **Automatic Saving**: Models are saved with metadata after training
            - **Quick Loading**: Reuse saved models to skip training time
            - **Performance Tracking**: Track model performance over time
            - **Best Model Selection**: Automatically load the best performing model for each type
            
            ### ⚙️ **Advanced Features**
            - **Hyperparameter Optimization**: Uses Optuna for automatic parameter tuning
            - **Automatic Preprocessing**: SMOTE oversampling + PCA dimensionality reduction
            - **Error Handling**: Robust error handling and user feedback
            - **Performance Visualization**: Interactive charts and detailed statistics
            
            ## 📊 Models Included
            
            - **Support Vector Machine (SVM)**
            - **K-Nearest Neighbors (KNN)**
            - **Decision Tree**
            - **Naive Bayes**
            - **Random Forest**
            - **Stacking Ensemble**
            
            ## 📁 Datasets Available
            
            - **KC1, KC2**: NASA software defect datasets
            - **CM1**: NASA Metrics Data Program
            - **JM1**: Real-time predictive systems
            - **PC1**: Flight software for Earth orbiting satellite
            
            ## 🚀 How to Use
            
            1. **Compare All Models**: Use saved models for instant results, or uncheck to train fresh
            2. **Single Model Analysis**: Train specific models with hyperparameter optimization
            3. **Saved Models**: View and manage your model collection
            4. Models are automatically saved after training for future use
            
            ## 🔧 Technical Details
            
            - **Preprocessing**: Automatic handling of imbalanced data using SMOTE
            - **Dimensionality Reduction**: PCA to reduce feature space
            - **Cross-Validation**: 5-fold CV for robust performance estimates
            - **Optimization**: Bayesian optimization using Optuna
            - **Storage**: Models saved using joblib with JSON metadata
            """)
    
    return demo

if __name__ == "__main__":
    print("🚀 Starting Enhanced ML Model Comparison Gradio App...")
    print("💾 Features: Model saving, hyperparameter optimization, advanced UI")
    print("📊 Navigate between tabs to explore different functionalities")
    
    app = create_app()
    app.launch(
        share=True, 
        server_port=7860,
        server_name="0.0.0.0",
        show_api=False,
        quiet=False
    ) 