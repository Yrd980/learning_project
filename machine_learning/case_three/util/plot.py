from datetime import datetime
import matplotlib.pyplot as plt
import os

# Ensure the results directory exists
os.makedirs("results", exist_ok=True)


def plot_model(model_name, accuracy, precision, recall, f1):
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
