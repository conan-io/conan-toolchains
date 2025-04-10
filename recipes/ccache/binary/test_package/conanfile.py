import os
from conan import ConanFile
from conan.tools.build import can_run
from conan.tools.cmake import CMake, cmake_layout
from conan.errors import ConanException


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def test(self):
        generated_file = os.path.join(self.dependencies.build[self.tested_reference_str].package_folder, "ccache-autoinject.cmake")
        if not os.path.exists(generated_file):
            raise ConanException("ccache-autoinject.cmake toolchain file does not exist")
        user_toolchain = self.conf.get("tools.cmake.cmaketoolchain:user_toolchain", check_type=list)
        if generated_file not in user_toolchain:
            raise ConanException("ccache not found in user toolchain")

        if can_run(self):
            self.run("ccache --version", env="conanbuild")

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
