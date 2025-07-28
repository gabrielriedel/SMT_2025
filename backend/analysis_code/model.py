from train_set import *
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report

class model:

    def logistic_regression_model():
        split_data = train_set.split_model_data()
        model = LogisticRegression()
        model.fit(X_train, y_train)
        probs = model.predict_proba(X_test)[:, 1] 


    def random_forest_model():
        split_data = train_set.split_model_data()
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train, y_train)
        rf_probs = rf_model.predict_proba(X_test)[:, 1]
        rf_preds = (rf_probs >= 0.5).astype(int)

    def xg_boost_model():
        split_data = train_set.split_model_data()
        xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        xgb_model.fit(X_train, y_train)
        xgb_probs = xgb_model.predict_proba(X_test)[:, 1]
        xgb_preds = (xgb_probs >= 0.5).astype(int)
