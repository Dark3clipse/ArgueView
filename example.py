from preamble import *
from argueview import *
from sklearn.model_selection import *
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import *
from sklearn.ensemble import *
from sklearn.metrics import *
import pandas as pd
import lime
import lime.lime_tabular
from typing import List
from typing import Tuple

from os import sys
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#from sklearn.neighbors import KNeighborsClassifier
#from sklearn.linear_model import LogisticRegression
#from sklearn.svm import *
#import imageio


#import LORE.lore as lore


class ArgueViewExample:

    #inner classes
    class Dataset:
        def __init__(self, D, X, y, C, F, y_labels, X_train, y_train, X_test, y_test):
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

        def setModel(self, m, y_pred) -> None:
            self.m = m
            self.y_pred = y_pred

        def printMetrics(self) -> None:
            print("Predictive accuracy: {:.2f}".format(np.mean(self.y_pred == self.y_test)))
            print("Classification report for classifier %s:\n%s\n"
                  % (self.m, classification_report(self.y_test, self.y_pred)))
            print("Confusion matrix:\n%s" % confusion_matrix(self.y_test, self.y_pred))

    # properties
    datasets: List[Dataset] = []



    def config(self) -> None:
        oml.config.apikey = '11e82c8d91c5abece86f424369c71590'
        plt.rcParams['savefig.dpi'] = 100

    def loadData(self) -> None:

        # load data
        D = oml.datasets.get_dataset(31)  # Download credit-g data

        # extract data
        X, y, C, F = D.get_data(target=D.default_target_attribute, return_attribute_names=True, return_categorical_indicator=True)
        y_labels = D.retrieve_class_labels()  # ['good', 'bad']

        # separate into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=1/7)

        # store data
        self.datasets.append(self.Dataset(D, X, y, C, F, y_labels, X_train, y_train, X_test, y_test))

    def plotDataClasses(self, dataset: int, fname: str) -> None:
        unique, counts = np.unique(self.datasets[dataset].y_test, return_counts=True)
        plt.bar(unique, counts, width=0.8, bottom=None, align='center', data=None)
        plt.savefig("output/"+fname)

    def createPipelineGridSearch(self, dataset: int, param_grid) -> Pipeline:
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, self.datasets[dataset].C)
            ]
        )
        rf = RandomForestClassifier(n_estimators=250)

        return Pipeline(steps=[('preprocessor', preprocessor),
                             ('classifier', GridSearchCV(rf, param_grid, n_jobs=-1))])

    def exploreParams(self, dataset: int, fname: str):

        # create pipeline
        param_grid = {'max_depth': [2, 4, 6, 8, 10],
                      'max_features': [5, 10, 15, 20, 25],
                      'max_leaf_nodes': [5, 8, 10, 12, 15]
                      }
        pipe = self.createPipelineGridSearch(dataset, param_grid)

        # fit pipeline
        pipe.fit(self.datasets[dataset].X_train, self.datasets[dataset].y_train)

        # store results
        y_pred = pipe.predict(self.datasets[dataset].X_test)
        self.datasets[dataset].setModel(pipe, y_pred)

        # print metrics
        self.datasets[dataset].printMetrics()

        # create heatmap
        grid_search = pipe.named_steps['classifier']
        results = pd.DataFrame(grid_search.cv_results_)
        scoresf = np.array(results.mean_test_score).reshape(5, 5, 5)

        i = 1
        scores = scoresf[:, i, :]
        print("heat map for max features = ", param_grid['max_features'][i])
        mglearn.tools.heatmap(scores, xlabel='max_depth', xticklabels=param_grid['max_depth'],
                              ylabel='max_leaf_nodes', yticklabels=param_grid['max_leaf_nodes'], cmap="viridis",
                              fmt="%.2f")
        plt.savefig("output/" + fname)

    def fitModel(self, dataset: int) -> None:

        # create pipeline
        categorical_transformer = Pipeline(steps=[
            ('onehot', OneHotEncoder(handle_unknown='ignore'))
        ])
        preprocessor = ColumnTransformer(
            transformers=[
                ('cat', categorical_transformer, self.datasets[dataset].C)
            ]
        )
        rf = RandomForestClassifier(n_estimators=250, max_features=15, max_depth=10, max_leaf_nodes=16, n_jobs=-1)
        pipe = Pipeline(steps=[('preprocessor', preprocessor),
                             ('classifier', rf)])

        # fit pipeline
        pipe.fit(self.datasets[dataset].X_train, self.datasets[dataset].y_train)

        # store results
        y_pred = pipe.predict(self.datasets[dataset].X_test)
        self.datasets[dataset].setModel(pipe, y_pred)

        # print metrics
        self.datasets[dataset].printMetrics()

    def mlmodel(self) -> None:
        # load credit-g data
        self.loadData()

        # plot the class distribution
        self.plotDataClasses(0, "creditg_classes.png")

        # explore params
        # self.exploreParams(0, "gridsearch.png")

        # fit model
        self.fitModel(0)

    def pickCase(self, dataset: int) -> int:
        return 131 #np.random.randint(0, self.datasets[dataset].y_test.shape[0])

    def printCase(self, dataset, case: int) -> None:
        print("case id: " + str(case))
        print("label:", self.datasets[dataset].y_labels[self.datasets[dataset].y_test[case]])
        print("prediction:", self.datasets[dataset].y_labels[self.datasets[dataset].y_pred[case]])
        print("features:")
        df = pd.DataFrame(data=self.datasets[dataset].X_test[case], index=self.datasets[dataset].F, columns=['values'])
        print(df)

    def exploreCase(self, dataset: int, case: int) -> List[Tuple[int, int]]:
        explainer = lime.lime_tabular.LimeTabularExplainer(self.datasets[dataset].X_train, feature_names=self.datasets[dataset].F, class_names=self.datasets[dataset].y_labels, discretize_continuous=True)

        # generate explanation
        exp = explainer.explain_instance(self.datasets[dataset].X_test[case], self.datasets[dataset].m.predict_proba, num_features=10)

        # save
        exp.save_to_file("output/lime_dat"+str(dataset)+"_case"+str(case)+".html")

        return exp.as_map()

    def __init__(self):

        # configuration
        self.config()
        dataset = 0

        # step 1: get a machine learning model
        self.mlmodel()

        # step 2: pick an interesting case
        case = self.pickCase(dataset)
        # case = 53 # or use a fixed case

        # print the case
        self.printCase(dataset, case)

        # step 3: explore model local to the case
        exp = self.exploreCase(dataset, case)

        # step 4: build argumentation model
        argView = ArgueView(decision=self.datasets[dataset].y_pred[case], classes=self.datasets[dataset].y_labels, features=self.datasets[dataset].X_test[case], explanation_map=exp)
        argView.grounds([
            ("You have a sufficient amount on your checking account.", "You have an insufficient amount on your checking account."),
            ("We believe the duration of the credit is appropriate.", "We believe the duration of the credit is not appropriate."),
            ("Your credit history gives us confidence in your capabilities.", "Your credit history does not give us confidence in your capabilities."),
            ("We are interested in providing loans for <>.", "We are generally not interested in providing loans for <>."),
            ("Your credit amount gives us confidence in your capabilities.", "Your credit amount does not give us sufficient confidence in your capabilities."),
            ("Your savings gives us confidence in your capabilities.", "Your savings do not give us confidence in your capabilities."),
            ("The duration of your current employment gives us confidence in your capabilities.", "The duration of your current employment does not give us confidence in your capabilities."),
            ("With the requested loan included, your installment rate is below the threshold.", "The requested loan would increase your EMI over the threshold."),
            ("We have more confidence in providing loans to <> in general.", "We have less confidence in providing loans to <> in general."),
            ("<> gives us confidence in your capabilities.", "<> does not give us sufficient confidence in your capabilities."),
            ("The duration of your current residence gives us confidence in your capabilities.", "The duration of your current residence does not give us confidence in your capabilities."),
            ("<> gives us confidence in your capabilities.", "<> does not give us confidence in your capabilities."),
            ("Your age gives us confidence in your capabilities.", " Your age does not give us confidence in your capabilities."),
            ("<> gives us confidence in your capabilities.", "<> does not give us confidence in your capabilities."),
            ("Living in <> increases the confidence we have in your capabilities.", "Living in <> decreases the confidence we have in your capabilities."),
            ("The amount of your credits gives us confidence in your capabilities.", "The amount of your credits does not give us confidence in your capabilities."),
            ("Your current employment responsibilities supports our confidence in your capabilities.", "Your current employment responsibilities give us less confidence in your capabilities."),
            ("The number of people that are liable to provide maintenance for gives us confidence in your capabilities.", "The number of people that are liable to provide maintenance for does not give us confidence in your capabilities."),
            ("The <> telephone gives us confidence in your capabilities.", "The <> telephone does not give us confidence in your capabilities."),
            ("Because you are <>a foreign worker, we have more confidence in your capabilities.", "Because you are <>a foreign worker, we have less confidence in your capabilities."),
        ], [
            [],
            [],
            [],
            ["the purpose of buying a new car", "the purpose of buying a used car", "the purpose of buying furniture or equipment", "the purpose of buying a radio or tv", "the purpose of buying domestic appliance", "the purpose of making repairs", "the purpose of gaining education", "the purpose of paying for vacation", "the purpose of retraining", "the purpose of investing in business", "unspecified purposes"],
            [],
            [],
            [],
            [],
            ["divorced or separated males", "females", "single males", "married or widowed males", "single females"],
            ["The lack of a co-applicant or guarantor", "Your co-applicant", "Your guarantor"],
            [],
            ["Your real-estate", "Your life insurance", "The fact that you own a car", "The absence of known property"],
            [],
            ["Your installment plan at a bank", "Your installment plan at a store", "Having no other installment plans"],
            ["rented housing", "owned housing", "free housing"],
            [],
            [],
            [],
            ["lack of ownership of a", "ownership of a"],
            ["", "not "],
        ])

        argView.printExplanationGrounds()

