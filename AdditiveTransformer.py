import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline


# Custom Transformer that extracts columns passed as argument to its constructor
class AdditiveTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.categories_ = None

    def fit(self, X, y=None):
        return self

        # Method that describes what we need this transformer to do

    def transform(self, X, y=None):
        n = (X.shape[1] - 1)
        Xout = np.empty([X.shape[0], n])
        self.categories_ = np.empty(n, dtype="S14")
        for i in range(0, X.shape[0]):
            for j in range(0, X.shape[1]-1):
                Xout[i,j] = X[i,j+1] - X[i,j]
                self.categories_[j] = 'N'+str(j+1)+' - N'+str(j)
        return Xout
