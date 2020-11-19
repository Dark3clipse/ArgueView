from random import random
from IPython.core.display import display, Javascript, HTML
from argueview.typings import Explanation
from argueview.visualizers import initjs, html_err_msg


def ToulminVisualizer(explanation: Explanation) -> None:
    next(initjs())
    eid = "vis-" + str(random())
    display(HTML("<div id='{id}'>{err_msg}</div>".format(id=eid, err_msg=html_err_msg())))
    display(Javascript("""
    if (window.argueview) {{
        window.ReactDom.render(
            window.React.createElement(window.argueview.ToulminVisualizer, {{explanation: {data}}}),
            document.getElementById('{id}')
        );
    }}
    """.format(id=eid, data=explanation.serialize())))
