![My Package Logo](assets/logo.png)

This is dbnl_bear, a python package to make it easier to use AI for reading assistance in historical analaysis. 

The "bear" part of the package name is inspired by a passage from Alex Komoroske's Bits and Bobs:

"LLMs are like a trained circus bear that can make you porridge in your kitchen. It's a miracle that it's able to do it at all, but watch out because no matter how well they can act like a human on some tasks they're still a wild animal. They might ransack your kitchen, and they could kill you, accidentally or intentionally. Just because it can talk like a human doesn't mean it deserves the responsibility of a human!" (editorial changes by AvD)

The package is available on PyPi. However, currently, it's not perfect, and should be used with some caution. 

The goal of the package is to make it easier for historians to use AI in their research. It will assist in parsing texts, sending them to the OpenAI API, and viewing the results. 

See the notebook for info on how to use this.

## Installation

The package now ships with a modern `pyproject.toml` configuration.  You can
install it directly from the repository using:

```bash
pip install git+https://github.com/trister95/dbnl_bear.git
```

Or clone the repository and install in editable mode:

```bash
pip install -e .
```
