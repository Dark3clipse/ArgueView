from sklearn.metrics import *
import numpy as np


class Dataset:
    def __init__(self, D, X, y, C, F, y_labels, X_train, y_train, X_test, y_test, FeatureData = None):
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

        self.FeatureData = FeatureData

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