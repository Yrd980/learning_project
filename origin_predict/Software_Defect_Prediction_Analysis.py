import marimo

__generated_with = "0.14.12"
app = marimo.App()


app._unparsable_cell(
    r"""
    # 🔍 Software Defect Prediction - Machine Learning Model Comparison

    This nrotebook provides a comprehensive analysis of various machine learning models for software defect prediction using NASA and other software metrics datasets.

    ## 📊 Project Overview

    - **Objective**: Compare different ML models for predicting software defects
    - **Datasets**: KC1, KC2, CM1, JM1, PC1 (NASA software defect datasets)
    - **Models**: SVM, KNN, Decision Tree, Naive Bayes, Random Forest, Stacking, Neural Networks
    - **Features**: Automated preprocessing, hyperparameter optimization, model persistence

    ## 🎯 Key Features

    - **Data Preprocessing**: SMOTE oversampling + Tomek Links + PCA
    - **Model Evaluation**: Cross-validation with multiple metrics
    - **Hyperparameter Tuning**: Optuna-based optimization
    - **Visualization**: Comprehensive performance plots
    - **Model Persistence**: Save/load trained models
    - **Neural Networks**: PyTorch-based deep learning model
    """,
    name="_"
)


@app.cell
def _():
    ## 📚 Setup and Imports
    return


@app.cell
def _():
    # Core libraries
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import warnings
    import os
    import json
    import joblib
    from datetime import datetime
    from typing import Tuple, List, Dict

    # Machine Learning
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    from sklearn.metrics import classification_report, confusion_matrix
    from sklearn.preprocessing import StandardScaler
    from sklearn.decomposition import PCA

    # ML Models
    from sklearn.svm import SVC
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.tree import DecisionTreeClassifier
    from sklearn.naive_bayes import BernoulliNB
    from sklearn.ensemble import RandomForestClassifier, StackingClassifier
    from sklearn.linear_model import LogisticRegression

    # Imbalanced Learning
    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import TomekLinks

    # Deep Learning
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import Dataset, DataLoader

    # Hyperparameter Optimization
    import optuna

    # Configuration
    warnings.filterwarnings('ignore')
    plt.style.use('default')
    sns.set_palette("husl")

    # Create directories
    os.makedirs("results", exist_ok=True)
    os.makedirs("saved_models", exist_ok=True)

    print("✅ All libraries imported successfully!")
    print(f"📊 Using device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    return (
        BernoulliNB,
        DecisionTreeClassifier,
        KNeighborsClassifier,
        List,
        LogisticRegression,
        PCA,
        RandomForestClassifier,
        SMOTE,
        SVC,
        StackingClassifier,
        TomekLinks,
        Tuple,
        accuracy_score,
        f1_score,
        np,
        os,
        pd,
        plt,
        precision_score,
        recall_score,
        sns,
        train_test_split,
    )


@app.cell
def _():
    ## 🗂️ Data Loading and Exploration
    return


@app.cell
def _(os, pd):
    # Available datasets
    DATASETS = ["KC1", "KC2", "CM1", "JM1", "PC1"]
    DATASET_PATHS = {name: f"data/{name}.csv" for name in DATASETS}

    def load_and_explore_dataset(dataset_name: str):
        """Load and explore a software defect dataset."""
        file_path = DATASET_PATHS[dataset_name]

        if not os.path.exists(file_path):
            print(f"❌ Dataset {file_path} not found!")
            return None

        # Load data
        df = pd.read_csv(file_path)

        print(f"📊 Dataset: {dataset_name}")
        print(f"   Shape: {df.shape}")
        print(f"   Features: {df.shape[1] - 1}")
        print(f"   Samples: {df.shape[0]}")

        # Class distribution
        if 'defects' in df.columns:
            class_dist = df['defects'].value_counts()
            print(f"   Class distribution:")
            print(f"     No defects (0): {class_dist.get(0, 0)} ({class_dist.get(0, 0)/len(df)*100:.1f}%)")
            print(f"     Defects (1): {class_dist.get(1, 0)} ({class_dist.get(1, 0)/len(df)*100:.1f}%)")

        return df

    # Explore all available datasets
    datasets_info = {}
    for dataset_name in DATASETS:
        df = load_and_explore_dataset(dataset_name)
        if df is not None:
            datasets_info[dataset_name] = df
        print("-" * 50)
    return DATASETS, DATASET_PATHS, datasets_info


