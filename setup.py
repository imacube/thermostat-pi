import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thermopi",
    version="0.0.1",
    author="Ryan",
    author_email="ryan@imacube.net",
    description="Manages a house thermostat.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/imacube/thermopi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)