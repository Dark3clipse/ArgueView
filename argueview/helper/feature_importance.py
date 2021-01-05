#!/bin/python
from typing import Dict, Tuple
from anchor.anchor_explanation import AnchorExplanation
from shap import Explanation
from argueview.typings import FeatureImportance, Case
import numpy as np


def feature_importance_from_lime(explanation: Dict[int, FeatureImportance], case: Case) -> Tuple[
    FeatureImportance, float]:
    # invert feature contributions when they are negatively framed w.r.t. decision-class
    for i in range(0, len(explanation[1])):
        v = list(explanation[1][i])
        # v[1] = -v[1]
        explanation[1][i] = tuple(v)

    # extract feature contribution map
    feature_importance = explanation[1]

    # compute unexplained
    change = sum(list(map(lambda x: x[1], explanation[1])))
    final = max(case.class_proba)
    unexplained = final - change

    return feature_importance, unexplained


def feature_importance_from_shap(shap_values: Explanation, case: Case) -> Tuple[FeatureImportance, float]:
    decision_class = np.argmax(case.class_proba)
    shap_values_for_class = shap_values[..., decision_class]

    # save as feature_importance map
    dat = iter(shap_values_for_class[case.id].values)
    fid = iter([i for i in range(len(shap_values_for_class[case.id].values))])
    feature_importance = list(zip(fid, dat))

    # unexplained importance
    unexplained = shap_values_for_class[case.id].base_values

    return feature_importance, unexplained


def feature_importance_from_anchor(explanation: AnchorExplanation, case: Case) -> Tuple[FeatureImportance, float]:
    """not implemented"""
    fi=[]
    return fi, 0
