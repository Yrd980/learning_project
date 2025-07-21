from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# Ensure the results directory exists
os.makedirs("results", exist_ok=True)


def plot_model(model_name, accuracy, precision, recall, f1):
    """Plot metrics (Accuracy, Precision, Recall, F1) for a single model with improved visualization."""
    metrics = [accuracy, precision, recall, f1]
    metric_names = ["Accuracy", "Precision", "Recall", "F1"]
    colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]  # More vibrant colors
    
    # Calculate statistics
    stats = []
    for metric in metrics:
        stats.append({
            'mean': np.mean(metric),
            'std': np.std(metric),
            'min': np.min(metric),
            'max': np.max(metric)
        })

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(15, 12))
    fig.suptitle(f'{model_name} - Performance Analysis', fontsize=16, fontweight='bold')

    x = range(1, len(accuracy) + 1)

    # Flatten axes for easier iteration
    axes_flat = axes.flatten()

    for i, (ax, metric, name, color, stat) in enumerate(zip(axes_flat, metrics, metric_names, colors, stats)):
        # Plot main line
        ax.plot(x, metric, color=color, linewidth=2.5, marker='o', markersize=6, 
                label=f'{name}', alpha=0.8)
        
        # Add trend line
        z = np.polyfit(x, metric, 1)
        p = np.poly1d(z)
        ax.plot(x, p(x), "--", color=color, alpha=0.6, linewidth=1.5, label='Trend')
        
        # Add mean line
        ax.axhline(y=stat['mean'], color=color, linestyle=':', alpha=0.7, linewidth=2)
        
        # Fill between min and max for confidence interval visualization
        ax.fill_between(x, stat['min'], stat['max'], color=color, alpha=0.1)
        
        # Styling
        ax.set_title(f'{name}\nMean: {stat["mean"]:.3f} ± {stat["std"]:.3f}', 
                    fontweight='bold', fontsize=12)
        ax.set_ylabel(name, fontsize=11)
        ax.set_xlabel('Epoch', fontsize=11)
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.legend(loc='lower right', fontsize=9)
        
        # Set consistent y-axis limits
        ax.set_ylim(max(0, stat['min'] - 0.05), min(1, stat['max'] + 0.05))
        
        # Add text box with statistics
        textstr = f'Min: {stat["min"]:.3f}\nMax: {stat["max"]:.3f}\nStd: {stat["std"]:.3f}'
        props = dict(boxstyle='round', facecolor=color, alpha=0.15)
        ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=9,
                verticalalignment='top', bbox=props)

    # Add overall summary
    overall_f1_mean = np.mean(f1)
    overall_f1_std = np.std(f1)
    fig.text(0.5, 0.02, f'Overall F1 Score: {overall_f1_mean:.4f} ± {overall_f1_std:.4f}', 
             ha='center', fontsize=12, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))

    plt.tight_layout(rect=[0, 0.05, 1, 0.96])

    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    save_path = f"results/{model_name}_{timestamp}.png"
    print(f"Enhanced plot saved to: {save_path}")
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()
    
    return {
        'mean_accuracy': stats[0]['mean'],
        'mean_precision': stats[1]['mean'], 
        'mean_recall': stats[2]['mean'],
        'mean_f1': stats[3]['mean'],
        'std_f1': stats[3]['std']
    }


def plot_model_comparison(results_dict):
    """
    Plot comparison of all models showing mean performance metrics.
    
    Args:
        results_dict: Dictionary with model names as keys and dict of metrics as values
                     e.g., {'SVM': {'accuracy': [0.8, 0.9], 'precision': [0.7, 0.8], ...}}
    """
    models = list(results_dict.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    metric_names = ['Accuracy', 'Precision', 'Recall', 'F1 Score']
    
    # Calculate means and stds
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
    
    # Create comparison bar chart
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('Model Performance Comparison', fontsize=16, fontweight='bold')
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for i, (metric, metric_name) in enumerate(zip(metrics, metric_names)):
        ax = axes[i//2, i%2]
        
        bars = ax.bar(models, means[metric], yerr=stds[metric], 
                     capsize=5, color=colors[:len(models)], alpha=0.8)
        
        ax.set_title(f'{metric_name} Comparison', fontweight='bold')
        ax.set_ylabel(metric_name)
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.3)
        
        # Add value labels on bars
        for bar, mean_val, std_val in zip(bars, means[metric], stds[metric]):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                   f'{mean_val:.3f}±{std_val:.3f}',
                   ha='center', va='bottom', fontsize=9)
        
        # Rotate x-axis labels if they're too long
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    save_path = f"results/model_comparison_{timestamp}.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Comparison plot saved to: {save_path}")
    plt.show()


