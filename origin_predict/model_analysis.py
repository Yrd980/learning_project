import marimo

__generated_with = "0.9.27"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.metrics import classification_report, confusion_matrix
    import warnings
    warnings.filterwarnings('ignore')
    
    # Import our model functions
    from origin.model import (
        preprocess, apply_resampling_and_pca, 
        get_models, evaluate_model, optimize_model,
        save_model_results, list_saved_models, get_best_saved_models, load_model_results
    )
    
    mo.md("""
    # 🔍 Interactive ML Model Analysis
    
    **A comprehensive tool for software defect prediction model comparison**
    
    This interactive notebook allows you to:
    - 🎯 Compare multiple ML models
    - 📊 Analyze individual model performance
    - 💾 Save and load trained models
    - ⚙️ Optimize hyperparameters
    - 📈 Visualize results interactively
    """)
    return (
        apply_resampling_and_pca,
        classification_report,
        confusion_matrix,
        evaluate_model,
        get_best_saved_models,
        get_models,
        list_saved_models,
        load_model_results,
        mo,
        np,
        optimize_model,
        pd,
        plt,
        preprocess,
        save_model_results,
        sns,
        warnings,
    )


@app.cell
def __(mo):
    # Dataset and model selection
    DATASETS = ["KC1", "KC2", "CM1", "JM1", "PC1"]
    MODELS = ["SVM", "KNN", "Decision Tree", "Naive Bayes", "Random Forest", "Stacking"]
    
    dataset_selector = mo.ui.dropdown(
        options=DATASETS,
        value="KC2",
        label="📁 Select Dataset"
    )
    
    model_selector = mo.ui.dropdown(
        options=MODELS,
        value="Random Forest", 
        label="🤖 Select Model"
    )
    
    use_saved_checkbox = mo.ui.checkbox(
        value=True,
        label="🚀 Use Saved Models (faster)"
    )
    
    optimize_checkbox = mo.ui.checkbox(
        value=True,
        label="⚙️ Optimize Hyperparameters"
    )
    
    mo.md(f"""
    ## 🎛️ Configuration Panel
    
    {dataset_selector} {model_selector}
    
    {use_saved_checkbox} {optimize_checkbox}
    """)
    return (
        DATASETS,
        MODELS,
        dataset_selector,
        model_selector,
        optimize_checkbox,
        use_saved_checkbox,
    )


@app.cell
def __(dataset_selector, mo):
    # Data exploration section
    dataset_name = dataset_selector.value
    
    try:
        # Load and show basic dataset info
        file_path = f"data/{dataset_name}.csv"
        raw_data = pd.read_csv(file_path)
        
        # Basic statistics
        total_samples = len(raw_data)
        n_features = len(raw_data.columns) - 1  # Assuming last column is target
        
        # Get target distribution if possible
        target_col = raw_data.columns[-1]
        target_dist = raw_data[target_col].value_counts()
        
        dataset_info = mo.md(f"""
        ## 📊 Dataset: {dataset_name}
        
        - **Total Samples**: {total_samples:,}
        - **Features**: {n_features}
        - **Target Distribution**: 
          - Class 0 (No Defect): {target_dist.get(0, 'N/A')}
          - Class 1 (Defect): {target_dist.get(1, 'N/A')}
        - **Imbalance Ratio**: {target_dist.get(0, 0) / target_dist.get(1, 1):.2f}:1
        """)
        
    except Exception as e:
        dataset_info = mo.md(f"⚠️ Error loading dataset: {e}")
    
    dataset_info
    return dataset_info, dataset_name, file_path, n_features, raw_data, target_col, target_dist, total_samples


