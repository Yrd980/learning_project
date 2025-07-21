from flask import Flask, render_template_string, request, jsonify
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from origin.model import (
    preprocess, apply_resampling_and_pca, 
    get_models, evaluate_model, optimize_model,
    save_model_results, list_saved_models, get_best_saved_models, load_model_results
)
import warnings
warnings.filterwarnings('ignore')

plt.ioff()

app = Flask(__name__)

# Available datasets and models
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

# Split HTML into manageable parts
HTML_HEAD = """
<!DOCTYPE html>
<html>
<head>
    <title>🔍 ML Model Comparison Tool</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
        }
        .tabs {
            display: flex;
            border-bottom: 2px solid #3498db;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        .tab {
            padding: 10px 20px;
            cursor: pointer;
            background: #ecf0f1;
            border: none;
            margin-right: 5px;
            margin-bottom: 5px;
            border-radius: 5px 5px 0 0;
        }
        .tab.active {
            background: #3498db;
            color: white;
        }
        .tab-content {
            display: none;
            padding: 20px 0;
        }
        .tab-content.active {
            display: block;
        }
        .form-group {
            margin: 15px 0;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #34495e;
        }
        select, button {
            padding: 10px;
            border: 2px solid #bdc3c7;
            border-radius: 5px;
            font-size: 14px;
        }
        button {
            background: #3498db;
            color: white;
            border: none;
            cursor: pointer;
            padding: 12px 24px;
            border-radius: 5px;
            font-size: 16px;
            margin: 10px 5px;
        }
        button:hover {
            background: #2980b9;
        }
        button.secondary {
            background: #95a5a6;
        }
        button.secondary:hover {
            background: #7f8c8d;
        }
        .loading {
            display: none;
            text-align: center;
            color: #3498db;
            margin: 20px 0;
        }
        .results {
            margin-top: 20px;
            padding: 20px;
            background: #ecf0f1;
            border-radius: 5px;
        }
        .plot {
            text-align: center;
            margin: 20px 0;
        }
        .plot img {
            max-width: 100%;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .radio-group {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            margin: 10px 0;
        }
        .radio-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .checkbox-item {
            display: flex;
            align-items: center;
            gap: 8px;
            margin: 10px 0;
        }
        .error {
            color: #e74c3c;
            background: #fdf2f2;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
        }
        .success {
            color: #27ae60;
            background: #f2fdf5;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #27ae60;
        }
        .info {
            color: #2980b9;
            background: #ebf3fd;
            padding: 10px;
            border-radius: 5px;
            border-left: 4px solid #2980b9;
        }
        .saved-models-table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        .saved-models-table th,
        .saved-models-table td {
            padding: 8px 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        .saved-models-table th {
            background-color: #34495e;
            color: white;
        }
        .saved-models-table tr:hover {
            background-color: #f5f5f5;
        }
        .model-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 15px 0;
        }
        .stat-card {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #3498db;
        }
        .stat-card h4 {
            margin: 0 0 10px 0;
            color: #2c3e50;
        }
        .stat-value {
            font-size: 1.2em;
            font-weight: bold;
            color: #27ae60;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🔍 Software Defect Prediction Model Comparison</h1>
        
        <div class="tabs">
            <button class="tab active" onclick="openTab(event, 'compare')">📊 Compare All Models</button>
            <button class="tab" onclick="openTab(event, 'single')">🎯 Single Model Analysis</button>
            <button class="tab" onclick="openTab(event, 'saved')">💾 Saved Models</button>
            <button class="tab" onclick="openTab(event, 'info')">ℹ️ Information</button>
        </div>
"""

