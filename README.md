# 🛠️ conan-toolchains

This repository contains Conan recipes for toolchains and command line
utilities, for example the Emscripten SDK or other compilers. These recipes are
maintained independently of [Conan Center Index](https://github.com/conan-io/conan-center-index)
with flexible maintenance scopes.

---

## 🌟 Why a separate repo?

A **centralized** toolchains repository provides a dedicated home for *SDKs*,
compilers, cross-compilers, and experimental toolchains all in one place. It's
a great fit for a wide range of users: beginners can easily install a toolchain
alongside Conan and quickly cross-compile a project, while advanced users can
integrate it into their workflow by adding it as a local recipe index and
tailoring recipes as needed. It also supports bleeding-edge or niche toolchains
that don't belong in the main index, offering maximum flexibility and
control.

---

## 🚀 Getting started

Ensure [Conan](conan.io) is installed and available in your path.
If it isn't, check the Conan [downloads](https://docs.conan.io/2/installation.html) page to install it.

### Setup the `conan-toolchains` repo

This repo can be added to Conan as a [local recipe index](https://docs.conan.io/2/devops/devops_local_recipes_index.html#devops-local-recipes-index) repository. This means that Conan will retrieve recipes from it.


```sh
git clone https://github.com/conan-io/conan-toolchains.git
conan remote add conan-toolchains ./conan-toolchains
```

This repository is still under active development, and no Conan remote with pre-built binaries is available yet.


## EMSDK - Emscripten

There are specific profiles created to use the `emsdk` toolchain recipe.
Read the [Emscripten Compiler Profiles for Conan readme](conan_config/profiles/emsdk/README.md) to learn more about how to use them.


## Contributing

If you wish to contribute to **conan-toolchains**, follow these steps to clone the repository
and install the required development dependencies.

```
git clone git@github.com:conan-io/conan-toolchains.git
cd conan-toolchains
# Recommended: Setup your virtual environment before installing dependencies
pip install pre-commit
```

We use [pre-commit](https://pre-commit.com/) to enforce code style and formatting. To
activate the pre-commit hooks:

```
pre-commit install
```

This will ensure that every time you commit changes, the code will be formatted and linted
according to the project's standards.
