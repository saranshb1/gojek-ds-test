from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score, roc_auc_score, log_loss, precision_score, recall_score, f1_score


class Classifier(ABC):
    @abstractmethod
    def train(self, *params) -> None:
        pass

    @abstractmethod
    def evaluate(self, *params) -> Dict[str, float]:
        pass

    @abstractmethod
    def predict(self, *params) -> np.ndarray:
        pass


class SklearnClassifier(Classifier):
    def __init__(
        self, estimator: BaggingClassifier, features: List[str], target: str,
    ):
        self.clf = estimator
        self.features = features
        self.target = target

    def train(self, df_train: pd.DataFrame):
        self.clf.fit(df_train[self.features].values, df_train[self.target].values)

    def evaluate(self, df_test: pd.DataFrame):
        '''raise NotImplementedError(
            f"You're almost there! Identify an appropriate evaluation metric for your model and implement it here. "
            f"The expected output is a dictionary of the following schema: {{metric_name: metric_score}}"
        )'''
        
        """Evaluates the model performance using common classification metrics."""
        # Get predictions
        y_true = df_test[self.target].values
        y_pred_proba = self.clf.predict_proba(df_test[self.features].values)[:, 1]
        y_pred = (y_pred_proba >= 0.5).astype(int)  # Convert probabilities to class labels

        # Compute evaluation metrics
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "roc_auc": roc_auc_score(y_true, y_pred_proba),
            "log_loss": log_loss(y_true, y_pred_proba),
            "precision": precision_score(y_true, y_pred),
            "recall": recall_score(y_true, y_pred),
            "f1_score": f1_score(y_true, y_pred)
        }
        
        print(metrics)
        
        return metrics
        

    def predict(self, df: pd.DataFrame):
        return self.clf.predict_proba(df[self.features].values)[:, 1]
