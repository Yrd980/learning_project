from datetime import datetime
import matplotlib.pyplot as plt
import os

# Ensure the results directory exists
os.makedirs("results", exist_ok=True)


def plot_single_model(model_name, accuracy, precision, recall, f1):
    """Plot metrics (Accuracy, Precision, Recall, F1) for a single model."""
    metrics = [accuracy, precision, recall, f1]
    metric_names = ["Accuracy", "Precision", "Recall", "F1"]
    colors = ["red", "blue", "green", "darkkhaki"]

    fig, axes = plt.subplots(nrows=4, ncols=1, sharex=True, figsize=(8, 10))
    fig.suptitle(model_name, fontsize=14)

    x = range(1, len(accuracy) + 1)

    for ax, metric, name, color in zip(axes, metrics, metric_names, colors):
        ax.plot(x, metric, color=color, label=name)
        ax.legend(loc="lower right", ncol=1, shadow=True, fancybox=True)
        ax.set_ylabel(name)

    axes[-1].set_xlabel("Epoch")

    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    save_path = f"results/{model_name}_{timestamp}.png"
    print(f"Plot saved to: {save_path}")
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig(save_path, dpi=300)
    plt.show()


def plot_multi_model(
    models, model_labels, colors, accuracy_data, precision_data, recall_data, f1_data
):
    """Plot all metrics for multiple models in a 2x2 grid."""
    metrics_data = [accuracy_data, precision_data, recall_data, f1_data]
    metric_names = ["Accuracy", "Precision", "Recall", "F1"]

    fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 8))
    axes = axes.flatten()
    x = range(1, len(accuracy_data[0]) + 1)

    img_name_parts = []

    for model_idx in models:
        label = model_labels[model_idx]
        color = colors[model_idx]
        img_name_parts.append(label)

        for ax, metric, name in zip(axes, metrics_data, metric_names):
            ax.plot(x, metric[model_idx], label=label, color=color)
            ax.set_title(name)
            ax.set_xlabel("Epoch")
            ax.set_ylabel(name)

    # Add legend to the last subplot
    axes[-1].legend(
        loc="upper center",
        bbox_to_anchor=(-0.1, -0.2),
        ncol=len(models),
        shadow=True,
        fancybox=True,
    )

    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    img_name = "-".join(img_name_parts) + f"_{timestamp}.png"
    save_path = f"results/{img_name}"

    print(f"Plot saved to: {save_path}")
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.show()