HTML_BODY = """
        <!-- Compare Models Tab -->
        <div id="compare" class="tab-content active">
            <h2>Compare All Models</h2>
            <div class="form-group">
                <label>Select Dataset:</label>
                <div class="radio-group">
                    {% for dataset in datasets %}
                    <div class="radio-item">
                        <input type="radio" name="compare_dataset" value="{{ dataset }}" 
                               {% if dataset == 'KC2' %}checked{% endif %} id="comp_{{ dataset }}">
                        <label for="comp_{{ dataset }}">{{ dataset }}</label>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="form-group">
                <div class="checkbox-item">
                    <input type="checkbox" id="use_saved_compare" checked>
                    <label for="use_saved_compare">🚀 Use Saved Models (faster, loads pre-trained models)</label>
                </div>
            </div>
            
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
                <button onclick="compareModels()">📊 Compare All Models</button>
                <button class="secondary" onclick="checkSavedModels()">🔍 Check Available Saved Models</button>
            </div>
            
            <div class="loading" id="compare_loading">
                <p>⏳ Training and comparing models... This may take a few minutes.</p>
            </div>
            
            <div id="compare_results"></div>
        </div>

        <!-- Single Model Tab -->
        <div id="single" class="tab-content">
            <h2>Single Model Analysis</h2>
            <div class="form-group">
                <label>Select Dataset:</label>
                <div class="radio-group">
                    {% for dataset in datasets %}
                    <div class="radio-item">
                        <input type="radio" name="single_dataset" value="{{ dataset }}" 
                               {% if dataset == 'KC2' %}checked{% endif %} id="single_{{ dataset }}">
                        <label for="single_{{ dataset }}">{{ dataset }}</label>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="form-group">
                <label>Select Model:</label>
                <div class="radio-group">
                    {% for model in models %}
                    <div class="radio-item">
                        <input type="radio" name="single_model" value="{{ model }}" 
                               {% if model == 'Random Forest' %}checked{% endif %} id="model_{{ loop.index }}">
                        <label for="model_{{ loop.index }}">{{ model }}</label>
                    </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="form-group">
                <div class="checkbox-item">
                    <input type="checkbox" id="save_model" checked>
                    <label for="save_model">💾 Save Model After Training</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="optimize_hyperparams" checked>
                    <label for="optimize_hyperparams">⚙️ Optimize Hyperparameters (takes longer but better results)</label>
                </div>
            </div>
            
            <button onclick="analyzeSingleModel()">📈 Analyze & Train Model</button>
            
            <div class="loading" id="single_loading">
                <p>⏳ Training and analyzing model... Please wait.</p>
            </div>
            
            <div id="single_results"></div>
        </div>

        <!-- Saved Models Tab -->
        <div id="saved" class="tab-content">
            <h2>💾 Saved Models Management</h2>
            <p>View and manage your trained models. Saved models can be reused to avoid retraining from scratch.</p>
            
            <div style="margin: 20px 0;">
                <button onclick="loadSavedModels()">🔄 Refresh Saved Models</button>
                <button class="secondary" onclick="clearAllSavedModels()">🗑️ Clear All Saved Models</button>
            </div>
            
            <div id="saved_models_content">
                <p>Click "Refresh Saved Models" to load the list...</p>
            </div>
        </div>

        <!-- Information Tab -->
        <div id="info" class="tab-content">
            <h2>About This Tool</h2>
            <p>This application provides comprehensive comparison of machine learning models for software defect prediction with advanced model management.</p>
            
            <h3>🎯 Features:</h3>
            <ul>
                <li><strong>Model Comparison</strong>: Compare all 6 models side-by-side</li>
                <li><strong>Single Model Analysis</strong>: Detailed performance analysis for individual models</li>
                <li><strong>Model Saving</strong>: Automatically save trained models to avoid retraining</li>
                <li><strong>Hyperparameter Optimization</strong>: Use Optuna for automatic parameter tuning</li>
                <li><strong>Automatic Preprocessing</strong>: SMOTE oversampling + PCA dimensionality reduction</li>
                <li><strong>Performance Visualization</strong>: Interactive charts and detailed statistics</li>
            </ul>
            
            <h3>📊 Models Included:</h3>
            <ul>
                <li>Support Vector Machine (SVM)</li>
                <li>K-Nearest Neighbors (KNN)</li>
                <li>Decision Tree</li>
                <li>Naive Bayes</li>
                <li>Random Forest</li>
                <li>Stacking Ensemble</li>
            </ul>
        </div>
    </div>
"""

