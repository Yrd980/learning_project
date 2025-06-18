from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Model Comparison Plot")
        self.setMinimumSize(800, 600)

        # Setup central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Add a layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Create the matplotlib canvas
        self.plot_canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.layout.addWidget(self.plot_canvas)

        # Plot something
        self.plot_example()

    def plot_example(self):
        ax = self.plot_canvas.figure.add_subplot(111)
        ax.clear()  # Clear previous plot
        ax.plot([1, 2, 3], [4, 6, 5], label="Example")
        ax.set_title("Sample Plot")
        ax.legend()
        self.plot_canvas.draw()  # Refresh the canvas

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
