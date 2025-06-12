import optuna
import pandas as pd
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
from typing import Tuple, List
from util.plot import plot_model


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

        print(f"{model_name} - Epoch {epoch}:")
        print(f"  Accuracy : {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall   : {rec:.4f}")
        print(f"  F1 Score : {f1:.4f}")

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


def main(file_path: str):
    X_raw, y_raw = preprocess(file_path)
    X_pca, y_processed = apply_resampling_and_pca(X_raw, y_raw)

    models = get_models()

    for name, model in models.items():
        try:
            print(f"Training {name}...")
            acc, prec, rec, f1 = evaluate_model(name, model, X_pca, y_processed)

            # Skip hyperparameter tuning if no search space defined
            try:
                _, best_params, best_score = optimize_model(name, X_pca, y_processed)
                print(f"{name} best params:", best_params)
                print(f"{name} best score:", best_score)
            except ValueError as e:
                print(f"Skipping tuning for {name}: {e}")

            plot_model(name, acc, prec, rec, f1)
        except Exception as e:
            print(f"[ERROR] Model {name} failed: {e}")


if __name__ == "__main__":
    main("data/KC2.csv")