HTML_SCRIPT = """
    <script>
        // Global JavaScript functions
        function openTab(evt, tabName) {
            console.log('Opening tab:', tabName);
            var i, tabcontent, tabs;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].classList.remove("active");
            }
            tabs = document.getElementsByClassName("tab");
            for (i = 0; i < tabs.length; i++) {
                tabs[i].classList.remove("active");
            }
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
            
            // Auto-load saved models when switching to that tab
            if (tabName === 'saved') {
                loadSavedModels();
            }
        }

        function getSelectedRadio(name) {
            const element = document.querySelector('input[name="' + name + '"]:checked');
            return element ? element.value : null;
        }

        function compareModels() {
            console.log('compareModels called');
            const dataset = getSelectedRadio('compare_dataset');
            const useSaved = document.getElementById('use_saved_compare').checked;
            const loading = document.getElementById('compare_loading');
            const results = document.getElementById('compare_results');
            
            if (!dataset) {
                results.innerHTML = '<div class="error">Please select a dataset</div>';
                return;
            }
            
            loading.style.display = 'block';
            results.innerHTML = '';
            
            fetch('/compare', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({dataset: dataset, use_saved: useSaved})
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.success) {
                    let statsHtml = '';
                    if (data.model_stats) {
                        statsHtml = '<div class="model-stats">';
                        for (const [model, stats] of Object.entries(data.model_stats)) {
                            statsHtml += 
                                '<div class="stat-card">' +
                                    '<h4>' + model + '</h4>' +
                                    '<div class="stat-value">F1: ' + stats.f1.toFixed(4) + '</div>' +
                                    '<div>Acc: ' + stats.accuracy.toFixed(4) + ' | Prec: ' + stats.precision.toFixed(4) + ' | Rec: ' + stats.recall.toFixed(4) + '</div>' +
                                '</div>';
                        }
                        statsHtml += '</div>';
                    }
                    
                    results.innerHTML = 
                        '<div class="success">✅ ' + data.message + '</div>' +
                        (data.used_saved ? '<div class="info">📂 Loaded from saved models</div>' : '<div class="info">🔄 Trained fresh models and saved them</div>') +
                        statsHtml +
                        '<div class="results">' +
                            '<h3>📊 Detailed Results</h3>' +
                            '<pre>' + data.results_text + '</pre>' +
                        '</div>' +
                        (data.plot ? '<div class="plot"><img src="' + data.plot + '" alt="Comparison Plot"></div>' : '');
                } else {
                    results.innerHTML = '<div class="error">❌ ' + data.message + '</div>';
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                results.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            });
        }

        function analyzeSingleModel() {
            console.log('analyzeSingleModel called');
            const dataset = getSelectedRadio('single_dataset');
            const model = getSelectedRadio('single_model');
            const saveModel = document.getElementById('save_model').checked;
            const optimizeHyperparams = document.getElementById('optimize_hyperparams').checked;
            const loading = document.getElementById('single_loading');
            const results = document.getElementById('single_results');
            
            if (!dataset || !model) {
                results.innerHTML = '<div class="error">Please select both dataset and model</div>';
                return;
            }
            
            loading.style.display = 'block';
            results.innerHTML = '';
            
            fetch('/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    dataset: dataset, 
                    model: model, 
                    save_model: saveModel,
                    optimize_hyperparams: optimizeHyperparams
                })
            })
            .then(response => response.json())
            .then(data => {
                loading.style.display = 'none';
                if (data.success) {
                    let hyperparamInfo = '';
                    if (data.best_params && Object.keys(data.best_params).length > 0) {
                        hyperparamInfo = 
                            '<div class="info">' +
                                '<strong>🎯 Optimized Hyperparameters:</strong><br>' +
                                JSON.stringify(data.best_params, null, 2).replace(/[{}",]/g, '').replace(/\\n/g, '<br>') +
                                '<br><strong>Best CV F1 Score:</strong> ' + (data.best_score ? data.best_score.toFixed(4) : 'N/A') +
                            '</div>';
                    }
                    
                    results.innerHTML = 
                        '<div class="success">✅ Analysis completed for ' + model + ' on ' + dataset + '</div>' +
                        (data.model_saved ? '<div class="info">💾 Model saved successfully</div>' : '') +
                        hyperparamInfo +
                        '<div class="results">' +
                            '<h3>📈 Performance Statistics</h3>' +
                            '<pre>' + data.stats_text + '</pre>' +
                        '</div>' +
                        (data.plot ? '<div class="plot"><img src="' + data.plot + '" alt="Model Performance Plot"></div>' : '');
                } else {
                    results.innerHTML = '<div class="error">❌ ' + data.message + '</div>';
                }
            })
            .catch(error => {
                loading.style.display = 'none';
                results.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            });
        }

        function loadSavedModels() {
            console.log('loadSavedModels called');
            const content = document.getElementById('saved_models_content');
            content.innerHTML = '<p>⏳ Loading saved models...</p>';
            
            fetch('/saved_models')
            .then(response => response.json())
            .then(data => {
                if (data.success && data.models.length > 0) {
                    let tableHtml = 
                        '<h3>📊 Saved Models (' + data.models.length + ' total)</h3>' +
                        '<table class="saved-models-table">' +
                            '<thead>' +
                                '<tr>' +
                                    '<th>Model</th>' +
                                    '<th>Dataset</th>' +
                                    '<th>F1 Score</th>' +
                                    '<th>CV Score</th>' +
                                    '<th>Timestamp</th>' +
                                '</tr>' +
                            '</thead>' +
                            '<tbody>';
                    
                    data.models.forEach(function(model) {
                        tableHtml += 
                            '<tr>' +
                                '<td><strong>' + model.model_name + '</strong></td>' +
                                '<td>' + model.dataset_name + '</td>' +
                                '<td>' + model.mean_f1.toFixed(4) + '</td>' +
                                '<td>' + (model.best_cv_score ? model.best_cv_score.toFixed(4) : 'N/A') + '</td>' +
                                '<td>' + model.timestamp + '</td>' +
                            '</tr>';
                    });
                    
                    tableHtml += '</tbody></table>';
                    content.innerHTML = tableHtml;
                } else {
                    content.innerHTML = '<div class="info">📭 No saved models found. Train some models first!</div>';
                }
            })
            .catch(error => {
                content.innerHTML = '<div class="error">❌ Error loading saved models: ' + error.message + '</div>';
            });
        }

        function checkSavedModels() {
            console.log('checkSavedModels called');
            const dataset = getSelectedRadio('compare_dataset');
            const results = document.getElementById('compare_results');
            
            if (!dataset) {
                results.innerHTML = '<div class="error">Please select a dataset</div>';
                return;
            }
            
            fetch('/check_saved', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({dataset: dataset})
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    if (data.saved_models.length > 0) {
                        let modelsHtml = '<div class="info"><strong>📂 Available saved models for ' + dataset + ':</strong><br>';
                        data.saved_models.forEach(function(model) {
                            modelsHtml += '• ' + model.model_name + ' (F1: ' + model.mean_f1.toFixed(4) + ', saved: ' + model.timestamp + ')<br>';
                        });
                        modelsHtml += '</div>';
                        results.innerHTML = modelsHtml;
                    } else {
                        results.innerHTML = '<div class="info">📭 No saved models found for ' + dataset + '. Models will be trained from scratch.</div>';
                    }
                } else {
                    results.innerHTML = '<div class="error">❌ ' + data.message + '</div>';
                }
            })
            .catch(error => {
                results.innerHTML = '<div class="error">❌ Error: ' + error.message + '</div>';
            });
        }

        function clearAllSavedModels() {
            console.log('clearAllSavedModels called');
            if (!confirm('Are you sure you want to delete all saved models? This cannot be undone.')) {
                return;
            }
            
            fetch('/clear_saved_models', {method: 'POST'})
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.getElementById('saved_models_content').innerHTML = 
                        '<div class="success">✅ All saved models have been cleared.</div>';
                } else {
                    document.getElementById('saved_models_content').innerHTML = 
                        '<div class="error">❌ Error: ' + data.message + '</div>';
                }
            })
            .catch(error => {
                document.getElementById('saved_models_content').innerHTML = 
                    '<div class="error">❌ Error: ' + error.message + '</div>';
            });
        }

        // Auto-load saved models when page loads
        window.onload = function() {
            console.log('Page loaded successfully');
            loadSavedModels();
        };
        
        // Test function
        function testJS() {
            alert('JavaScript is working!');
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    # Combine all HTML parts
    full_html = HTML_HEAD + HTML_BODY + HTML_SCRIPT
    return render_template_string(full_html, datasets=DATASETS, models=MODELS)

@app.route('/compare', methods=['POST'])
def compare_models():
    try:
        data = request.get_json()
        dataset_name = data['dataset']
        use_saved = data.get('use_saved', False)
        
        file_path = f"data/{dataset_name}.csv"
        
        # Preprocess data
        X_raw, y_raw = preprocess(file_path)
        X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
        
        results = {}
        best_scores = {}
        used_saved = False
        
        if use_saved:
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
            return jsonify({'success': False, 'message': 'No models could be evaluated'})
        
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
        
        # Create results text
        results_text = f"{dataset_name} Model Comparison Results:\n\n"
        for model, scores in results.items():
            results_text += f"{model}:\n"
            results_text += f"  Accuracy:  {scores['accuracy']:.4f}\n"
            results_text += f"  Precision: {scores['precision']:.4f}\n"
            results_text += f"  Recall:    {scores['recall']:.4f}\n"
            results_text += f"  F1 Score:  {scores['f1']:.4f}\n\n"
        
        return jsonify({
            'success': True,
            'message': f'Successfully compared {len(results)} models on {dataset_name} dataset',
            'results_text': results_text,
            'plot': plot_data,
            'model_stats': results,
            'used_saved': used_saved
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/analyze', methods=['POST'])
def analyze_single_model():
    try:
        data = request.get_json()
        dataset_name = data['dataset']
        model_name = data['model']
        save_model = data.get('save_model', True)
        optimize_hyperparams = data.get('optimize_hyperparams', True)
        
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
        
        # Create stats text
        stats_text = f"{model_name} Performance Statistics on {dataset_name}:\n\n"
        stats_text += f"Accuracy:  {np.mean(acc):.4f} ± {np.std(acc):.4f}\n"
        stats_text += f"           Range: {np.min(acc):.4f} - {np.max(acc):.4f}\n\n"
        stats_text += f"Precision: {np.mean(prec):.4f} ± {np.std(prec):.4f}\n"
        stats_text += f"           Range: {np.min(prec):.4f} - {np.max(prec):.4f}\n\n"
        stats_text += f"Recall:    {np.mean(rec):.4f} ± {np.std(rec):.4f}\n"
        stats_text += f"           Range: {np.min(rec):.4f} - {np.max(rec):.4f}\n\n"
        stats_text += f"F1 Score:  {np.mean(f1):.4f} ± {np.std(f1):.4f}\n"
        stats_text += f"           Range: {np.min(f1):.4f} - {np.max(f1):.4f}\n"
        
        return jsonify({
            'success': True,
            'stats_text': stats_text,
            'plot': plot_data,
            'model_saved': model_saved,
            'best_params': best_params,
            'best_score': best_score
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/saved_models')
def get_saved_models():
    try:
        saved_models = list_saved_models()
        return jsonify({
            'success': True,
            'models': saved_models
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/check_saved', methods=['POST'])
def check_saved_models():
    try:
        data = request.get_json()
        dataset_name = data['dataset']
        
        best_saved = get_best_saved_models(dataset_name)
        saved_models = []
        
        for model_name, info in best_saved.items():
            saved_models.append({
                'model_name': model_name,
                'mean_f1': info['mean_f1'],
                'timestamp': info['timestamp']
            })
        
        return jsonify({
            'success': True,
            'saved_models': saved_models
        })
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

@app.route('/clear_saved_models', methods=['POST'])
def clear_saved_models():
    try:
        import shutil
        import os
        
        if os.path.exists('saved_models'):
            shutil.rmtree('saved_models')
            os.makedirs('saved_models', exist_ok=True)
        
        return jsonify({'success': True, 'message': 'All saved models cleared'})
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})

if __name__ == '__main__':
    print("🚀 Starting ML Model Comparison Web App with Model Storage...")
    print("📖 Open your browser and go to: http://localhost:5000")
    print("💾 Models will be automatically saved after training")
    print("🧪 You can also test basic functionality at: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5000) 