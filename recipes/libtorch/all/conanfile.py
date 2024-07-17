from conan import ConanFile
from conan.tools.build import check_min_cppstd
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout, CMakeDeps
from conan.tools.files import apply_conandata_patches, export_conandata_patches, get
from conan.tools.microsoft import is_msvc_static_runtime
from conan.tools.scm import Git


class libtorchRecipe(ConanFile):
    name = "libtorch"
    version = "2.3.0"
    package_type = "library"

    license = "BSD-3-Clause"
    url = "https://github.com/conan-io/conan-recipes-contrib"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}

    implements = ["auto_shared_fpic"]

    def requirements(self):
        is_windows = self.settings.os == "Windows"

        self.requires("libuv/[>=1 <2]")
        self.requires("fmt/[^10]")
        self.requires("foxi/[*]")
        self.requires("fp16/[*]")
        self.requires("xnnpack/[>=cci.20240229]")
        self.requires("pthreadpool/[*]")
        self.requires("libbacktrace/[*]")
        self.requires("openblas/[*]", options={'build_lapack': not is_windows})
        self.requires("onnx/[>=1 <2]")
        self.requires("cpuinfo/[*]")
        self.requires("eigen/[>=3 <4]")
        self.requires("pybind11/[>=2 <3]", transitive_libs=False)
        self.requires("protobuf/[*]")
        self.tool_requires("protobuf/<host_version>")

        if not is_windows:
            self.requires("sleef/[<3.6]")

    def validate(self):
        check_min_cppstd(self, "17")

    def layout(self):
        cmake_layout(self, src_folder="src")

    def export_sources(self):
        export_conandata_patches(self)

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)
        apply_conandata_patches(self)
        # git = Git(self)
        # git.clone(url="https://github.com/pytorch/pytorch.git",
        #           args=[
        #               '--branch=v2.3.0', '--depth=1', '--recurse-submodules',
        #               '-j4'
        #           ],
        #           target=".")
        # git.checkout(commit="v2.3.0")
        # url = "https://github.com/pytorch/pytorch/releases/download/v2.3.0/pytorch-v2.3.0.tar.gz"
        # checksum = "69579513b26261bbab32e13b7efc99ad287fcf3103087f2d4fdf1adacd25316f"
        # get(self, url=url, sha256=checksum, strip_root=True)

    def generate(self):
        deps = CMakeDeps(self)
        deps.set_property("libbacktrace", "cmake_file_name", "Backtrace")
        deps.set_property("cpuinfo", "cmake_target_name", "cpuinfo")
        deps.set_property("xnnpack", "cmake_target_name", "XNNPACK")
        deps.set_property("pthreadpool", "cmake_target_name", "pthreadpool")
        deps.set_property("sleef", "cmake_target_name", "sleef")
        deps.generate()

        tc = CMakeToolchain(self)
        tc.cache_variables["BUILD_CAFFE2"] = "OFF"
        tc.cache_variables["BUILD_TEST"] = "OFF"

        tc.cache_variables["USE_CUDA"] = "OFF"
        tc.cache_variables["BUILD_PYTHON"] = "OFF"
        tc.cache_variables["USE_SYSTEM_LIBS"] = True
        tc.cache_variables["USE_DISTRIBUTED"] = False
        tc.cache_variables["BLAS"] = "OpenBLAS"

        tc.cache_variables["USE_OPENMP"] = False
        tc.cache_variables["CMAKE_DISABLE_FIND_PACKAGE_OpenMP"] = True
        tc.cache_variables["CMAKE_DISABLE_FIND_PACKAGE_MKL"] = True
        # tc.cache_variables["CMAKE_DISABLE_FIND_PACKAGE_BLAS"] = True

        tc.cache_variables["USE_GLOO"] = False
        tc.cache_variables["ONNX_ML"] = False
        tc.cache_variables["USE_MPI"] = False
        tc.cache_variables["USE_MAGMA"] = False
        tc.cache_variables["USE_MKL"] = False
        tc.cache_variables["USE_MKLDNN"] = False
        tc.cache_variables["USE_TENSORPIPE"] = self.settings.os == "Windows"
        tc.cache_variables["USE_SYSTEM_FP16"] = False
        tc.cache_variables["USE_FBGEMM"] = False  #vendored in?
        tc.cache_variables["USE_FAKELOWP"] = False
        tc.cache_variables["USE_METAL"] = False
        tc.cache_variables["USE_NUMPY"] = False
        tc.cache_variables["USE_KINETO"] = False
        tc.cache_variables["USE_CCACHE"] = False
        

        tc.cache_variables["CAFFE2_LINK_LOCAL_PROTOBUF"] = False
        tc.cache_variables["BUILD_CUSTOM_PROTOBUF"] = False
        tc.cache_variables[
            "CAFFE2_USE_MSVC_STATIC_RUNTIME"] = is_msvc_static_runtime(self)

        tc.cache_variables["CMAKE_BUILD_TYPE"] = str(self.settings.build_type)

        if self.dependencies.host["libbacktrace"]:
            tc.cache_variables["CMAKE_REQUIRE_FIND_PACKAGE_Backtrace"] = True

        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.bindirs = ['lib'] # for torch_cpu.dll on Windows
        self.cpp_info.includedirs = [
            'include/torch/csrc/api/include', 'include'
        ]

        # TODO: 
        # - on windows probably need to link against one or two libraries, not more
        # - handle static vs shared properly, shared has fewer libraries because they're "baked" into the main library 
        self.cpp_info.libs = ["torch_cpu", "c10", "Caffe2_perfkernels_avx2", "Caffe2_perfkernels_avx512", "Caffe2_perfkernels_avx", "nnpack", "qnnpack", "pytorch_qnnpack", "clog"]

