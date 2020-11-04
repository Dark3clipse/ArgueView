from typing import Union, List, Optional
import pandas as pd
from openml import OpenMLDataset
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import scipy

from argueview.typings import OpenMLFeatureData


class Dataset:
    D: OpenMLDataset
    X: Union[np.ndarray, pd.DataFrame, scipy.sparse.csr_matrix]
    X_train: Union[np.ndarray, pd.DataFrame, scipy.sparse.csr_matrix]
    X_test: Union[np.ndarray, pd.DataFrame, scipy.sparse.csr_matrix]
    y: Optional[Union[np.ndarray, pd.DataFrame]]
    y_train: Optional[Union[np.ndarray, pd.DataFrame]]
    y_test: Optional[Union[np.ndarray, pd.DataFrame]]
    C: List[bool]
    F: List[str]
    y_labels: Union[None, List[str]]
    feature_data: Union[OpenMLFeatureData, None]

    def __init__(self,
                 D: OpenMLDataset,
                 X: Union[np.ndarray, pd.DataFrame, scipy.sparse.csr_matrix],
                 y: Optional[Union[np.ndarray, pd.DataFrame]],
                 C: List[bool],
                 F: List[str],
                 y_labels: Union[None, List[str]],
                 X_train: Union[np.ndarray, pd.DataFrame, scipy.sparse.csr_matrix],
                 y_train: Optional[Union[np.ndarray, pd.DataFrame]],
                 X_test: Union[np.ndarray, pd.DataFrame, scipy.sparse.csr_matrix],
                 y_test: Optional[Union[np.ndarray, pd.DataFrame]],
                 feature_data: Union[OpenMLFeatureData, None] = None):
        self.D = D
        self.C = C
        self.y_labels = y_labels
        self.F = F
        self.X = X
        self.y = y
        self.X_train = X_train
        self.X_test = X_test
        self.y_train = y_train
        self.y_test = y_test

        self.feature_data = feature_data

    def setModel(self, m, y_pred) -> None:
        self.m = m
        self.y_pred = y_pred

    def accuracy(self) -> float:
        return np.mean(self.y_pred == self.y_test)

    def printMetrics(self) -> None:
        print("Predictive accuracy: {:.2f}".format(np.mean(self.y_pred == self.y_test)))
        print("Classification report for classifier %s:\n%s\n"
              % (self.m, classification_report(self.y_test, self.y_pred)))
        print("Confusion matrix:\n%s" % confusion_matrix(self.y_test, self.y_pred))
