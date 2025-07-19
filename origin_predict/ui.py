import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QCheckBox,
    QMessageBox,
)
from origin.model import model_view


class ModelCompareApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Model Comparison Tool")
        self.resize(600, 400)

        self.layout = QVBoxLayout()

        # File selector
        self.file_label = QLabel("No file selected")
        self.select_file_btn = QPushButton("Select CSV File")
        self.select_file_btn.clicked.connect(self.select_file)
        self.layout.addWidget(self.file_label)
        self.layout.addWidget(self.select_file_btn)

        # Model selection checkboxes
        self.model_names = [
            "Decision Tree",
            "Stacking",
            "SVM",
            "KNN",
            "Random Forest",
            "Naive Bayes",
        ]
        self.model_checkboxes = [QCheckBox(name) for name in self.model_names]
        for cb in self.model_checkboxes:
            cb.setChecked(False)
            self.layout.addWidget(cb)

        # Run button
        self.run_button = QPushButton("Run Comparison")
        self.run_button.clicked.connect(self.run_comparison)
        self.layout.addWidget(self.run_button)

        self.setLayout(self.layout)
        self.file_path = ""

    def select_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )
        if path:
            self.file_path = path
            self.file_label.setText(f"Selected: {path}")

    def get_selected_models(self):
        selected_models = []
        for cb in self.model_checkboxes:
            if cb.isChecked():
                selected_models.append(cb.text())
        return selected_models

    def run_comparison(self):
        if not self.file_path:
            QMessageBox.warning(self, "Input Error", "Please select a CSV file first.")
            return

        checked = [cb.isChecked() for cb in self.model_checkboxes]
        if not any(checked):
            QMessageBox.warning(
                self, "Input Error", "Please select at least one model."
            )
            return

        model_list = self.get_selected_models()
        for model in model_list:
            model_view(self.file_path, model)

        QMessageBox.information(self, "Success", "Model comparison completed.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ModelCompareApp()
    window.show()
    sys.exit(app.exec())
