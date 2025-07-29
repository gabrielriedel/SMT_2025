from train_set import *
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report, precision_recall_curve
import numpy as np
import bambi as bmb
import pandas as pd
import arviz as az

class Model:

    def logistic_regression_model(split_data):
        X_train, X_val, X_test = split_data["X"]
        y_train, y_val, y_test = split_data["y"]

        # Create a pipeline: scaling + logistic regression
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("logit", LogisticRegression(class_weight="balanced"))
        ])

        # Fit the model
        pipeline.fit(X_train, y_train)

        # Predict probabilities on validation set
        val_probs = pipeline.predict_proba(X_val)[:, 1]

        # Find best threshold using F1 score
        precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
        best_idx = f1_scores.argmax()
        best_threshold = thresholds[best_idx]

        print(f"Best threshold (validation): {best_threshold:.3f}")
        
        val_preds = (val_probs >= best_threshold).astype(int)
        print("Unique predictions:", np.unique(val_preds, return_counts=True))

        # Validation metrics
        auc = roc_auc_score(y_val, val_probs)
        acc = accuracy_score(y_val, val_preds)
        precision = precision_score(y_val, val_preds)
        recall = recall_score(y_val, val_preds)
        f1 = f1_score(y_val, val_preds)

        print(f"\n[Validation Metrics]")
        print(f"AUC:       {auc:.3f}")
        print(f"Accuracy:  {acc:.3f}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall:    {recall:.3f}")
        print(f"F1 Score:  {f1:.3f}")

        # Test evaluation
        test_probs = pipeline.predict_proba(X_test)[:, 1]
        test_preds = (test_probs >= best_threshold).astype(int)

        test_auc = roc_auc_score(y_test, test_probs)
        test_acc = accuracy_score(y_test, test_preds)
        test_precision = precision_score(y_test, test_preds)
        test_recall = recall_score(y_test, test_preds)
        test_f1 = f1_score(y_test, test_preds)

        print(f"\n[Test Metrics]")
        print(f"AUC:       {test_auc:.3f}")
        print(f"Accuracy:  {test_acc:.3f}")
        print(f"Precision: {test_precision:.3f}")
        print(f"Recall:    {test_recall:.3f}")
        print(f"F1 Score:  {test_f1:.3f}")

        return pipeline, best_threshold
    
    def random_forest_model(split_data):
        X_train, X_val, X_test = split_data["X"]
        y_train, y_val, y_test = split_data["y"]

        # Train model
        rf_model = RandomForestClassifier(n_estimators=100, class_weight="balanced", random_state=42)
        rf_model.fit(X_train, y_train)

        # Get validation probabilities
        val_probs = rf_model.predict_proba(X_val)[:, 1]

        # Tune threshold using validation set
        precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
        best_idx = f1_scores.argmax()
        best_threshold = thresholds[best_idx]

        print(f"Best threshold (validation): {best_threshold:.3f}")
        
        val_preds = (val_probs >= best_threshold).astype(int)

        # Validation metrics
        val_auc = roc_auc_score(y_val, val_probs)
        val_acc = accuracy_score(y_val, val_preds)
        val_precision = precision_score(y_val, val_preds)
        val_recall = recall_score(y_val, val_preds)
        val_f1 = f1_score(y_val, val_preds)

        print("\n[Validation Metrics]")
        print(f"AUC:       {val_auc:.3f}")
        print(f"Accuracy:  {val_acc:.3f}")
        print(f"Precision: {val_precision:.3f}")
        print(f"Recall:    {val_recall:.3f}")
        print(f"F1 Score:  {val_f1:.3f}")

        # Evaluate on test using best threshold
        test_probs = rf_model.predict_proba(X_test)[:, 1]
        test_preds = (test_probs >= best_threshold).astype(int)

        test_auc = roc_auc_score(y_test, test_probs)
        test_acc = accuracy_score(y_test, test_preds)
        test_precision = precision_score(y_test, test_preds)
        test_recall = recall_score(y_test, test_preds)
        test_f1 = f1_score(y_test, test_preds)

        print("\n[Test Metrics]")
        print(f"AUC:       {test_auc:.3f}")
        print(f"Accuracy:  {test_acc:.3f}")
        print(f"Precision: {test_precision:.3f}")
        print(f"Recall:    {test_recall:.3f}")
        print(f"F1 Score:  {test_f1:.3f}")

        return rf_model, best_threshold
    
    def knn_model(split_data, n_neighbors=5):
        X_train, X_val, X_test = split_data["X"]
        y_train, y_val, y_test = split_data["y"]

        # Create a pipeline: scale + KNN
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("knn", KNeighborsClassifier(n_neighbors=n_neighbors))
        ])

        # Fit the pipeline on training data
        pipeline.fit(X_train, y_train)

        # Predict probabilities on validation set
        val_probs = pipeline.predict_proba(X_val)[:, 1]

        # Tune threshold using validation F1 score
        precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
        best_idx = f1_scores.argmax()
        best_threshold = thresholds[best_idx]

        print(f"Best threshold (validation): {best_threshold:.3f}")

        val_preds = (val_probs >= best_threshold).astype(int)

        # Validation metrics
        val_auc = roc_auc_score(y_val, val_probs)
        val_acc = accuracy_score(y_val, val_preds)
        val_precision = precision_score(y_val, val_preds)
        val_recall = recall_score(y_val, val_preds)
        val_f1 = f1_score(y_val, val_preds)

        print("\n[Validation Metrics]")
        print(f"AUC:       {val_auc:.3f}")
        print(f"Accuracy:  {val_acc:.3f}")
        print(f"Precision: {val_precision:.3f}")
        print(f"Recall:    {val_recall:.3f}")
        print(f"F1 Score:  {val_f1:.3f}")

        # Predict on test set using best threshold
        test_probs = pipeline.predict_proba(X_test)[:, 1]
        test_preds = (test_probs >= best_threshold).astype(int)

        test_auc = roc_auc_score(y_test, test_probs)
        test_acc = accuracy_score(y_test, test_preds)
        test_precision = precision_score(y_test, test_preds)
        test_recall = recall_score(y_test, test_preds)
        test_f1 = f1_score(y_test, test_preds)

        print("\n[Test Metrics]")
        print(f"AUC:       {test_auc:.3f}")
        print(f"Accuracy:  {test_acc:.3f}")
        print(f"Precision: {test_precision:.3f}")
        print(f"Recall:    {test_recall:.3f}")
        print(f"F1 Score:  {test_f1:.3f}")

        return pipeline, best_threshold

    def xg_boost_model(split_data):
        X_train, X_val, X_test = split_data["X"]
        y_train, y_val, y_test = split_data["y"]

        # Train XGBoost
        xgb_model = XGBClassifier(
            use_label_encoder=False,
            eval_metric='logloss',
            scale_pos_weight=float((y_train == 0).sum() / (y_train == 1).sum()),  # balance positive/negative
            random_state=42
        )
        xgb_model.fit(X_train, y_train)

        # Predict probabilities on validation set
        val_probs = xgb_model.predict_proba(X_val)[:, 1]

        # Tune threshold using F1 score
        precisions, recalls, thresholds = precision_recall_curve(y_val, val_probs)
        f1_scores = 2 * (precisions * recalls) / (precisions + recalls + 1e-10)
        best_idx = f1_scores.argmax()
        best_threshold = thresholds[best_idx]

        print(f"Best threshold (validation): {best_threshold:.3f}")
        
        val_preds = (val_probs >= best_threshold).astype(int)

        # Validation metrics
        val_auc = roc_auc_score(y_val, val_probs)
        val_acc = accuracy_score(y_val, val_preds)
        val_precision = precision_score(y_val, val_preds)
        val_recall = recall_score(y_val, val_preds)
        val_f1 = f1_score(y_val, val_preds)

        print("\n[Validation Metrics]")
        print(f"AUC:       {val_auc:.3f}")
        print(f"Accuracy:  {val_acc:.3f}")
        print(f"Precision: {val_precision:.3f}")
        print(f"Recall:    {val_recall:.3f}")
        print(f"F1 Score:  {val_f1:.3f}")

        # Test evaluation
        test_probs = xgb_model.predict_proba(X_test)[:, 1]
        test_preds = (test_probs >= best_threshold).astype(int)

        test_auc = roc_auc_score(y_test, test_probs)
        test_acc = accuracy_score(y_test, test_preds)
        test_precision = precision_score(y_test, test_preds)
        test_recall = recall_score(y_test, test_preds)
        test_f1 = f1_score(y_test, test_preds)

        print("\n[Test Metrics]")
        print(f"AUC:       {test_auc:.3f}")
        print(f"Accuracy:  {test_acc:.3f}")
        print(f"Precision: {test_precision:.3f}")
        print(f"Recall:    {test_recall:.3f}")
        print(f"F1 Score:  {test_f1:.3f}")

        return xgb_model, best_threshold


    
    def evaluate_on_test(model, X_test, y_test, threshold):
        test_probs = model.predict_proba(X_test)[:, 1]
        test_preds = (test_probs >= threshold).astype(int)

        auc = roc_auc_score(y_test, test_probs)
        acc = accuracy_score(y_test, test_preds)
        precision = precision_score(y_test, test_preds)
        recall = recall_score(y_test, test_preds)
        f1 = f1_score(y_test, test_preds)

        print(f"\n[Test Metrics]")
        print(f"AUC:       {auc:.3f}")
        print(f"Accuracy:  {acc:.3f}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall:    {recall:.3f}")
        print(f"F1 Score:  {f1:.3f}")

train_set = TrainSet()
split_data = train_set.split_model_data(val_prop=0.1, test_prop=0.2)
Model.xg_boost_model(split_data)