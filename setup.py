import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "anchor-exp==0.0.2.0",
        "backcall==0.2.0",
        "blis==0.7.4; python_version >= '3.6'",
        "catalogue==1.0.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "certifi==2020.12.5",
        "chardet==3.0.4",
        "cycler==0.10.0",
        "cymem==2.0.5",
        "decorator==4.4.2",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "imageio==2.9.0",
        "importlib-metadata==3.1.1; python_version >= '3.6'",
        "ipython==7.19.0",
        "ipython-genutils==0.2.0",
        "jedi==0.17.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "joblib==0.17.0; python_version >= '3.6'",
        "jsonpickle==1.4.1",
        "kiwisolver==1.3.1; python_version >= '3.6'",
        "lime==0.2.0.1; python_version >= '3.5'",
        "matplotlib==3.3.3; python_version >= '3.6'",
        "murmurhash==1.0.5",
        "networkx==2.5; python_version >= '3.6'",
        "numpy==1.19.4",
        "parso==0.7.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pexpect==4.8.0; sys_platform != 'win32'",
        "pickleshare==0.7.5",
        "pillow==9.0.0; python_version >= '3.6'",
        "plac==1.1.3",
        "preshed==3.0.5",
        "prompt-toolkit==3.0.8; python_full_version >= '3.6.1'",
        "ptyprocess==0.6.0",
        "pygments==2.7.3; python_version >= '3.5'",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "python-dateutil==2.8.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pywavelets==1.1.1; python_version >= '3.5'",
        "requests==2.25.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "scikit-image==0.17.2; python_version >= '3.6'",
        "scikit-learn==0.23.2; python_version >= '3.6'",
        "scipy==1.5.4",
        "six==1.15.0; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "spacy==2.3.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "srsly==1.0.5",
        "thinc==7.4.3",
        "threadpoolctl==2.1.0; python_version >= '3.5'",
        "tifffile==2020.12.4; python_version >= '3.7'",
        "tqdm==4.54.1; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "traitlets==5.0.5; python_version >= '3.7'",
        "urllib3==1.26.2; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
        "wasabi==0.8.0",
        "wcwidth==0.2.5",
        "zipp==3.4.0; python_version >= '3.6'",
    ],
    name="argueview",
    version="0.2.1",
    author="Sophia Hadash",
    author_email="s.hadash@tue.nl",
    description="ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SophiaHadash/ArgueView",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Development Status :: 3 - Alpha",
    ],
    keywords="explanations, text, toulmin, argumentation",
    python_requires=">=3.5",
)
