import optuna
import pandas as pd
import numpy as np
import joblib
import os
import json
from datetime import datetime
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier, StackingClassifier
from sklearn.linear_model import LogisticRegression
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import TomekLinks
from typing import Tuple, List, Dict, Any
from util.plot import plot_model, plot_model_comparison, plot_comprehensive_comparison, create_summary_table

# Ensure models directory exists
os.makedirs("saved_models", exist_ok=True)


def preprocess(file_path: str) -> Tuple[pd.DataFrame, pd.Series]:
    columns = [
        "loc",
        "v(g)",
        "ev(g)",
        "iv(g)",
        "n",
        "v",
        "l",
        "d",
        "i",
        "e",
        "b",
        "t",
        "lOCode",
        "lOComment",
        "lOBlank",
        "lOCodeAndComment",
        "uniq_Op",
        "uniq_Opnd",
        "total_Op",
        "total_Opnd",
        "branchCount",
    ]
    df = pd.read_csv(file_path)
    X = df[columns]
    y = df["defects"]
    return X, y


def apply_resampling_and_pca(
    X: pd.DataFrame, y: pd.Series
) -> Tuple[pd.DataFrame, pd.Series]:
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    tl = TomekLinks()
    X_cleaned, y_cleaned = tl.fit_resample(X_resampled, y_resampled)

    pca = PCA(n_components=3)
    X_pca = pca.fit_transform(X_cleaned)

    return X_pca, y_cleaned


def evaluate_model(
    model_name: str, model, X, y, epochs: int = 10
) -> Tuple[List[float], List[float], List[float], List[float]]:
    acc_list, prec_list, rec_list, f1_list = [], [], [], []

    print(f"\nEvaluating {model_name}...")
    for epoch in range(1, epochs + 1):
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=epoch
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)

        acc_list.append(acc)
        prec_list.append(prec)
        rec_list.append(rec)
        f1_list.append(f1)

        if epoch <= 3 or epoch % 5 == 0:  # Reduce verbose output
            print(f"  Epoch {epoch}: Acc={acc:.4f}, Prec={prec:.4f}, Rec={rec:.4f}, F1={f1:.4f}")

    print(f"  {model_name} Final Averages: Acc={np.mean(acc_list):.4f}±{np.std(acc_list):.4f}, "
          f"F1={np.mean(f1_list):.4f}±{np.std(f1_list):.4f}")
    
    return acc_list, prec_list, rec_list, f1_list


def get_search_space(trial: optuna.Trial, model_name: str):
    if model_name == "SVM":
        return SVC(
            kernel="poly",
            C=trial.suggest_float("C", 0.01, 10.0, log=True),
            degree=trial.suggest_int("degree", 1, 5),
            class_weight="balanced",
        )
    elif model_name == "KNN":
        return KNeighborsClassifier(
            n_neighbors=trial.suggest_int("n_neighbors", 1, 20),
            weights=trial.suggest_categorical("weights", ["uniform", "distance"]),
            p=trial.suggest_int("p", 1, 2),
        )
    elif model_name == "Decision Tree":
        return DecisionTreeClassifier(
            criterion=trial.suggest_categorical("criterion", ["gini", "entropy"]),
            max_depth=trial.suggest_int("max_depth", 3, 30),
        )
    elif model_name == "Random Forest":
        return RandomForestClassifier(
            n_estimators=trial.suggest_int("n_estimators", 100, 1000),
            max_depth=trial.suggest_int("max_depth", 10, 100),
            min_samples_split=trial.suggest_int("min_samples_split", 2, 10),
            min_samples_leaf=trial.suggest_int("min_samples_leaf", 1, 5),
            random_state=42,
        )
    else:
        raise ValueError(f"No tuning space defined for model: {model_name}")


def get_models():
    base_learners = [
        (
            "rf",
            RandomForestClassifier(n_estimators=1000, random_state=42, max_depth=200),
        ),
        ("dt", DecisionTreeClassifier(criterion="entropy", max_depth=10)),
    ]
    meta_learner = LogisticRegression()

    return {
        "SVM": SVC(kernel="poly", C=1.0, degree=1, class_weight="balanced"),
        "KNN": KNeighborsClassifier(n_neighbors=6, weights="distance", p=1),
        "Decision Tree": DecisionTreeClassifier(criterion="entropy", max_depth=15),
        "Naive Bayes": BernoulliNB(),
        "Random Forest": RandomForestClassifier(
            n_estimators=490,
            random_state=42,
            max_depth=95,
            min_samples_split=7,
            min_samples_leaf=3,
        ),
        "Stacking": StackingClassifier(
            estimators=base_learners, final_estimator=meta_learner
        ),
    }


