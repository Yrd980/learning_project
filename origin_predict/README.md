# 🔍 Software Defect Prediction - ML Model Comparison Tool

A comprehensive machine learning framework for comparing and analyzing different algorithms in software defect prediction using NASA and other software metrics datasets.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![PyTorch](https://img.shields.io/badge/PyTorch-v2.0+-red.svg)
![Scikit-learn](https://img.shields.io/badge/scikit--learn-v1.0+-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🎯 Project Overview

This project provides a complete pipeline for software defect prediction analysis, featuring:

- **6 Traditional ML Models**: SVM, KNN, Decision Tree, Naive Bayes, Random Forest, Stacking
- **Deep Learning**: PyTorch-based Neural Network implementation
- **Advanced Preprocessing**: SMOTE oversampling + Tomek Links + PCA
- **Hyperparameter Optimization**: Optuna-based automated tuning
- **Interactive UI**: Gradio web interface and Jupyter notebook
- **Model Persistence**: Save/load trained models with metadata
- **Comprehensive Visualization**: Performance plots and comparison charts

## 📊 Supported Datasets

| Dataset | Description | Domain |
|---------|-------------|---------|
| **KC1** | NASA software defect dataset | Spacecraft instrument |
| **KC2** | NASA software defect dataset | Storage management |
| **CM1** | NASA Metrics Data Program | Spacecraft instrument |
| **JM1** | Real-time predictive systems | Real-time ground system |
| **PC1** | Flight software | Earth orbiting satellite |

## 🚀 Features

### 🔧 **Core Functionality**
- **Automated Preprocessing Pipeline**: Handles imbalanced data with SMOTE + Tomek Links + PCA
- **Multiple Model Support**: Traditional ML + Deep Learning approaches
- **Performance Metrics**: Accuracy, Precision, Recall, F1-Score with statistical analysis
- **Cross-Validation**: Robust evaluation with multiple train-test splits
- **Model Comparison**: Side-by-side performance analysis

### 🎨 **Interfaces**
- **Gradio Web UI**: Interactive web interface with model management
- **Jupyter Notebook**: Comprehensive analysis and visualization environment
- **Command Line**: Direct script execution with options

### 📈 **Advanced Analytics**
- **Hyperparameter Optimization**: Bayesian optimization using Optuna
- **Model Persistence**: Automatic saving with metadata and performance tracking
- **Cross-Dataset Analysis**: Compare model generalization across datasets
- **Statistical Visualization**: Trend lines, confidence intervals, heatmaps

## 📦 Installation

### Prerequisites
- Python 3.8+
- CUDA (optional, for GPU acceleration)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd origin_predict
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare Data
Place your dataset files in the `data/` directory:
```
data/
├── KC1.csv
├── KC2.csv
├── CM1.csv
├── JM1.csv
└── PC1.csv
```

## 🎮 Usage

### 🌐 **Web Interface (Recommended)**
Launch the interactive Gradio web application:

```bash
python ui.py
python simple_ui.py
marimo edit Software_Defect_Prediction_Analysis.py
```

Access the web interface at `http://localhost:7860`

**Features:**
- 📊 **Compare All Models**: Side-by-side comparison with saved model support
- 🎯 **Single Model Analysis**: Detailed analysis with hyperparameter optimization
- 💾 **Model Management**: View, load, and manage saved models
- ℹ️ **Information**: Comprehensive documentation and help

### 📓 **Jupyter Notebook**
For detailed analysis and experimentation:

```bash
jupyter notebook Software_Defect_Prediction_Analysis.ipynb
```

**Interactive Functions:**
```python
# Quick comparison (3 epochs)
results = quick_comparison('KC2')

# Detailed analysis (10 epochs)
results = detailed_analysis('KC1')

# Compare across datasets
comparison = compare_datasets()

# Interactive guided analysis
results = interactive_analysis()
```

### 💻 **Command Line Interface**
Run analysis directly from terminal:

```bash
# Basic analysis
python origin/model.py data/KC2.csv

# Use saved models
python origin/model.py data/KC2.csv --use-saved

# Single model view
python model/model.py  # For neural network
```

## 🏗️ Project Structure

```
origin_predict/
├── 📁 data/                    # Dataset files
│   ├── KC1.csv
│   ├── KC2.csv
│   └── ...
├── 📁 model/                   # Neural network implementation
│   ├── dataset.py             # PyTorch dataset class
│   └── model.py               # Neural network model
├── 📁 origin/                  # Traditional ML models
│   └── model.py               # Main analysis pipeline
├── 📁 util/                    # Utility functions
│   ├── __init__.py
│   └── plot.py                # Visualization tools
├── 📁 saved_models/           # Saved model artifacts
├── 📁 results/                # Generated plots and reports
├── 📄 ui.py                   # Gradio web interface
├── 📄 simple_ui.py            # Simplified interface
├── 📓 Software_Defect_Prediction_Analysis.ipynb  # Jupyter notebook
├── 📄 requirements.txt        # Dependencies
└── 📄 README.md              # This file
```

## 🔬 Technical Details

### **Preprocessing Pipeline**
1. **Feature Selection**: 21 software metrics (LOC, complexity, Halstead metrics)
2. **SMOTE Oversampling**: Balance class distribution
3. **Tomek Links**: Remove borderline samples
4. **PCA**: Dimensionality reduction to 3 components

### **Models Implemented**

| Model | Library | Hyperparameter Tuning |
|-------|---------|----------------------|
| SVM | scikit-learn | ✅ (C, degree, kernel) |
| KNN | scikit-learn | ✅ (n_neighbors, weights, p) |
| Decision Tree | scikit-learn | ✅ (criterion, max_depth, min_samples) |
| Naive Bayes | scikit-learn | ❌ (no tunable params) |
| Random Forest | scikit-learn | ✅ (n_estimators, max_depth, min_samples) |
| Stacking | scikit-learn | ❌ (ensemble method) |
| Neural Network | PyTorch | Manual architecture |

### **Performance Metrics**
- **Accuracy**: Overall correctness
- **Precision**: True positives / (True positives + False positives)
- **Recall**: True positives / (True positives + False negatives)
- **F1-Score**: Harmonic mean of precision and recall

## 📊 Example Results

### Model Comparison on KC2 Dataset
```
🏆 BEST PERFORMING MODELS
══════════════════════════════════════════════════════════════════════════════════
Best Accuracy: Random Forest (0.8234)
Best Precision: SVM (0.7891)
Best Recall: Decision Tree (0.8456)
Best F1 Score: Random Forest (0.8012)
Best CV F1 Score: Random Forest (0.7956)
══════════════════════════════════════════════════════════════════════════════════
```

### Cross-Dataset Performance
| Model | KC1 F1 | KC2 F1 | CM1 F1 | Avg F1 |
|-------|---------|---------|---------|---------|
| Random Forest | 0.801 | 0.823 | 0.789 | 0.804 |
| SVM | 0.756 | 0.778 | 0.743 | 0.759 |
| Decision Tree | 0.734 | 0.756 | 0.712 | 0.734 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **NASA Metrics Data Program** for providing the software defect datasets
- **Scikit-learn** for machine learning algorithms
- **PyTorch** for deep learning capabilities
- **Optuna** for hyperparameter optimization
- **Gradio** for the interactive web interface

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](../../issues) section
2. Review the Jupyter notebook for detailed examples
3. Use the web interface help section
4. Create a new issue with detailed information

## 🔮 Future Enhancements

- [ ] Additional deep learning architectures (CNN, LSTM)
- [ ] More datasets from different domains
- [ ] Ensemble method combinations
- [ ] Real-time prediction API
- [ ] Docker containerization
- [ ] MLOps pipeline integration

---

**Made with ❤️ for the software engineering research community** 