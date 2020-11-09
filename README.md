# ArgueView

ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.

Example output:

![Example output](https://github.com/sophiahadash/argueview/blob/master/screenshots/scr1.png?raw=true)


The procedure for creating ArgueView explanations is as follows:
1. A traditional machine-learning context is created (i.e. data, model)
2. An explainer is employed to produce *feature importance*. This can be a white-box or black-box explainer. An example of a black-box explainer is [LIME](https://github.com/marcotcr/lime).
3. The machine-learning context and the *feature importance* are given to ArgueView such that it can produce a textual explanation.

![Procedure visualization](https://github.com/sophiahadash/argueview/blob/master/screenshots/model.png?raw=true)


### Running the examples

There are two examples available to help you learn how to use ArgueView. The 'plain' examples uses hypothetical data to show a minimalistic use-case. The CreditG example uses real data and a real ML model to illustrate a real-world use case.

If you would like to run the CreditG example the script needs to obtain the data. For this we use [OpenML](https://www.openml.org/). However, usage requires a valid API key and you will need to obtain one to run the example.

After you have obtained your key, create a `.env` file with your [OpenML](https://www.openml.org/) API key. 

```
echo "OML_APIKEY={my-key}" > .env
```
*Note: You can skip this step if you want to run the hypothetical example.*

Install all dependencies:

```
pipenv install --dev
```~~~~

Run an example:

```
/path/to/python3 ./examples/{example}/example.py
```

Additionally, there is a Jupyther Notebook available to directly see how ArgueView works. Check it out [here](https://github.com/SophiaHadash/ArgueView/blob/master/examples/creditg_lime/example.ipynb).

### Including in your project

To include this package in your project use your python dependency management tool to import this repo. Example using `pipenv`:

```
pipenv install -e git+https://github.com/SophiaHadash/ArgueView@{commit}
```