def plot_comprehensive_comparison(results_dict):
    """
    Plot a comprehensive comparison showing all metrics for all models in one view.
    """
    models = list(results_dict.keys())
    metrics = ['accuracy', 'precision', 'recall', 'f1']
    
    # Calculate means
    data = []
    for model in models:
        row = [model]
        for metric in metrics:
            if metric in results_dict[model]:
                row.append(np.mean(results_dict[model][metric]))
            else:
                row.append(0)
        data.append(row)
    
    df = pd.DataFrame(data, columns=['Model'] + [m.capitalize() for m in metrics])
    
    # Create radar chart style comparison
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Left plot: Line plot showing all metrics for each model
    x_pos = np.arange(len(metrics))
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
    
    for i, model in enumerate(models):
        values = [df[df['Model'] == model][metric.capitalize()].iloc[0] for metric in metrics]
        ax1.plot(x_pos, values, marker='o', linewidth=2, label=model, 
                color=colors[i % len(colors)], markersize=8)
        
        # Add value labels
        for j, val in enumerate(values):
            ax1.annotate(f'{val:.3f}', (x_pos[j], val), 
                        textcoords="offset points", xytext=(0,10), ha='center')
    
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([m.capitalize() for m in metrics])
    ax1.set_ylabel('Score')
    ax1.set_title('All Models - All Metrics Comparison', fontweight='bold')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.1)
    
    # Right plot: Heatmap showing ranking
    metric_data = df.set_index('Model').values
    im = ax2.imshow(metric_data, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    
    ax2.set_xticks(np.arange(len(metrics)))
    ax2.set_yticks(np.arange(len(models)))
    ax2.set_xticklabels([m.capitalize() for m in metrics])
    ax2.set_yticklabels(models)
    ax2.set_title('Performance Heatmap', fontweight='bold')
    
    # Add text annotations on heatmap
    for i in range(len(models)):
        for j in range(len(metrics)):
            text = ax2.text(j, i, f'{metric_data[i, j]:.3f}',
                           ha="center", va="center", color="black", fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax2, shrink=0.6)
    cbar.set_label('Performance Score', rotation=270, labelpad=20)
    
    plt.tight_layout()
    
    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    save_path = f"results/comprehensive_comparison_{timestamp}.png"
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    print(f"Comprehensive comparison plot saved to: {save_path}")
    plt.show()


def create_summary_table(results_dict, best_scores=None):
    """
    Create and display a summary table of all model performances.
    
    Args:
        results_dict: Dictionary with model performance data
        best_scores: Dictionary with best cross-validation scores from hyperparameter tuning
    """
    models = list(results_dict.keys())
    
    summary_data = []
    for model in models:
        row = {'Model': model}
        
        # Calculate statistics for each metric
        for metric in ['accuracy', 'precision', 'recall', 'f1']:
            if metric in results_dict[model]:
                values = results_dict[model][metric]
                row[f'{metric.capitalize()} Mean'] = f"{np.mean(values):.4f}"
                row[f'{metric.capitalize()} Std'] = f"{np.std(values):.4f}"
            else:
                row[f'{metric.capitalize()} Mean'] = "N/A"
                row[f'{metric.capitalize()} Std'] = "N/A"
        
        # Add best CV score if available
        if best_scores and model in best_scores:
            row['Best CV F1'] = f"{best_scores[model]:.4f}" if best_scores[model] else "N/A"
        
        summary_data.append(row)
    
    df = pd.DataFrame(summary_data)
    
    print("\n" + "="*100)
    print("MODEL PERFORMANCE SUMMARY")
    print("="*100)
    print(df.to_string(index=False))
    print("="*100)
    
    # Save to CSV
    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    csv_path = f"results/model_summary_{timestamp}.csv"
    df.to_csv(csv_path, index=False)
    print(f"Summary table saved to: {csv_path}")
    
    return df
