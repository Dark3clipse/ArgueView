import json
import os
import lime
import lime.lime_tabular
import numpy as np
import openml as oml
import pandas as pd
import requests
from openml import OpenMLDataset
import settings
from typing import Dict
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import *
from sklearn.model_selection import *
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import *
from argueview.typings import Source, OpenMLFeatureData, Case, CaseSource, CaseFeature, FeatureImportance
from examples.Dataset import Dataset
from argueview import *
from argueview.helper import feature_importance_from_lime


# set OpenML API Key
oml.config.apikey = os.getenv('OML_APIKEY')


# example class that uses ArgueView
class ArgueViewExample:

    dataset: Dataset

    def openml_get_data_features(self, dataset_id: int) -> any:
        endpoint = "https://www.openml.org/api/v1/json/data/features/" + str(
            dataset_id) + "?api_key=" + oml.config.apikey
        headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
        r = requests.get(endpoint, headers=headers, verify=False)
        if r.status_code == 200:
            loads = json.loads(r.text)
            for f in loads['data_features']['feature']:
                f['index'] = int(f['index'])
                f['is_target'] = bool(f['is_target'])
                f['is_ignore'] = bool(f['is_ignore'])
                f['is_row_identifier'] = bool(f['is_row_identifier'])
                f['number_of_missing_values'] = int(f['number_of_missing_values'])
            return loads
        else:
            return ""

    def appendFeatureDescriptions(self):
        d = self.dataset.feature_data.feature
        d[0]["description"] = "Status of existing checking account, in Deutsche Mark."
        d[1]["description"] = "Duration in months"
        d[2]["description"] = "Credit history (credits taken, paid back duly, delays, critical accounts)"
        d[3]["description"] = "Purpose of the credit (car, television,...)"
        d[4]["description"] = "Credit amount"
        d[5]["description"] = "Status of savings account/bonds, in Deutsche Mark."
        d[6]["description"] = "Present employment, in number of years."
        d[7]["description"] = "Installment rate in percentage of disposable income"
        d[8]["description"] = "Personal status (married, single,...) and sex"
        d[9]["description"] = "Other debtors / guarantors"
        d[10]["description"] = "Present residence since X years"
        d[11]["description"] = "Property (e.g. real estate)"
        d[12]["description"] = "Age in years"
        d[13]["description"] = "Other installment plans (banks, stores)"
        d[14]["description"] = "Housing (rent, own,...)"
        d[15]["description"] = "Number of existing credits at this bank"
        d[16]["description"] = "Job"
        d[17]["description"] = "Number of people being liable to provide maintenance for"
        d[18]["description"] = "Telephone (yes,no)"
        d[19]["description"] = "Foreign worker (yes,no)"


    def load(self) -> None:

        # CreditG OpenML identifier
        dset = 31

        # Download credit-g data
        D: OpenMLDataset = oml.datasets.get_dataset(dset)

        # extract data
        X, y, C, F = D.get_data(target=D.default_target_attribute, dataset_format='array')
        y_labels = D.retrieve_class_labels()

        # separate into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=1/7)

        # load additional data on the features
        rt = self.openml_get_data_features(dset)
        dfeature = None
        if len(rt) > 0:
            dfeature = OpenMLFeatureData(rt['data_features'])

        # store data
        self.dataset = Dataset(D, X, y, C, F, y_labels, X_train, y_train, X_test, y_test, dfeature)

        # manually append feature descriptions (not available through openml api)
        self.appendFeatureDescriptions()


    def fit(self) -> None:

        # create pipeline
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, self.dataset.C)
            ]
        )
        rf = RandomForestClassifier(n_estimators=250, max_features=15, max_depth=10, max_leaf_nodes=16, n_jobs=-1)
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                             ('classifier', rf)])

        # fit pipeline
        pipe.fit(self.dataset.X_train, self.dataset.y_train)

        # store results
        y_pred = pipe.predict(self.dataset.X_test)
        self.dataset.setModel(pipe, y_pred)

        # print metrics
        self.dataset.printMetrics()


    def pickCase(self) -> int:
        return np.random.randint(0, self.dataset.y_test.shape[0])

    def printCase(self, dataset, case: int) -> None:
        print("case id: " + str(case))
        print("label:", self.dataset.y_labels[self.dataset.y_test[case]])
        print("prediction:", self.dataset.y_labels[self.dataset.y_pred[case]])
        print("features:")
        df = pd.DataFrame(data=self.dataset.X_test[case], index=self.dataset.F, columns=['values'])
        print(df)

    def explainer(self, case: int) -> Dict[int, FeatureImportance]:
        explainer = lime.lime_tabular.LimeTabularExplainer(self.dataset.X_train,
                                                           feature_names=self.dataset.F,
                                                           class_names=self.dataset.y_labels,
                                                           discretize_continuous=True)

        # generate explanation
        exp = explainer.explain_instance(self.dataset.X_test[case],
                                         self.dataset.m.predict_proba,
                                         num_features=len(self.dataset.F))

        # save
        exp.save_to_file("output/lime.html")

        # get feature importance
        return exp.as_map()

    def buildArgViewModel(self) -> ArgueView:

        # create argueview instance
        argView = ArgueView()

        # define decisions-classes
        argView.classes(["You are applicable for a loan.", "You are not applicable for a loan."])
        argView.latent_continuous_target("applicability", "inapplicability", [1, -1])

        # set a backing
        #argView.backing("Supported by Sophia Hadash, MSc from Jheronimus Academy of Data Science.")

        # add the data source
        argView.add_data_source(Source({
            "name": 'German Credit',
            "author": 'Dr. Hans Hofmann, Universität Hamburg, Institut für Statistik und Ökonometrie',
            "description": 'This dataset classifies people described by a set of attributes as good or bad credit risks.',
            "href": 'https://archive.ics.uci.edu/ml/datasets/statlog+(german+credit+data)',
            "observations": 1000,
            "type": 'static',
            "year": 1994,
            "features": self.dataset.feature_data.feature
        }))



        return argView

    def example(self):

        # step 1: load CreditG Data
        self.load()

        # step 2: fit a model on the data
        self.fit()

        # step 3: pick a case for explaining
        case_id = self.pickCase()
        case = Case({
            "id": case_id,
            "class_proba": self.dataset.m.predict_proba(self.dataset.X_test)[case_id].tolist(),
            "sources": [CaseSource({
                "features": list(map(lambda x: CaseFeature({"value": x}), self.dataset.X_test[case_id].tolist()))
            })]
        })
        print('case: '+str(case_id))

        # step 4: use an explainer to generate feature importance for each source (in our example we have one source)
        fmap = self.explainer(case_id)
        feature_importance, unexplained = feature_importance_from_lime(fmap, case)

        # step 5: build argumentation model
        argView = self.buildArgViewModel()

        # step 6: generate explanation
        explanation = argView.generate(case, feature_importance, unexplained)

        # print and export
        explanation.print()
        explanation.save('output/explanation.json')

    def __init__(self):
        self.example()

if __name__ == "__main__":
    app = ArgueViewExample()
