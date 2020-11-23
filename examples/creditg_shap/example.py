import json
import os
import numpy as np
import openml as oml
import pandas as pd
import requests
from openml import OpenMLDataset
import shap
from shap import Explanation

import settings
from typing import List, Tuple
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import *
from sklearn.model_selection import *
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import *

from argueview.helper import feature_importance_from_shap
from argueview.typings import Source, OpenMLFeatureData, Case, CaseSource, CaseFeature
from examples.Dataset import Dataset
from argueview import *



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

    def explainer(self) -> Explanation:

        def custom_masker(mask, x):
            return (x * mask).reshape(1, len(x))

        explainer = shap.explainers.Permutation(self.dataset.m.predict_proba, custom_masker)
        explainer.feature_names = self.dataset.F
        explainer.output_names = self.dataset.y_labels

        shap_values = explainer(self.dataset.X)

        return shap_values

    def buildArgViewModel(self) -> ArgueView:

        # create argueview instance
        argView = ArgueView()

        # define decisions-classes
        argView.classes(["You are applicable for a loan.", "You are not applicable for a loan."])
        argView.latent_continuous_target("applicability", "inapplicability", [1, -1])

        # set a backing
        argView.backing("Supported by Sophia Hadash, MSc from Jheronimus Academy of Data Science.")

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

        argView.grounds([
            ["You have a sufficient amount on your checking account.",
             "You have an insufficient amount on your checking account."],
            ["We believe the duration of the credit is appropriate.",
             "We believe the duration of the credit is not appropriate."],
            ["Your credit history gives us confidence in your capabilities.",
             "Your credit history does not give us confidence in your capabilities."],
            ["We are interested in providing loans for <>.",
             "We are generally not interested in providing loans for <>."],
            ["Your credit amount gives us confidence in your capabilities.",
             "Your credit amount does not give us sufficient confidence in your capabilities."],
            ["Your savings give us confidence in your capabilities.",
             "Your savings do not give us confidence in your capabilities."],
            ["The duration of your current employment gives us confidence in your capabilities.",
             "The duration of your current employment does not give us confidence in your capabilities."],
            ["With the requested loan included, your installment rate is below the threshold.",
             "The requested loan would increase your EMI over the threshold."],
            ["We have more confidence in providing loans to <> in general.",
             "We have less confidence in providing loans to <> in general."],
            ["<> gives us confidence in your capabilities.",
             "<> does not give us sufficient confidence in your capabilities."],
            ["The duration of your current residence gives us confidence in your capabilities.",
             "The duration of your current residence does not give us confidence in your capabilities."],
            ["<> gives us confidence in your capabilities.", "<> does not give us confidence in your capabilities."],
            ["Your age gives us confidence in your capabilities.",
             " Your age does not give us confidence in your capabilities."],
            ["<> gives us confidence in your capabilities.", "<> does not give us confidence in your capabilities."],
            ["Living in <> increases the confidence we have in your capabilities.",
             "Living in <> decreases the confidence we have in your capabilities."],
            ["The amount of your credits gives us confidence in your capabilities.",
             "The amount of your credits does not give us confidence in your capabilities."],
            ["Your current employment responsibilities supports our confidence in your capabilities.",
             "Your current employment responsibilities give us less confidence in your capabilities."],
            ["The number of people that are liable to provide maintenance for gives us confidence in your capabilities.",
            "The number of people that are liable to provide maintenance for does not give us confidence in your capabilities."],
            ["The <> telephone gives us confidence in your capabilities.",
             "The <> telephone does not give us confidence in your capabilities."],
            ["Because you are <>a foreign worker, we have more confidence in your capabilities.",
             "Because you are <>a foreign worker, we have less confidence in your capabilities."],
        ], [
            [],
            [],
            [],
            ["the purpose of buying a new car", "the purpose of buying a used car",
             "the purpose of buying furniture or equipment", "the purpose of buying a radio or tv",
             "the purpose of buying domestic appliance", "the purpose of making repairs",
             "the purpose of gaining education", "the purpose of paying for vacation", "the purpose of retraining",
             "the purpose of investing in business", "unspecified purposes"],
            [],
            [],
            [],
            [],
            ["divorced or separated males", "females", "single males", "married or widowed males", "single females"],
            ["The lack of a co-applicant or guarantor", "Your co-applicant", "Your guarantor"],
            [],
            ["Your real-estate", "Your life insurance", "The fact that you own a car", "The absence of known property"],
            [],
            ["Your installment plan at a bank", "Your installment plan at a store",
             "Having no other installment plans"],
            ["rented housing", "owned housing", "free housing"],
            [],
            [],
            [],
            ["lack of ownership of a", "ownership of a"],
            ["", "not "],
        ])

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
        shap_values = self.explainer()
        feature_importance, unexplained = feature_importance_from_shap(shap_values, case)

        # step 5: build argumentation model
        argView = self.buildArgViewModel()

        # step 6: generate explanation
        explanation = argView.generate(case, feature_importance, unexplained)

        # print
        explanation.print()

    def __init__(self):
        self.example()

if __name__ == "__main__":
    app = ArgueViewExample()
