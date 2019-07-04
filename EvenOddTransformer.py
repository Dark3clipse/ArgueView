import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline


# Custom Transformer that extracts columns passed as argument to its constructor
class EvenOddTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.categories_ = None

    def fit(self, X, y=None):
        return self

        # Method that describes what we need this transformer to do

    def transform(self, X, y=None):
        for i in range(0, X.shape[0]):
            for j in range(0, X.shape[1]):
                X[i, j] = X[i, j] % 2

        self.categories_ = np.empty(X.shape[1], dtype="S10")
        for j in range(0, X.shape[1]):
            self.categories_[j] = 'f' + str(j) + ' = odd'

        return X