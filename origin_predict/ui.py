import gradio as gr
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from origin.model import (
    preprocess, apply_resampling_and_pca, 
    get_models, evaluate_model
)
import warnings
warnings.filterwarnings('ignore')

plt.ioff()

# Available datasets
DATASETS = ["KC1", "KC2", "CM1", "JM1", "PC1"]
MODELS = ["SVM", "KNN", "Decision Tree", "Naive Bayes", "Random Forest", "Stacking"]

def plot_to_base64(fig):
    """Convert matplotlib figure to base64 string."""
    try:
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        buf.close()
        plt.close(fig)
        return f"data:image/png;base64,{img_base64}"
    except:
        plt.close(fig)
        return None

def compare_models(dataset_name):
    """Compare all models on selected dataset."""
    try:
        file_path = f"data/{dataset_name}.csv"
        
        # Preprocess data
        X_raw, y_raw = preprocess(file_path)
        X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        
        # Get models and evaluate
        models = get_models()
        results = {}
        
        for name, model in models.items():
            try:
                acc, prec, rec, f1 = evaluate_model(name, model, X_pca, y_processed, epochs=3)
                results[name] = {
                    'accuracy': np.mean(acc),
                    'precision': np.mean(prec),
                    'recall': np.mean(rec),
                    'f1': np.mean(f1)
                }
            except Exception as e:
                print(f"Error with {name}: {e}")
                continue
        
        if not results:
            return "No models could be evaluated", None
        
        # Create comparison plot
        fig, ax = plt.subplots(figsize=(12, 8))
        
        models_list = list(results.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1']
        x_pos = np.arange(len(metrics))
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        
        for i, model in enumerate(models_list):
            values = [results[model][metric] for metric in metrics]
            ax.plot(x_pos, values, marker='o', linewidth=2, label=model, 
                   color=colors[i % len(colors)], markersize=8)
        
        ax.set_xticks(x_pos)
        ax.set_xticklabels([m.capitalize() for m in metrics])
        ax.set_ylabel('Score')
        ax.set_title(f'{dataset_name} Dataset - Model Comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, 1)
        
        plt.tight_layout()
        plot_data = plot_to_base64(fig)
        
        # Create results text
        results_text = f"# {dataset_name} Results\n\n"
        for model, scores in results.items():
            results_text += f"**{model}**: "
            results_text += f"Acc={scores['accuracy']:.3f}, "
            results_text += f"Prec={scores['precision']:.3f}, "
            results_text += f"Rec={scores['recall']:.3f}, "
            results_text += f"F1={scores['f1']:.3f}\n\n"
        
        return results_text, plot_data
        
    except Exception as e:
        return f"Error: {str(e)}", None

def analyze_single_model(dataset_name, model_name):
    """Analyze a single model."""
    try:
        file_path = f"data/{dataset_name}.csv"
        
        # Preprocess data
        X_raw, y_raw = preprocess(file_path)
        X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        
        # Get and evaluate model
        models = get_models()
        model = models[model_name]
        acc, prec, rec, f1 = evaluate_model(model_name, model, X_pca, y_processed, epochs=5)
        
        # Create performance plot
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        fig.suptitle(f'{model_name} on {dataset_name}')
        
        metrics = [acc, prec, rec, f1]
        names = ['Accuracy', 'Precision', 'Recall', 'F1']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        axes = axes.flatten()
        epochs = range(1, len(acc) + 1)
        
        for i, (metric, name, color) in enumerate(zip(metrics, names, colors)):
            axes[i].plot(epochs, metric, color=color, marker='o', linewidth=2)
            axes[i].set_title(f'{name}: {np.mean(metric):.3f} ± {np.std(metric):.3f}')
            axes[i].set_xlabel('Epoch')
            axes[i].set_ylabel(name)
            axes[i].grid(True, alpha=0.3)
            axes[i].set_ylim(0, 1)
        
        plt.tight_layout()
        plot_data = plot_to_base64(fig)
        
        # Create stats text
        stats_text = f"# {model_name} on {dataset_name}\n\n"
        stats_text += f"**Accuracy**: {np.mean(acc):.4f} ± {np.std(acc):.4f}\n\n"
        stats_text += f"**Precision**: {np.mean(prec):.4f} ± {np.std(prec):.4f}\n\n"
        stats_text += f"**Recall**: {np.mean(rec):.4f} ± {np.std(rec):.4f}\n\n"
        stats_text += f"**F1 Score**: {np.mean(f1):.4f} ± {np.std(f1):.4f}\n\n"
        
        return stats_text, plot_data
        
    except Exception as e:
        return f"Error: {str(e)}", None

# Create the simplest possible interface
def create_app():
    # Model comparison interface
    with gr.Blocks() as compare_interface:
        gr.HTML("<h1>🔍 Model Comparison</h1>")
        
        dataset_input = gr.Radio(choices=DATASETS, value="KC2", label="Dataset")
        compare_btn = gr.Button("Compare Models")
        
        results_output = gr.Markdown()
        plot_output = gr.Image()
        
        compare_btn.click(
            compare_models,
            inputs=[dataset_input],
            outputs=[results_output, plot_output]
        )
    
    # Single model interface  
    with gr.Blocks() as single_interface:
        gr.HTML("<h1>🎯 Single Model Analysis</h1>")
        
        dataset_input2 = gr.Radio(choices=DATASETS, value="KC2", label="Dataset")
        model_input = gr.Radio(choices=MODELS, value="Random Forest", label="Model")
        analyze_btn = gr.Button("Analyze Model")
        
        stats_output = gr.Markdown()
        single_plot_output = gr.Image()
        
        analyze_btn.click(
            analyze_single_model,
            inputs=[dataset_input2, model_input],
            outputs=[stats_output, single_plot_output]
        )
    
    # Combined interface with tabs
    with gr.Blocks(title="ML Model Comparison") as demo:
        gr.HTML("<h1>🔍 Software Defect Prediction</h1>")
        
        with gr.Tab("Compare All Models"):
            gr.HTML("<h2>Compare all models on a dataset</h2>")
            
            dataset_sel = gr.Radio(choices=DATASETS, value="KC2", label="Select Dataset")
            compare_button = gr.Button("🚀 Compare Models", variant="primary")
            
            results_text = gr.Markdown()
            comparison_plot = gr.Image()
            
            compare_button.click(
                compare_models,
                inputs=[dataset_sel],
                outputs=[results_text, comparison_plot]
            )
        
        with gr.Tab("Single Model Analysis"):
            gr.HTML("<h2>Detailed analysis of one model</h2>")
            
            dataset_sel2 = gr.Radio(choices=DATASETS, value="KC2", label="Select Dataset") 
            model_sel = gr.Radio(choices=MODELS, value="Random Forest", label="Select Model")
            analyze_button = gr.Button("📊 Analyze Model", variant="primary")
            
            model_stats = gr.Markdown()
            model_plot = gr.Image()
            
            analyze_button.click(
                analyze_single_model,
                inputs=[dataset_sel2, model_sel],
                outputs=[model_stats, model_plot]
            )
        
        with gr.Tab("Info"):
            gr.Markdown("""
            ## About This Tool
            
            This tool compares machine learning models for software defect prediction.
            
            **Datasets**: KC1, KC2, CM1, JM1, PC1
            
            **Models**: SVM, KNN, Decision Tree, Naive Bayes, Random Forest, Stacking
            
            **Features**:
            - Compare all models side-by-side
            - Detailed single model analysis  
            - Automatic data preprocessing (SMOTE + PCA)
            - Performance visualization
            
            **Usage**:
            1. Select a dataset
            2. Click "Compare Models" or choose a specific model to analyze
            3. View results and plots
            """)
    
    return demo

if __name__ == "__main__":
    app = create_app()
    app.launch(share=True, server_port=7860) 