import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="argueview-shadash",
    version="0.0.1",
    author="Sophia Hadash",
    author_email="s.hadash@tue.nl",
    description="ArgueView is a tool for generating text-based presentations for machine-learning predictions and feature-importance based explanation tools. The tool makes use of Toulmin's model of argumentation for structuring the text-based explanations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/argueview",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