def syntax_file(text):
    """Detects syntax in the file located in Google Cloud Storage."""
    client = language.LanguageServiceClient()

    # Instantiates a plain text document.
    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects syntax in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    tokens = client.analyze_syntax(document).tokens

    # part-of-speech tags from enums.PartOfSpeech.Tag
    pos_tag = ('UNKNOWN', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM',
               'PRON', 'PRT', 'PUNCT', 'VERB', 'X', 'AFFIX')

    for token in tokens:
        print(u'{}: {}'.format(pos_tag[token.part_of_speech.tag],
                               token.text.content))

def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)

    for entity in result.entities:
        print('Mentions: ')
        print(u'Name: "{}"'.format(entity.name))
        for mention in entity.mentions:
            print(u'  Begin Offset : {}'.format(mention.text.begin_offset))
            print(u'  Content : {}'.format(mention.text.content))
            print(u'  Magnitude : {}'.format(mention.sentiment.magnitude))
            print(u'  Sentiment : {}'.format(mention.sentiment.score))
            print(u'  Type : {}'.format(mention.type))
        print(u'Salience: {}'.format(entity.salience))
        print(u'Sentiment: {}\n'.format(entity.sentiment))

if __name__ == "__main__":
    #syntax_file("The lack of ownership of a telephone does not give us confidence in your capabilities.")
    app = ArgueViewExample()