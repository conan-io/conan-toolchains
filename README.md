# 🛠️ conan-toolchains

This repository contains Conan recipes for toolchains and command line
utilities, for example the Emscripten SDK or other compilers. These recipes are
maintained independently of [Conan Center Index](https://github.com/conan-io/conan-center-index)
with flexible maintenance scopes.


## 🌟 Why a separate repo?

A **centralized** toolchains repository provides a dedicated home for *SDKs*,
compilers, cross-compilers, and experimental toolchains all in one place. It's
a great fit for a wide range of users: beginners can easily install a toolchain
alongside Conan and quickly cross-compile a project, while advanced users can
integrate it into their workflow by adding it as a local recipe index and
tailoring recipes as needed. It also supports bleeding-edge or niche toolchains
that don't belong in the main index, offering maximum flexibility and
control.

## 🧰 Reference Profiles

This repository includes several **pre-configured Conan profiles** designed to make toolchain setup effortless:

To install the respective profiles:

```sh
$ conan config install https://github.com/conan-io/conan-toolchains.git -sf conan_config
```

Profiles could be later listed:
```sh
$ conan profile list
```
Toolchain profiles will be located under `<toolchain_name>/<profile>`.
Profiles starting with dot (`.`) are considered *base* which are used for other profiles and should not be used directly.


## 🚀 Getting started

### Setup `conan-toolchains` as a [local recipe index](https://docs.conan.io/2/devops/devops_local_recipes_index.html#devops-local-recipes-index) repository

Before adding `conan-toolchains` ensure [conan](https://github.com/conan-io/conan) is installed and available in your path.
Check conan [downloads](https://docs.conan.io/2/installation.html) page.

```sh
git clone https://github.com/conan-io/conan-toolchains.git
conan remote add conan-toolchains ./conan-toolchains
```

This repository is still under active development, and no Conan remote with pre-built binaries is available yet.


## Contributing

We welcome and appreciate contributions to **conan-toolchains**!

We recommend using [pre-commit](https://pre-commit.com/) to enforce code style and formatting. To
activate the pre-commit hooks contributors could optionally run the following commands:

```
# Setup your virtual environment before installing dependencies
pip install pre-commit
pre-commit install
```

This will ensure that every time you commit changes, the code will be formatted and linted
according to the project's standards.
