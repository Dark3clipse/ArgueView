from random import random
from IPython.core.display import display, Javascript, HTML
from argueview.typings import Explanation, LatentContinuousTargetDisplay, Framing
from argueview.visualizers import initjs, html_err_msg


def FeatureListVisualizer(explanation: Explanation, framing: Framing = "positive", lct: LatentContinuousTargetDisplay = "positive") -> None:
    next(initjs())
    eid = "vis-" + str(random())
    display(HTML("<div id='{id}'>{err_msg}</div>".format(id=eid, err_msg=html_err_msg())))
    display(Javascript("""
    if (window.argueview) {{
        window.ReactDom.render(
            window.React.createElement(window.argueview.FeatureListVisualizer, {{explanation: {data}, framing: {framing}, lct: {lct}}}),
            document.getElementById('{id}')
        );
    }}
    """.format(id=eid, data=explanation.serialize(), framing=framing, lct=lct)))
