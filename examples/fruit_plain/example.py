from argueview import ArgueView
from argueview.typings import Source, Feature, Case, CaseSource, CaseFeature, FeatureImportance

# create argueview instance
argView = ArgueView()

# define decisions-classes
argView.classes(['pear', 'orange'])

# set a backing
argView.backing('Supported by Sophia Hadash, MSc from Jheronimus Academy of Data Science.')

# add a data source
argView.add_data_source(Source({
    "name": 'Apples and Oranges Dataset',
    "author": 'S. Hadash',
    "description": 'Dataset of apples and oranges.',
    "href": '',
    "observations": 1000,
    "type": 'static',
    "year": 2020,
    "features": [Feature({
        "data_type": 'nominal',
        "description": 'shape',
        "index": 0,
        "is_ignore": False,
        "is_row_identifier": False,
        "is_target": False,
        "name": 'shape',
        "nominal_value": ['spherical', 'non-spherical'],
        "number_of_missing_values": 0
    }), Feature({
        "data_type": 'nominal',
        "description": 'color',
        "index": 1,
        "is_ignore": False,
        "is_row_identifier": False,
        "is_target": False,
        "name": 'color',
        "nominal_value": ['red', 'green', 'yellow', 'orange'],
        "number_of_missing_values": 0
    })]
}))

# define argumentation grounds
argView.grounds([['Shape is less spherical', 'Shape is more spherical'],
                ["The color '<>' provides evidence for class pear", "The color '<>' provides evidence for class orange"]],
                [[],
                ['red', 'green', 'yellow', 'orange']])

# define a hypothetical case
case = Case({
    "id": 0,
    "class_proba": [.05, .95],
    "sources": [CaseSource({
        "features": [CaseFeature({
            "value": 0
        }), CaseFeature({
            "value": 3
        })]
    })]
})

# define some hypothetical feature-importance mapping
feature_importance = FeatureImportance([(0, .1), (1, .7)])

# unexplained contribution
unexplained = .15 # = class probability - sum(feature_importance_contributions) = .95 - .7 - .1

# generate explanation
explanation = argView.generate(case, feature_importance, unexplained)

# print
explanation.print()