@app.cell
def __(mo):
    # Action buttons
    compare_all_button = mo.ui.button(
        label="🚀 Compare All Models",
        kind="success"
    )
    
    analyze_single_button = mo.ui.button(
        label="🎯 Analyze Single Model", 
        kind="warn"
    )
    
    show_saved_button = mo.ui.button(
        label="💾 Show Saved Models",
        kind="neutral"
    )
    
    mo.md(f"""
    ## 🎬 Actions
    
    {compare_all_button} {analyze_single_button} {show_saved_button}
    """)
    return analyze_single_button, compare_all_button, show_saved_button


@app.cell
def __(
    apply_resampling_and_pca,
    compare_all_button,
    dataset_name,
    evaluate_model,
    file_path,
    get_best_saved_models,
    get_models,
    load_model_results,
    mo,
    np,
    plt,
    preprocess,
    save_model_results,
    use_saved_checkbox,
):
    # Compare all models logic
    if compare_all_button.value:
        try:
            mo.output.clear()
            
            # Preprocess data
            X_raw, y_raw = preprocess(file_path)
            X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
            
            results = {}
            used_saved = False
            
            if use_saved_checkbox.value:
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
            
            if results:
                # Create comparison plot
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                
                # Line plot for metrics comparison
                models_list = list(results.keys())
                metrics = ['accuracy', 'precision', 'recall', 'f1']
                x_pos = np.arange(len(metrics))
                
                colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
                
                for i, model in enumerate(models_list):
                    values = [results[model][metric] for metric in metrics]
                    ax1.plot(x_pos, values, marker='o', linewidth=3, label=model, 
                           color=colors[i % len(colors)], markersize=10)
                
                ax1.set_xticks(x_pos)
                ax1.set_xticklabels([m.capitalize() for m in metrics])
                ax1.set_ylabel('Score', fontsize=12)
                ax1.set_title(f'{dataset_name} - Performance Comparison', fontsize=14, fontweight='bold')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                ax1.set_ylim(0, 1)
                
                # Bar plot for F1 scores
                f1_scores = [results[model]['f1'] for model in models_list]
                sorted_indices = np.argsort(f1_scores)[::-1]
                sorted_models = [models_list[i] for i in sorted_indices]
                sorted_f1 = [f1_scores[i] for i in sorted_indices]
                
                bars = ax2.bar(range(len(sorted_models)), sorted_f1, 
                              color=[colors[i % len(colors)] for i in range(len(sorted_models))])
                ax2.set_xticks(range(len(sorted_models)))
                ax2.set_xticklabels(sorted_models, rotation=45, ha='right')
                ax2.set_ylabel('F1 Score', fontsize=12)
                ax2.set_title(f'{dataset_name} - F1 Score Ranking', fontsize=14, fontweight='bold')
                ax2.grid(True, alpha=0.3, axis='y')
                
                # Add value labels on bars
                for bar, score in zip(bars, sorted_f1):
                    ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.01,
                            f'{score:.3f}', ha='center', va='bottom', fontweight='bold')
                
                plt.tight_layout()
                
                # Create results table
                results_df = pd.DataFrame(results).T
                results_df = results_df.round(4)
                results_df = results_df.sort_values('f1', ascending=False)
                
                # Add ranking
                results_df['rank'] = range(1, len(results_df) + 1)
                results_df = results_df[['rank', 'accuracy', 'precision', 'recall', 'f1']]
                
                status = "📂 Loaded from saved models" if used_saved else "🔄 Trained fresh models"
                
                comparison_output = mo.vstack([
                    mo.md(f"## 🏆 Model Comparison Results - {dataset_name}"),
                    mo.md(f"**Status**: {status}"),
                    mo.ui.table(results_df, label="📊 Performance Metrics"),
                    mo.as_html(fig)
                ])
                
            else:
                comparison_output = mo.md("❌ No models could be evaluated")
                
        except Exception as e:
            comparison_output = mo.md(f"❌ Error: {str(e)}")
    else:
        comparison_output = mo.md("Click '🚀 Compare All Models' to start comparison...")
    
    comparison_output
    return (
        X_pca,
        X_raw,
        bars,
        comparison_output,
        f1_scores,
        results,
        results_df,
        sorted_f1,
        sorted_indices,
        sorted_models,
        status,
        used_saved,
        y_processed,
        y_raw,
    )