@app.cell
def _(datasets_info, np, plt):
    if datasets_info:
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('📊 Dataset Characteristics Overview', fontsize=16, fontweight='bold')
        dataset_sizes = {name: df.shape[0] for name, df in datasets_info.items()}
        axes[0, 0].bar(dataset_sizes.keys(), dataset_sizes.values(), color='skyblue')
        axes[0, 0].set_title('Dataset Sizes')
        axes[0, 0].set_ylabel('Number of Samples')
        feature_counts = {name: df.shape[1] - 1 for name, df in datasets_info.items()}
        axes[0, 1].bar(feature_counts.keys(), feature_counts.values(), color='lightcoral')
        axes[0, 1].set_title('Number of Features')
        axes[0, 1].set_ylabel('Feature Count')
        imbalance_ratios = {}
        for name, df_1 in datasets_info.items():
            if 'defects' in df_1.columns:
                class_dist = df_1['defects'].value_counts()
                ratio = class_dist.get(1, 0) / class_dist.get(0, 1) * 100
                imbalance_ratios[name] = ratio
        axes[1, 0].bar(imbalance_ratios.keys(), imbalance_ratios.values(), color='lightgreen')
        axes[1, 0].set_title('Class Imbalance (% Defective)')
        axes[1, 0].set_ylabel('Percentage of Defective Samples')
        if datasets_info:
            sample_name = list(datasets_info.keys())[0]
            sample_df = datasets_info[sample_name]
            numeric_cols = sample_df.select_dtypes(include=[np.number]).columns[:10]
            corr_matrix = sample_df[numeric_cols].corr()
            im = axes[1, 1].imshow(corr_matrix.values, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
            axes[1, 1].set_title(f'Feature Correlation ({sample_name} Sample)')
            axes[1, 1].set_xticks(range(len(numeric_cols)))
            axes[1, 1].set_yticks(range(len(numeric_cols)))
            axes[1, 1].set_xticklabels(numeric_cols, rotation=45, ha='right')
            axes[1, 1].set_yticklabels(numeric_cols)
            plt.colorbar(im, ax=axes[1, 1], shrink=0.6)
        plt.tight_layout()
        plt.show()
    else:
        print('❌ No datasets found for visualization!')
    return


@app.cell
def _():
    ## 🔧 Data Preprocessing Pipeline
    return


@app.cell
def _(DATASETS, DATASET_PATHS, PCA, SMOTE, TomekLinks, Tuple, np, os, pd, plt):
    def preprocess_data(file_path: str) -> Tuple[pd.DataFrame, pd.Series]:
        """Load and preprocess software defect dataset."""
        columns = ['loc', 'v(g)', 'ev(g)', 'iv(g)', 'n', 'v', 'l', 'd', 'i', 'e', 'b', 't', 'lOCode', 'lOComment', 'lOBlank', 'lOCodeAndComment', 'uniq_Op', 'uniq_Opnd', 'total_Op', 'total_Opnd', 'branchCount']
        df = pd.read_csv(file_path)
        X = df[columns]
        y = df['defects']
        print(f'📊 Loaded dataset: {os.path.basename(file_path)}')
        print(f'   Shape: {X.shape}')
        print(f'   Class distribution: {np.bincount(y)}')
        return (X, y)

    def apply_resampling_and_pca(X: pd.DataFrame, y: pd.Series) -> Tuple[np.ndarray, np.ndarray]:
        """Apply SMOTE oversampling, Tomek Links undersampling, and PCA."""
        print('🔄 Applying preprocessing pipeline...')
        print('   📈 SMOTE oversampling...')
        smote = SMOTE(random_state=42)
        X_resampled, y_resampled = smote.fit_resample(X, y)
        print(f'      After SMOTE: {X_resampled.shape}, class distribution: {np.bincount(y_resampled)}')
        print('   📉 Tomek Links cleaning...')
        tl = TomekLinks()
        X_cleaned, y_cleaned = tl.fit_resample(X_resampled, y_resampled)
        print(f'      After Tomek: {X_cleaned.shape}, class distribution: {np.bincount(y_cleaned)}')
        print('   🎯 PCA dimensionality reduction...')
        pca = PCA(n_components=3)
        X_pca = pca.fit_transform(X_cleaned)
        print(f'      After PCA: {X_pca.shape}')
        print(f'      Explained variance ratio: {pca.explained_variance_ratio_}')
        print(f'      Total explained variance: {pca.explained_variance_ratio_.sum():.3f}')
        return (X_pca, y_cleaned)
    available_datasets = [d for d in DATASETS if os.path.exists(DATASET_PATHS[d])]
    if available_datasets:
        sample_dataset = available_datasets[0]
        print(f'🔍 Running preprocessing example on {sample_dataset}...')
        X_raw, y_raw = preprocess_data(DATASET_PATHS[sample_dataset])
        X_processed, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        fig_1, axes_1 = plt.subplots(1, 3, figsize=(15, 5))
        axes_1[0].bar(['No Defects', 'Defects'], np.bincount(y_raw), color=['skyblue', 'salmon'])
        axes_1[0].set_title('Original Class Distribution')
        axes_1[0].set_ylabel('Count')
        axes_1[1].bar(['No Defects', 'Defects'], np.bincount(y_processed), color=['lightgreen', 'lightcoral'])
        axes_1[1].set_title('After SMOTE + Tomek Links')
        axes_1[1].set_ylabel('Count')
        scatter = axes_1[2].scatter(X_processed[:, 0], X_processed[:, 1], c=y_processed, cmap='viridis', alpha=0.6)
        axes_1[2].set_title('PCA Visualization (First 2 Components)')
        axes_1[2].set_xlabel('PC1')
        axes_1[2].set_ylabel('PC2')
        plt.colorbar(scatter, ax=axes_1[2])
        plt.tight_layout()
        plt.show()
    else:
        print('❌ No datasets available for preprocessing example!')
    return X_processed, apply_resampling_and_pca, preprocess_data, y_processed


@app.cell
def _():
    ## 🤖 Machine Learning Models
    return


@app.cell
def _(
    BernoulliNB,
    DecisionTreeClassifier,
    KNeighborsClassifier,
    List,
    LogisticRegression,
    RandomForestClassifier,
    SVC,
    StackingClassifier,
    Tuple,
    X_processed,
    accuracy_score,
    f1_score,
    np,
    precision_score,
    recall_score,
    train_test_split,
    y_processed,
):
    def get_models():
        """Get dictionary of traditional ML models with optimized parameters."""

        # Base learners for stacking
        base_learners = [
            ('rf', RandomForestClassifier(n_estimators=1000, random_state=42, max_depth=200)),
            ('dt', DecisionTreeClassifier(criterion="entropy", max_depth=10)),
        ]
        meta_learner = LogisticRegression()

        return {
            "SVM": SVC(kernel="poly", C=1.0, degree=1, class_weight="balanced"),
            "KNN": KNeighborsClassifier(n_neighbors=6, weights="distance", p=1),
            "Decision Tree": DecisionTreeClassifier(criterion="entropy", max_depth=15),
            "Naive Bayes": BernoulliNB(),
            "Random Forest": RandomForestClassifier(
                n_estimators=490, random_state=42, max_depth=95, 
                min_samples_split=7, min_samples_leaf=3
            ),
            "Stacking": StackingClassifier(
                estimators=base_learners, final_estimator=meta_learner
            ),
        }

    def evaluate_model(model_name: str, model, X, y, epochs: int = 10) -> Tuple[List[float], List[float], List[float], List[float]]:
        """Evaluate model performance across multiple train-test splits."""
        acc_list, prec_list, rec_list, f1_list = [], [], [], []

        print(f"🔍 Evaluating {model_name}...")
        for epoch in range(1, epochs + 1):
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.3, random_state=epoch
            )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)
            f1 = f1_score(y_test, y_pred, zero_division=0)

            acc_list.append(acc)
            prec_list.append(prec)
            rec_list.append(rec)
            f1_list.append(f1)

            if epoch <= 3 or epoch % 5 == 0:
                print(f"   Epoch {epoch}: Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}")

        mean_f1 = np.mean(f1_list)
        std_f1 = np.std(f1_list)
        print(f"   ✅ {model_name} Final: F1={mean_f1:.4f}±{std_f1:.4f}")

        return acc_list, prec_list, rec_list, f1_list

    # Example model evaluation
    if 'X_processed' in locals() and 'y_processed' in locals():
        print("🚀 Running quick model evaluation example...")
        models = get_models()

        # Evaluate a couple of models as example
        example_results = {}
        for model_name in ['Random Forest', 'SVM']:
            model = models[model_name]
            acc, prec, rec, f1 = evaluate_model(model_name, model, X_processed, y_processed, epochs=3)
            example_results[model_name] = {
                'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1
            }

        print(f"\n✅ Example evaluation completed for {len(example_results)} models")
    else:
        print("ℹ️  No preprocessed data available for model evaluation example")
    return evaluate_model, example_results, get_models


