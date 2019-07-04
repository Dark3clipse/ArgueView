import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import FeatureUnion, Pipeline


# Custom Transformer that extracts columns passed as argument to its constructor
class IsMultiplierTransformer(BaseEstimator, TransformerMixin):

    def __init__(self):
        self.categories_ = None

    def fit(self, X, y=None):
        return self

        # Method that describes what we need this transformer to do

    def transform(self, X, y=None):
        s = X.shape[1]
        n = int(5*((s-1)*s - s*(s-1)/2))
        Xout = np.empty([X.shape[0], n])
        self.categories_ = np.empty(n, dtype="S14")

        for i in range(0, X.shape[0]):
            c = 0
            for j in range(0, X.shape[1]-1):
                for k in range(j+1, X.shape[1]):
                    for m in [2, 3]:
                        Xout[i, c] = (m*X[i,j] == X[i,k])
                        self.categories_[c] = 'N'+str(j)+' == 1/'+ str(m)+'*N'+str(k)
                        c += 1
                    for m in [1, 2, 3]:
                        Xout[i, c] = (X[i,j] == m*X[i,k])
                        self.categories_[c] = 'N'+str(j)+' == '+ str(m)+'*N'+str(k)
                        c += 1
        return Xout
