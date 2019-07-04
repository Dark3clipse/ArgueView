from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from Dataset import *
from IsMultiplierTransformer import *
from AdditiveTransformer import *
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import *
from sklearn.tree import DecisionTreeClassifier
from EvenOddTransformer import *
from sklearn import tree
from subprocess import check_call
import pandas as pd


class WasonTask:

    def __init__(self):
        self.dataset = None

    def generate(self) -> None:
        X = np.empty((1000, 3))
        X2 = np.empty((1000, 4))
        y = np.empty(1000)
        c = 0
        for i in range(0, 10):
            for j in range(0, 10):
                for k in range(0, 10):
                    X[c, :] = np.array([i, j, k])
                    #y[c] = (j == 2*i and k == 2*j) # sequence of x2
                    #y[c] = (j == 2 * i and k == 2 * j) or (j == 3 * i and k == 3 * j) or (i == 2 * j and j == 2 * k) or (i == 3 * j and j == 3 * k) # sequence of x any
                    #y[c] = (j == i + 1 and k == j - 2) # additive sequence
                    y[c] = ((i%2 + j%2 + k%2) != 1) # not one odd
                    X2[c, :] = np.array([i, j, k, y[c]])
                    if (y[c] == 1):
                        print(X[c, :])

                    c += 1
        C = np.array([0, 0, 0])
        F = ['a1', 'a2', 'a3']
        y_labels = ['false', 'true']

        pd.DataFrame(
            data=X2,
            columns=['N1', 'N2', 'N3', 'match']
        ).to_csv('output/data.csv', index=False)

        # separate into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=3452, test_size=1 / 7)

        # load additional data on the features
        dfeature = ['first number', 'second number', 'third number'];

        # store data
        self.dataset = Dataset(None, X, y, C, F, y_labels, X_train, y_train, X_test, y_test, dfeature)

    def model(self) -> None:

        # create pipeline
        preprocessor = Pipeline(steps=[
                ('onehot', EvenOddTransformer()),
                ('interactions', PolynomialFeatures(degree=2, interaction_only=True))
            ]
        )

        rf = DecisionTreeClassifier()
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', rf)])

        # fit pipeline
        pipe.fit(self.dataset.X_train, self.dataset.y_train)
        print(pipe.named_steps.preprocessor.named_steps.onehot.categories_)
        print(pipe.named_steps.preprocessor.named_steps.interactions.powers_)
        #print(pipe.named_steps.classifier.coef_)
        tree.export_graphviz(pipe.named_steps.classifier, 'output/tree.dot', class_names=self.dataset.y_labels)

        # store results
        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)

    def model_multiply(self) -> None:

        # create pipeline
        preprocessor = Pipeline(steps=[
                ('onehot', IsMultiplierTransformer()),
                #('interactions', PolynomialFeatures(degree=2, interaction_only=True))
            ]
        )

        rf = LogisticRegression()
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', rf)])

        # fit pipeline
        pipe.fit(self.dataset.X_train, self.dataset.y_train)

        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)
        self.dataset.printMetrics()

        print(pd.DataFrame(
            data=pipe.named_steps.classifier.coef_[0,:],
            index=pipe.named_steps.preprocessor.named_steps.onehot.categories_,
            columns=['coefficient']
        ))

        # also fit decision tree
        rf = DecisionTreeClassifier()
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', rf)])
        pipe.fit(self.dataset.X_train, self.dataset.y_train)
        tree.export_graphviz(pipe.named_steps.classifier, 'output/tree.dot', class_names=self.dataset.y_labels)


        # store results
        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)

    def model_additive(self) -> None:



        # create pipeline
        preprocessor = Pipeline(steps=[
            ('onehot', AdditiveTransformer()),
            ('onehot2', OneHotEncoder(categories='auto')),
            # ('interactions', PolynomialFeatures(degree=2, interaction_only=True))
        ])

        rf = LogisticRegression()
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', rf)])

        # fit pipeline
        pipe.fit(self.dataset.X_train, self.dataset.y_train)

        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)
        self.dataset.printMetrics()

        print(pipe.named_steps.preprocessor.named_steps.onehot.categories_)
        print(pipe.named_steps.preprocessor.named_steps.onehot2.categories_)

        categories_ = np.empty(len(pipe.named_steps.preprocessor.named_steps.onehot.categories_) * len(pipe.named_steps.preprocessor.named_steps.onehot2.categories_[0]), dtype="S15")
        c = 0
        for i in range(0, len(pipe.named_steps.preprocessor.named_steps.onehot.categories_)):
            for j in range(0, len(pipe.named_steps.preprocessor.named_steps.onehot2.categories_[0])):
                categories_[c] = str(pipe.named_steps.preprocessor.named_steps.onehot.categories_[i]) + ' = ' + str(pipe.named_steps.preprocessor.named_steps.onehot2.categories_[0][j])
                categories_[c] = categories_[c].decode('UTF-8').replace("b\"b\'", "")
                c += 1

        print(pd.DataFrame(
            data=pipe.named_steps.classifier.coef_[0, :],
            index=categories_,
            columns=['coefficient']
        ))

        # also fit decision tree
        rf = DecisionTreeClassifier()
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', rf)])
        pipe.fit(self.dataset.X_train, self.dataset.y_train)
        tree.export_graphviz(pipe.named_steps.classifier, 'output/tree.dot', class_names=self.dataset.y_labels, feature_names=categories_)

        # store results
        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)

    def model_numbers(self) -> None:
        # create pipeline
        preprocessor = Pipeline(steps=[
            ('onehot', OneHotEncoder())
        ])

        rf = LogisticRegression()
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                               ('classifier', rf)])

        # fit pipeline
        pipe.fit(self.dataset.X_train, self.dataset.y_train)
        print(pipe.named_steps.preprocessor.named_steps.onehot.categories_)
        print(pipe.named_steps.classifier.coef_)
        #tree.export_graphviz(pipe.named_steps.classifier, 'output/tree.dot', class_names=self.dataset.y_labels)

        # store results
        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)

    def get_dataset(self) -> Dataset:
        return self.dataset
