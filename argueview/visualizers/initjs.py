import os
import io
try:
    from IPython.core.display import display, HTML, Javascript
    from IPython import get_ipython
    have_ipython = True
except ImportError:
    have_ipython = False


def html_err_msg() -> str:
    return """
    <div style='color: #900; text-align: left;'>
      <b>Visualization omitted, Javascript library not loaded!</b><br>
      If this notebook was from another user you must trust this notebook (File -> Trust notebook). 
      If you are viewing this notebook on github the Javascript has been stripped for security. If you are using
      JupyterLab this error is because a JupyterLab extension has not yet been written.
    </div>"""


def _ipython_err_msg() -> str:
    return "IPython must be installed to use initjs()! Run `pip install ipython` and then restart argueview."


def initjs() -> None:
    assert have_ipython, _ipython_err_msg()
    bundle_path = os.path.join(os.path.split(__file__)[0], "resources", "bundle.min.js")
    with io.open(bundle_path, encoding="utf-8") as f:
        bundle_data = f.read()
    display(Javascript("{bundle_data}".format(bundle_data=bundle_data)))
    while True:
        yield