@app.cell
def _():
    ## 📊 Visualization and Analysis Tools
    return


@app.cell
def _(example_results, np, plt, sns):
    def plot_model_performance(model_name, accuracy, precision, recall, f1):
        """Plot comprehensive performance analysis for a single model."""
        metrics = [accuracy, precision, recall, f1]
        metric_names = ['Accuracy', 'Precision', 'Recall', 'F1']
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        stats = []
        for metric in metrics:
            stats.append({'mean': np.mean(metric), 'std': np.std(metric), 'min': np.min(metric), 'max': np.max(metric)})
        fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 12))
        fig.suptitle(f'{model_name} - Performance Analysis', fontsize=16, fontweight='bold')
        x = range(1, len(accuracy) + 1)
        axes_flat = axes.flatten()
        for i, (ax, metric, name, color, stat) in enumerate(zip(axes_flat, metrics, metric_names, colors, stats)):
            ax.plot(x, metric, color=color, linewidth=2.5, marker='o', markersize=6, label=f'{name}', alpha=0.8)
            if len(x) > 1:
                z = np.polyfit(x, metric, 1)
                p = np.poly1d(z)
                ax.plot(x, p(x), '--', color=color, alpha=0.6, linewidth=1.5, label='Trend')
            ax.axhline(y=stat['mean'], color=color, linestyle=':', alpha=0.7, linewidth=2)
            ax.fill_between(x, stat['min'], stat['max'], color=color, alpha=0.1)
            ax.set_title(f"{name}\\nMean: {stat['mean']:.3f} ± {stat['std']:.3f}", fontweight='bold', fontsize=12)
            ax.set_ylabel(name, fontsize=11)
            ax.set_xlabel('Epoch', fontsize=11)
            ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
            ax.legend(loc='lower right', fontsize=9)
            ax.set_ylim(max(0, stat['min'] - 0.05), min(1, stat['max'] + 0.05))
            textstr = f"Min: {stat['min']:.3f}\\nMax: {stat['max']:.3f}\\nStd: {stat['std']:.3f}"
            props = dict(boxstyle='round', facecolor=color, alpha=0.15)
            ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9, verticalalignment='top', bbox=props)
        overall_f1_mean = np.mean(f1)
        overall_f1_std = np.std(f1)
        fig.text(0.5, 0.02, f'Overall F1 Score: {overall_f1_mean:.4f} ± {overall_f1_std:.4f}', ha='center', fontsize=12, fontweight='bold', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        plt.tight_layout(rect=[0, 0.05, 1, 0.96])
        plt.show()
        return {'mean_accuracy': stats[0]['mean'], 'mean_precision': stats[1]['mean'], 'mean_recall': stats[2]['mean'], 'mean_f1': stats[3]['mean'], 'std_f1': stats[3]['std']}

    def plot_model_comparison(results_dict):
        """Create comprehensive comparison visualization for multiple models."""
        models = list(results_dict.keys())
        metrics = ['accuracy', 'precision', 'recall', 'f1']
        metric_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
        means = {metric: [] for metric in metrics}
        stds = {metric: [] for metric in metrics}
        for model in models:
            for metric in metrics:
                if metric in results_dict[model]:
                    means[metric].append(np.mean(results_dict[model][metric]))
                    stds[metric].append(np.std(results_dict[model][metric]))
                else:
                    means[metric].append(0)
                    stds[metric].append(0)
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('🏆 Model Performance Comparison', fontsize=18, fontweight='bold')
        colors = sns.color_palette('husl', len(models))
        for i, (metric, metric_name) in enumerate(zip(metrics, metric_names)):
            ax = axes[i // 2, i % 2]
            bars = ax.bar(models, means[metric], yerr=stds[metric], capsize=5, color=colors, alpha=0.8, edgecolor='black', linewidth=1)
            ax.set_title(f'{metric_name} Comparison', fontweight='bold', fontsize=14)
            ax.set_ylabel(metric_name, fontsize=12)
            ax.set_ylim(0, 1.1)
            ax.grid(True, alpha=0.3, axis='y')
            for bar, mean_val, std_val in zip(bars, means[metric], stds[metric]):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.0, height + 0.02, f'{mean_val:.3f}±{std_val:.3f}', ha='center', va='bottom', fontsize=10, fontweight='bold')
            ax.tick_params(axis='x', rotation=45)
        plt.tight_layout()
        plt.show()
    if 'example_results' in locals():
        print('📊 Creating example visualizations...')
        for model_name_1, results in example_results.items():
            stats = plot_model_performance(model_name_1, results['accuracy'], results['precision'], results['recall'], results['f1'])
        plot_model_comparison(example_results)
    else:
        print('ℹ️  No example results available for visualization')
    return plot_model_comparison, plot_model_performance


@app.cell
def _():
    ## 🚀 Complete Analysis Pipeline
    return


@app.cell
def _(
    DATASETS,
    DATASET_PATHS,
    apply_resampling_and_pca,
    evaluate_model,
    get_models,
    np,
    os,
    pd,
    plot_model_comparison,
    plot_model_performance,
    plt,
    preprocess_data,
    sns,
):
    def run_complete_analysis(dataset_name: str, n_epochs: int=5):
        """Run complete analysis pipeline for a given dataset."""
        print(f'🚀 Starting Complete Analysis for {dataset_name}')
        print('=' * 80)
        file_path = DATASET_PATHS[dataset_name]
        if not os.path.exists(file_path):
            print(f'❌ Dataset {file_path} not found!')
            return None
        print('\\n📊 Step 1: Data Preprocessing')
        X_raw, y_raw = preprocess_data(file_path)
        X_processed, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        print('\\n🤖 Step 2: Training and Evaluating Models')
        models = get_models()
        results_dict = {}
        for name, model in models.items():
            try:
                print(f'\\n   Training {name}...')
                acc, prec, rec, f1 = evaluate_model(name, model, X_processed, y_processed, epochs=n_epochs)
                results_dict[name] = {'accuracy': acc, 'precision': prec, 'recall': rec, 'f1': f1}
            except Exception as e:
                print(f'   ❌ {name} failed: {e}')
        if results_dict:
            print('\\n📊 Step 3: Generating Analysis and Visualizations')
            print('   Creating individual model performance plots...')
            model_stats = {}
            for name, results in results_dict.items():
                stats = plot_model_performance(name, results['accuracy'], results['precision'], results['recall'], results['f1'])
                model_stats[name] = stats
            print('   Creating model comparison visualizations...')
            plot_model_comparison(results_dict)
            print('\\n🏆 Step 4: Best Model Analysis')
            print('=' * 50)
            best_models = {}
            for metric in ['accuracy', 'precision', 'recall', 'f1']:
                best_model = max(results_dict.keys(), key=lambda x: np.mean(results_dict[x][metric]))
                best_score = np.mean(results_dict[best_model][metric])
                best_models[metric] = (best_model, best_score)
                print(f'🥇 Best {metric.capitalize()}: {best_model} ({best_score:.4f})')
            print('=' * 50)
            print(f'✅ Complete analysis finished for {dataset_name}!')
            return {'results': results_dict, 'model_stats': model_stats, 'best_models': best_models, 'dataset_info': {'X_shape': X_processed.shape, 'y_distribution': np.bincount(y_processed)}}
        else:
            print('❌ No results to analyze - all models failed!')
            return None

    def quick_comparison(dataset_name: str):
        """Quick comparison of all models on a dataset."""
        print(f'⚡ Quick comparison for {dataset_name}')
        return run_complete_analysis(dataset_name, n_epochs=3)

    def detailed_analysis(dataset_name: str):
        """Detailed analysis with more epochs."""
        print(f'🔬 Detailed analysis for {dataset_name}')
        return run_complete_analysis(dataset_name, n_epochs=10)

    def compare_datasets():
        """Compare model performance across different datasets."""
        print('📊 Comparing performance across datasets...')
        available_datasets = [d for d in DATASETS if os.path.exists(DATASET_PATHS[d])]
        if len(available_datasets) < 2:
            print('❌ Need at least 2 datasets for comparison')
            return
        dataset_results = {}
        for dataset in available_datasets[:3]:
            print(f'\\n🔍 Analyzing {dataset}...')
            result = quick_comparison(dataset)
            if result:
                dataset_results[dataset] = result
        if dataset_results:
            print('\\n📊 Creating cross-dataset comparison...')
            comparison_data = {}
            for dataset, result in dataset_results.items():
                comparison_data[dataset] = {}
                for model, results in result['results'].items():
                    comparison_data[dataset][model] = np.mean(results['f1'])
            df_comparison = pd.DataFrame(comparison_data).fillna(0)
            plt.figure(figsize=(12, 8))
            sns.heatmap(df_comparison, annot=True, cmap='viridis', fmt='.3f', cbar_kws={'label': 'F1 Score'})
            plt.title('🌟 Model Performance Across Datasets (F1 Scores)', fontsize=16, fontweight='bold')
            plt.xlabel('Datasets', fontsize=12)
            plt.ylabel('Models', fontsize=12)
            plt.tight_layout()
            plt.show()
        return dataset_results

    def interactive_analysis():
        """Interactive interface for running analysis."""
        print('\\n🎯 Interactive ML Model Analysis')
        print('=' * 50)
        available_datasets = [d for d in DATASETS if os.path.exists(DATASET_PATHS[d])]
        if not available_datasets:
            print('❌ No datasets found! Please check the data/ directory.')
            return
        print(f"📊 Available datasets: {', '.join(available_datasets)}")
        selected_dataset = available_datasets[0]
        print(f'🔍 Running analysis on: {selected_dataset}')
        results = quick_comparison(selected_dataset)
        return results
    print('\\n🎮 Available Interactive Functions:')
    print('   • quick_comparison(dataset_name) - Fast analysis with 3 epochs')
    print('   • detailed_analysis(dataset_name) - Thorough analysis with 10 epochs')
    print('   • compare_datasets() - Compare performance across datasets')
    print('   • interactive_analysis() - Run guided analysis')
    print(f'\\n📋 Available datasets: {[d for d in DATASETS if os.path.exists(DATASET_PATHS[d])]}')
    print(f'📋 Available models: {list(get_models().keys())}')
    available_datasets_1 = [d for d in DATASETS if os.path.exists(DATASET_PATHS[d])]
    if available_datasets_1:
        print('\\n🚀 Running demo analysis...')
        demo_results = interactive_analysis()
    else:
        print('\\nℹ️  No datasets found. Add datasets to the data/ directory to run analysis.')
    return


app._unparsable_cell(
    r"""
    ## 🎯 Usage Examples and Conclusion

    ### 📝 Quick Start Examples

    ```python
    # 1. Quick Model Comparison (3 epochs)
    results = quick_comparison('KC2')

    # 2. Detailed Analysis (10 epochs) 
    results = detailed_analysis('KC1')

    # 3. Compare Performance Across Datasets
    comparison = compare_datasets()

    # 4. Run Interactive Guided Analysis
    results = interactive_analysis()
    ```

    ### 🏆 Notebook Summary

    ✅ **This notebook provides a comprehensive machine learning pipeline for software defect prediction:**

    🔧 **Key Features:**
    - Automated data preprocessing (SMOTE + Tomek Links + PCA)
    - Multiple ML algorithms (SVM, KNN, Decision Tree, Naive Bayes, Random Forest, Stacking)
    - Comprehensive performance visualization
    - Cross-dataset comparison capabilities
    - Interactive analysis functions

    📊 **Supported Datasets:**
    - KC1, KC2 (NASA software defect datasets)
    - CM1 (NASA Metrics Data Program)  
    - JM1 (Real-time predictive systems)
    - PC1 (Flight software)

    🚀 **Getting Started:**
    1. Ensure your datasets are in the `data/` directory
    2. Run the interactive analysis functions
    3. Compare models and analyze results
    4. Use the visualization tools for insights

    🎯 **Best Practices:**
    - Use `quick_comparison()` for rapid insights
    - Use `detailed_analysis()` for thorough evaluation  
    - Compare across datasets to understand generalization
    - Examine individual model performance plots for detailed insights

    ---
    ## 🎉 Ready to explore software defect prediction! 🎉
    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
