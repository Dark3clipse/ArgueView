from random import random
from IPython.core.display import display, Javascript, HTML
from argueview.typings import Explanation, LatentContinuousTargetDisplay, Framing
from argueview.visualizers import initjs, html_err_msg


def FeatureListVisualizer(explanation: Explanation, framing: Framing = "positive", lct: LatentContinuousTargetDisplay = "label", threshold: float = -1, threshold_badge: float = 0, threshold_omit: float = -1) -> None:
    next(initjs())
    eid = "vis-" + str(random())
    display(HTML("<div id='{id}'>{err_msg}</div>".format(id=eid, err_msg=html_err_msg())))
    display(Javascript("""
    if (window.argueview) {{
        window.ReactDom.render(
            window.React.createElement(window.argueview.FeatureListVisualizer, {{explanation: {data}, framing: "{f}", lct: "{l}", threshold: {t}, thresholdBadge: {t2}, thresholdOmit: {t3}}}),
            document.getElementById('{id}')
        );
    }}
    """.format(id=eid, data=explanation.serialize(), f=framing, l=lct, t=threshold, t2=threshold_badge, t3=threshold_omit)))
