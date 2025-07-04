# EMSDK - Emscripten Compiler Profiles for Conan

This repository provides a collection of pre-built Conan profiles that can be
used as a reference for **cross-compiling projects to WebAssembly (WASM)**.

📘 For detailed information and usage examples, refer to the official [Conan
documentation](https://docs.conan.io/2/examples/cross_build/emscripten.html#setting-up-conan-profile-for-webassembly-wasm).

💡 Issues and suggestions are welcome via the `conan-toolchains` repository.
Contributions are encouraged!


## 🧭 Introduction

As of **Conan 2.18**, the `emcc` compiler (from
[Emscripten](https://emscripten.org/docs/)) is natively supported. This allows
accurate modeling of the compiler’s built-in features.

The current `emcc` compiler model includes the following settings:

```
emcc:
    version: [ANY]
    libcxx: [null, libstdc++, libstdc++11, libc++]
    threads: [null, posix, wasm_workers]
    cppstd: [null, 98, gnu98, 11, gnu11, 14, gnu14, 17, gnu17, 20, gnu20, 23, gnu23, 26, gnu26]
    cstd: [null, 99, gnu99, 11, gnu11, 17, gnu17, 23, gnu23]
```

> ℹ️ Note: `emcc` is a front-end for the `clang` compiler, so it shares many of the same settings and options.

However, there are a few **important caveats** to consider when using Emscripten with Conan.


## ⚠️ Caveats

### 🔄 ABI Incompatibility

There is **no ABI compatibility guarantee** between different `emcc` versions.
Refer to the [Emscripten Changelog](https://github.com/emscripten-core/emscripten/blob/main/ChangeLog.md) for details.

In Conan v2, the `compiler.version` setting mostly acts as **syntactic sugar**. While it doesn't influence compilation directly, it:

- Enables Conan to apply version-specific flags, compile and link flags.
- Ensures distinct **package IDs** for different compiler versions.

To prevent ABI issues, make sure your **Conan profile's `compiler.version`**
matches the **actual `emsdk` version** used. This ensures consistent builds and
automatic recompilation when updating `emsdk`.



### 🧵 Multithreading

The `emcc` compiler can produce incompatible binaries depending on whether threading is enabled.

Refer to the Emscripten documentation on [pthreads](https://emscripten.org/docs/porting/pthreads.html#compiling-with-pthreads-enabled)
and [wasm workers](https://emscripten.org/docs/api_reference/wasm_workers.html).

Emscripten supports two threading models:

- **POSIX Threads (Pthreads)**
- **Wasm Workers**

These are **mutually incompatible**, and this distinction must be reflected in the Conan profile to avoid mixing binaries.

Enable threading in your profile by setting:

```ini
compiler.threads=posix        # For Pthreads
compiler.threads=wasm_workers # For Wasm Workers
```

Conan will automatically inject the necessary linker flags.

## 📂 Profile Overview

This repository includes the following profiles:
- `wasm32`: WebAssembly 32-bit target (default).
- `wasm64`: Experimental 64-bit WebAssembly target (for projects needing >4 GB dynamic memory).
- `local`: Use your locally installed emsdk instead of the Conan-managed one.


⚠️ WASM64 caveats:

The latest node version `emsdk/4.0.10` installs is the `node/22.16.0`, which can not run directly wasm64 binaries.
Also, it is not valid to compile wasm64 with `-sMIN_NODE_VERSION=221600`, see following error:
```
em++: warning: MIN_NODE_VERSION=221600 is not compatible with MEMORY64 (230000 or above required) [-Wcompatibility]
```
Thus, to be able to run an `wasm64` binary you will need to download at least `node/23` manually in your system.

🛠️ For the local profile:
- Ensure `emcc`, `em++`, `emar`, etc. are available in your `PATH`.
- Check the `[buildenv]` section in the profile.
- Optionally, provide your own `Emscripten.cmake` via the `user_toolchains` setting.
- Define the arch setting: `wasm`, `wasm64`, or the mostly deprecated `asm.js`.


## ▶️ Usage

After installing the profiles (TBD), you can build your project like this:

```
$ conan build <path> -pr emsdk/wasm32
```

### 🧠 Dynamic Memory Allocation

By default, WebAssembly does not allow dynamic memory growth. To enable it, you must set the following linker flag:

`-s ALLOW_MEMORY_GROWTH=1`

Our base profiles enable this flag by default to simplify usage.

If you want to disable memory growth, simply remove or comment out the relevant line in the profile.

🔎 The Conan docs explain the dynamic memory limits for each architecture.
These are also preconfigured in the `wasm32` and `wasm64` profiles and can be
customized as needed, including the `INITIAL_MEMORY` setting.


### 🙌 Contribute

Feel free to open issues or pull requests in the `conan-toolchains` repository.
Contributions to extend or improve these profiles are welcome!
