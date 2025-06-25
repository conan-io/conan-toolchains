from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
import os


class TestPackageConan(ConanFile):
    settings = "os", "arch", "compiler", "build_type"
    generators = "CMakeToolchain", "VirtualBuildEnv"

    def build_requirements(self):
        self.tool_requires(self.tested_reference_str)

    def layout(self):
        cmake_layout(self)

    def build(self):
        if self.settings.os == "Emscripten":
            cmake = CMake(self)
            cmake.configure()
            cmake.build()

    def test(self):
        # Check the package provides working binaries
        self.run("emcc -v")
        self.run("em++ -v")
        self.run("node -v")

        if self.settings.os == "Emscripten":
            test_file = os.path.join(self.cpp.build.bindirs[0], "test_package.js")
            self.run(f"node {test_file}")
