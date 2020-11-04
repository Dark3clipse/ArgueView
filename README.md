# ArgueView

ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.

Example:

![Example output](https://github.com/sophiahadash/argueview/blob/master/screenshots/scr1.png?raw=true)


The procedure for creating ArgueView explanations is as follows:
1. A traditional machine-learning context is created (i.e. data, model)
2. An explainer is employed to produce *feature importance*. This can be a white-box or black-box explainer. An example of a black-box explainer is [LIME](https://github.com/marcotcr/lime).
3. The machine-learning context and the *feature importance* are given to ArgueView such that it can produce a textual explanation.

![Procedure visualization](https://github.com/sophiahadash/argueview/blob/master/screenshots/model.png?raw=true)

### Including in your project

To include this package in your project use your python dependency management tool to import this repo. Example using `pipenv`:

```
pipenv install -e git+https://github.com/SophiaHadash/ArgueView@{commit}
```


### Running the example

Create a `.env` file with your OpenML API key:

```
echo "OML_APIKEY={my-key}" > .env
```

Install all dependencies

```
pipenv install --dev
```

Run the example

```
/path/to/python3 ./examples/example.py
```