@app.cell
def __(
    analyze_single_button,
    apply_resampling_and_pca,
    dataset_name,
    evaluate_model,
    file_path,
    get_models,
    mo,
    model_selector,
    np,
    optimize_checkbox,
    optimize_model,
    plt,
    preprocess,
    save_model_results,
):
    # Single model analysis logic
    if analyze_single_button.value:
        try:
            model_name = model_selector.value
            
            # Preprocess data
            X_raw_single, y_raw_single = preprocess(file_path)
            X_pca_single, y_processed_single = apply_resampling_and_pca(X_raw_single, y_raw_single)
            
            # Get and evaluate model
            models = get_models()
            model = models[model_name]
            acc, prec, rec, f1 = evaluate_model(model_name, model, X_pca_single, y_processed_single, epochs=5)
            
            # Hyperparameter optimization
            best_params = {}
            best_score = None
            optimized_model = model
            
            if optimize_checkbox.value:
                try:
                    optimized_model, best_params, best_score = optimize_model(
                        model_name, X_pca_single, y_processed_single, n_trials=20
                    )
                except ValueError:
                    # Model doesn't support hyperparameter tuning
                    pass
            
            # Save model
            try:
                results_dict = {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}
                save_model_results(model_name, optimized_model, results_dict, best_params, best_score, dataset_name)
                model_saved = True
            except Exception as e:
                print(f"Failed to save model: {e}")
                model_saved = False
            
            # Create performance plot
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            fig.suptitle(f'{model_name} Performance on {dataset_name}', fontsize=16, fontweight='bold')
            
            metrics = [acc, prec, rec, f1]
            names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
            
            axes = axes.flatten()
            epochs = range(1, len(acc) + 1)
            
            for i, (metric, name, color) in enumerate(zip(metrics, names, colors)):
                axes[i].plot(epochs, metric, color=color, marker='o', linewidth=2, markersize=8)
                axes[i].fill_between(epochs, metric, alpha=0.3, color=color)
                axes[i].set_title(f'{name}: {np.mean(metric):.4f} ± {np.std(metric):.4f}', fontweight='bold')
                axes[i].set_xlabel('Epoch')
                axes[i].set_ylabel(name)
                axes[i].grid(True, alpha=0.3)
                axes[i].set_ylim(0, 1)
                
                # Add min/max annotations
                axes[i].axhline(y=np.mean(metric), color=color, linestyle='--', alpha=0.7)
                axes[i].text(0.02, 0.98, f'Max: {np.max(metric):.3f}\nMin: {np.min(metric):.3f}', 
                           transform=axes[i].transAxes, verticalalignment='top',
                           bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            
            # Create statistics summary
            stats_summary = {
                'Metric': names,
                'Mean': [np.mean(metric) for metric in metrics],
                'Std': [np.std(metric) for metric in metrics],
                'Min': [np.min(metric) for metric in metrics],
                'Max': [np.max(metric) for metric in metrics]
            }
            stats_df = pd.DataFrame(stats_summary).round(4)
            
            # Build output components
            output_components = [
                mo.md(f"## 🎯 {model_name} Analysis on {dataset_name}"),
            ]
            
            if model_saved:
                output_components.append(mo.md("💾 **Model saved successfully**"))
            
            if best_params and len(best_params) > 0:
                hyperparams_md = "### ⚙️ Optimized Hyperparameters\n"
                for param, value in best_params.items():
                    hyperparams_md += f"- **{param}**: {value}\n"
                if best_score:
                    hyperparams_md += f"- **Best CV F1 Score**: {best_score:.4f}\n"
                output_components.append(mo.md(hyperparams_md))
            
            output_components.extend([
                mo.ui.table(stats_df, label="📊 Performance Statistics"),
                mo.as_html(fig)
            ])
            
            single_analysis_output = mo.vstack(output_components)
            
        except Exception as e:
            single_analysis_output = mo.md(f"❌ Error: {str(e)}")
    else:
        single_analysis_output = mo.md("Click '🎯 Analyze Single Model' to start analysis...")
    
    single_analysis_output
    return (
        X_pca_single,
        X_raw_single,
        acc,
        best_params,
        best_score,
        f1,
        model,
        model_name,
        model_saved,
        optimized_model,
        output_components,
        prec,
        rec,
        results_dict,
        single_analysis_output,
        stats_df,
        stats_summary,
        y_processed_single,
        y_raw_single,
    )


@app.cell
def __(list_saved_models, mo, pd, show_saved_button):
    # Saved models display
    if show_saved_button.value:
        try:
            saved_models = list_saved_models()
            
            if saved_models:
                # Convert to DataFrame for better display
                saved_df = pd.DataFrame(saved_models)
                saved_df = saved_df.round(4)
                saved_df = saved_df.sort_values(['dataset_name', 'mean_f1'], ascending=[True, False])
                
                # Group by dataset for better organization
                datasets_info = []
                for dataset in saved_df['dataset_name'].unique():
                    dataset_models = saved_df[saved_df['dataset_name'] == dataset]
                    datasets_info.append(mo.md(f"### 📊 {dataset} Dataset ({len(dataset_models)} models)"))
                    datasets_info.append(mo.ui.table(
                        dataset_models[['model_name', 'mean_f1', 'best_cv_score', 'timestamp']], 
                        label=f"{dataset} Models"
                    ))
                
                saved_models_output = mo.vstack([
                    mo.md(f"# 💾 Saved Models ({len(saved_models)} total)"),
                    mo.md("Models are automatically saved after training and can be reused for faster comparisons."),
                    *datasets_info
                ])
                
            else:
                saved_models_output = mo.md("""
                # 💾 Saved Models
                
                📭 **No saved models found**
                
                Train some models using the buttons above to see them here!
                """)
                
        except Exception as e:
            saved_models_output = mo.md(f"❌ Error loading saved models: {str(e)}")
    else:
        saved_models_output = mo.md("Click '💾 Show Saved Models' to view saved models...")
    
    saved_models_output
    return dataset_models, datasets_info, saved_df, saved_models, saved_models_output


@app.cell
def __(mo):
    # Footer with information
    mo.md("""
    ---
    
    ## 🔧 Technical Details
    
    ### 📊 **Preprocessing Pipeline**
    - **SMOTE Oversampling**: Handles class imbalance
    - **PCA Dimensionality Reduction**: Reduces feature space
    - **Cross-validation**: 5-fold CV for robust estimates
    
    ### 🤖 **Models Available**
    - **SVM**: Support Vector Machine with RBF kernel
    - **KNN**: K-Nearest Neighbors with distance weighting
    - **Decision Tree**: CART algorithm with pruning
    - **Naive Bayes**: Gaussian Naive Bayes
    - **Random Forest**: Ensemble of decision trees
    - **Stacking**: Meta-ensemble combining multiple models
    
    ### ⚙️ **Hyperparameter Optimization**
    - **Engine**: Optuna (Bayesian optimization)
    - **Objective**: F1-score maximization
    - **Trials**: 20 optimization steps
    - **CV Strategy**: 5-fold cross-validation
    
    ### 💾 **Model Persistence**
    - **Format**: Joblib + JSON metadata
    - **Storage**: Local `saved_models/` directory
    - **Metadata**: Performance metrics, hyperparameters, timestamps
    - **Auto-loading**: Best models loaded automatically
    
    *Built with ❤️ using Marimo, scikit-learn, and Optuna*
    """)
    return


if __name__ == "__main__":
    app.run() 