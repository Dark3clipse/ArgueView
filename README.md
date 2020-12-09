
<p align="center">
  <img href="https://github.com/SophiaHadash/ArgueView" alt="ArgueView" src="https://raw.githubusercontent.com/SophiaHadash/ArgueView/master/screenshots/logo.svg" width="50%" />
<p>

--- 
[![Build Status](https://jenkins.tuneblendr.com/job/ArgueView/job/master/badge/icon?style=flat&link=https%3A%2F%2Fjenkins.tuneblendr.com%2Fblue%2Forganizations%2Fjenkins%2FTuneblendr%2Factivity "Build Status")](https://jenkins.tuneblendr.com/blue/organizations/jenkins/ArgueView/activity)

ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.

Example output using the visualizer:

![Example Visualization](https://github.com/sophiahadash/argueview/blob/master/screenshots/toulmin-visualizer.png?raw=true)
![Example output](https://github.com/sophiahadash/argueview/blob/master/screenshots/featurelist-visualizer.png?raw=true)


The procedure for creating ArgueView explanations is as follows:
1. A traditional machine-learning context is created (i.e. data, model)
2. An explainer is employed to produce *feature importance*. This can be a white-box or black-box explainer. An example of a black-box explainer is [LIME](https://github.com/marcotcr/lime).
3. The machine-learning context and the *feature importance* are given to ArgueView such that it can produce a textual explanation.

![Procedure visualization](https://github.com/sophiahadash/argueview/blob/master/screenshots/model.png?raw=true)

## Installation

ArgueView is available as a python package on [PyPi](https://pypi.org/project/argueview/). You can install it using `pip`:

```
pip install argueview
```

Or, using `pipenv`:

```
pipenv install argueview
```

## Usage

Usage is documented in our examples. Examples are available in python and jupyter notebooks. The following examples are available:

- minimal, hypothetical data and explainer: [python](https://github.com/SophiaHadash/ArgueView/blob/master/examples/fruit_plain/example.py)
- creditg data with [LIME](https://github.com/marcotcr/lime) explainer: [python](https://github.com/SophiaHadash/ArgueView/blob/master/examples/creditg_lime/example.py), [notebook](https://github.com/SophiaHadash/ArgueView/blob/master/examples/creditg_lime/example.ipynb)
- creditg data with [shap](https://github.com/slundberg/shap) explainer: [python](https://github.com/SophiaHadash/ArgueView/blob/master/examples/creditg_shap/example.py), [notebook](https://github.com/SophiaHadash/ArgueView/blob/master/examples/creditg_shap/example.ipynb)

## Running the examples

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
```

Run an example:

```
/path/to/python3 ./examples/{example}/example.py
```

Additionally, there is are Jupyther Notebooks available to directly see how ArgueView works.

## Building

Follow these steps to build ArgueView from source.

- make sure you install the dependencies. ArgueView requires the following dependencies: `python>=3.5`, `pip3`, `pipenv`, `git`.
- build using make
    ``` 
    make
    ```

### Using Docker

Alternatively you can build ArgueView using docker.

- build context dockerfile
    ```
    docker build -t argueview/context:local .
    ```
- run `build.sh` in a container
    ```
    CID=$(docker run 
        -v /var/run/docker.sock:/var/run/docker.sock
        argueview/context
        build.sh)
    ```
- copy results from the container
    ```
    docker cp ${CID}:/argueview/argueview.egg-info ./argueview.egg-info
    docker cp ${CID}:/argueview/build ./build
    docker cp ${CID}:/argueview/dist ./dist
    ```
