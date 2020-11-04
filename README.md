# ArgueView

ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.

Example presentation:
[Example output](https://github.com/sophiahadash/argueview/blob/master/screenshots/scr1.png?raw=true)

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