def optimize_model(model_name: str, X, y, n_trials: int = 30):

    if model_name in ["Naive Bayes", "Stacking"]:
        print(f"[INFO] {model_name} has no tuning space. Using default parameters.")
        model = get_models()[model_name]
        score = cross_val_score(model, X, y, scoring="f1", cv=3).mean()
        return model, {}, score

    def objective(trial):
        model = get_search_space(trial, model_name)
        score = cross_val_score(model, X, y, scoring="f1", cv=3).mean()
        return score

    study = optuna.create_study(direction="maximize")
    study.optimize(objective, n_trials=n_trials)

    best_params = study.best_params
    best_score = study.best_value
    best_model = get_search_space(study.best_trial, model_name)

    return best_model, best_params, best_score


def save_model_results(model_name: str, model, results: Dict, best_params: Dict, best_score: float, dataset_name: str):
    """Save trained model and its results for future use."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create model directory
    model_dir = f"saved_models/{dataset_name}_{timestamp}"
    os.makedirs(model_dir, exist_ok=True)
    
    # Save model
    model_path = f"{model_dir}/{model_name}_model.joblib"
    joblib.dump(model, model_path)
    
    # Save results and metadata
    metadata = {
        'model_name': model_name,
        'dataset_name': dataset_name,
        'timestamp': timestamp,
        'best_params': best_params,
        'best_cv_score': best_score,
        'results': {
            'mean_accuracy': np.mean(results['accuracy']),
            'std_accuracy': np.std(results['accuracy']),
            'mean_precision': np.mean(results['precision']),
            'std_precision': np.std(results['precision']),
            'mean_recall': np.mean(results['recall']),
            'std_recall': np.std(results['recall']),
            'mean_f1': np.mean(results['f1']),
            'std_f1': np.std(results['f1'])
        },
        'raw_results': results,
        'model_path': model_path
    }
    
    metadata_path = f"{model_dir}/{model_name}_metadata.json"
    with open(metadata_path, 'w') as f:
        # Convert numpy types to native Python types for JSON serialization
        json_metadata = json.loads(json.dumps(metadata, default=lambda x: float(x) if isinstance(x, np.floating) else list(x) if isinstance(x, np.ndarray) else x))
        json.dump(json_metadata, f, indent=2)
    
    print(f"  Model saved: {model_path}")
    print(f"  Metadata saved: {metadata_path}")
    
    return model_dir

def load_model_results(model_dir: str, model_name: str):
    """Load saved model and its results."""
    model_path = f"{model_dir}/{model_name}_model.joblib"
    metadata_path = f"{model_dir}/{model_name}_metadata.json"
    
    if not os.path.exists(model_path) or not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Model files not found in {model_dir}")
    
    # Load model
    model = joblib.load(model_path)
    
    # Load metadata
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    
    return model, metadata

def list_saved_models(dataset_name: str = None):
    """List all saved models, optionally filtered by dataset."""
    if not os.path.exists("saved_models"):
        return []
    
    saved_models = []
    for item in os.listdir("saved_models"):
        item_path = os.path.join("saved_models", item)
        if os.path.isdir(item_path):
            if dataset_name is None or item.startswith(dataset_name):
                # Look for metadata files in this directory
                for file in os.listdir(item_path):
                    if file.endswith("_metadata.json"):
                        metadata_path = os.path.join(item_path, file)
                        try:
                            with open(metadata_path, 'r') as f:
                                metadata = json.load(f)
                            saved_models.append({
                                'directory': item,
                                'model_name': metadata['model_name'],
                                'dataset_name': metadata['dataset_name'],
                                'timestamp': metadata['timestamp'],
                                'best_cv_score': metadata['best_cv_score'],
                                'mean_f1': metadata['results']['mean_f1']
                            })
                        except:
                            continue
    
    return sorted(saved_models, key=lambda x: x['timestamp'], reverse=True)

def get_best_saved_models(dataset_name: str):
    """Get the best saved model for each model type for a given dataset."""
    saved_models = list_saved_models(dataset_name)
    best_models = {}
    
    for model_info in saved_models:
        model_name = model_info['model_name']
        f1_score = model_info['mean_f1']
        
        if model_name not in best_models or f1_score > best_models[model_name]['mean_f1']:
            best_models[model_name] = model_info
    
    return best_models


def main(file_path: str, use_saved_models: bool = False):
    print(f"Loading and preprocessing data from: {file_path}")
    dataset_name = os.path.splitext(os.path.basename(file_path))[0]
    
    X_raw, y_raw = preprocess(file_path)
    X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)
    
    print(f"Dataset shape after preprocessing: {X_pca.shape}")
    print(f"Class distribution: {np.bincount(y_processed)}")

    results_dict = {}
    best_scores = {}
    saved_model_dir = None

    if use_saved_models:
        print("\n" + "="*80)
        print("CHECKING FOR SAVED MODELS")
        print("="*80)
        
        best_saved = get_best_saved_models(dataset_name)
        if best_saved:
            print(f"Found {len(best_saved)} saved model types for {dataset_name}")
            for model_name, info in best_saved.items():
                print(f"  {model_name}: F1={info['mean_f1']:.4f} (saved {info['timestamp']})")
            
            # Load the best models
            for model_name, info in best_saved.items():
                try:
                    model_dir = f"saved_models/{info['directory']}"
                    model, metadata = load_model_results(model_dir, model_name)
                    
                    results_dict[model_name] = metadata['raw_results']
                    best_scores[model_name] = metadata['best_cv_score']
                    
                    print(f"  Loaded {model_name} from saved models")
                except Exception as e:
                    print(f"  Failed to load {model_name}: {e}")
            
            if results_dict:
                print(f"Successfully loaded {len(results_dict)} models from cache")
            else:
                print("No models could be loaded, will train from scratch")
                use_saved_models = False
        else:
            print(f"No saved models found for {dataset_name}, will train from scratch")
            use_saved_models = False

    if not use_saved_models:
        models = get_models()

        print("\n" + "="*80)
        print("STARTING MODEL EVALUATION")
        print("="*80)

        for name, model in models.items():
            try:
                # Evaluate model performance
                acc, prec, rec, f1 = evaluate_model(name, model, X_pca, y_processed)
                
                # Store results
                results_dict[name] = {
                    'accuracy': acc,
                    'precision': prec,
                    'recall': rec,
                    'f1': f1
                }

                # Hyperparameter tuning
                print(f"  Optimizing hyperparameters for {name}...")
                try:
                    optimized_model, best_params, best_score = optimize_model(name, X_pca, y_processed)
                    best_scores[name] = best_score
                    print(f"  {name} best params: {best_params}")
                    print(f"  {name} best CV F1: {best_score:.4f}")
                    
                    # Save the optimized model
                    if saved_model_dir is None:
                        saved_model_dir = f"saved_models/{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        os.makedirs(saved_model_dir, exist_ok=True)
                    
                    save_model_results(name, optimized_model, results_dict[name], 
                                     best_params, best_score, dataset_name)
                    
                except ValueError as e:
                    print(f"  Skipping tuning for {name}: {e}")
                    best_scores[name] = None
                    
                    # Save the base model
                    if saved_model_dir is None:
                        saved_model_dir = f"saved_models/{dataset_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                        os.makedirs(saved_model_dir, exist_ok=True)
                    
                    save_model_results(name, model, results_dict[name], 
                                     {}, None, dataset_name)
                
            except Exception as e:
                print(f"[ERROR] Model {name} failed: {e}")

    # Generate visualizations (same for both saved and new models)
    print("\n" + "="*80)
    print("GENERATING COMPARISON VISUALIZATIONS")
    print("="*80)

    if results_dict:
        # Generate individual plots for each model
        for name, results in results_dict.items():
            plot_model(name, results['accuracy'], results['precision'], 
                      results['recall'], results['f1'])
        
        # Summary table
        create_summary_table(results_dict, best_scores)
        
        # Comparison plots
        plot_model_comparison(results_dict)
        plot_comprehensive_comparison(results_dict)
        
        # Find and display best performing model
        print("\n" + "="*80)
        print("BEST PERFORMING MODELS")
        print("="*80)
        
        for metric in ['accuracy', 'precision', 'recall', 'f1']:
            best_model = max(results_dict.keys(), 
                           key=lambda x: np.mean(results_dict[x][metric]))
            best_score = np.mean(results_dict[best_model][metric])
            print(f"Best {metric.capitalize()}: {best_model} ({best_score:.4f})")
        
        # Best hyperparameter tuning score
        if any(score is not None for score in best_scores.values()):
            best_tuned_model = max([k for k, v in best_scores.items() if v is not None], 
                                 key=lambda x: best_scores[x])
            print(f"Best CV F1 Score: {best_tuned_model} ({best_scores[best_tuned_model]:.4f})")
        
        print("="*80)
        
        if not use_saved_models and saved_model_dir:
            print(f"\nModels saved to: {saved_model_dir}")
    else:
        print("No results to display - all models failed!")


def model_view(file_path, model_name):
    print(f"Single model evaluation for: {model_name}")
    X_raw, y_raw = preprocess(file_path)
    X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)

    model = get_models()[model_name]
    acc, prec, rec, f1 = evaluate_model(model_name, model, X_pca, y_processed)
    
    print(f"Optimizing {model_name}...")
    try:
        _, best_params, best_score = optimize_model(model_name, X_pca, y_processed)
        print(f"{model_name} best params: {best_params}")
        print(f"{model_name} best CV F1 score: {best_score}")
    except ValueError as e:
        print(f"No hyperparameter tuning for {model_name}: {e}")

    plot_model(model_name, acc, prec, rec, f1)


if __name__ == "__main__":
    import sys
    
    # Check command line arguments
    use_saved = "--use-saved" in sys.argv
    file_path = "data/KC2.csv"
    
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        file_path = sys.argv[1]
    
    main(file_path, use_saved_models=use_saved)
