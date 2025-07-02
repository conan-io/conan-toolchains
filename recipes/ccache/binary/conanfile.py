import os
from pathlib import Path

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy

required_conan_version = ">=2.1"

AUTOIJECT_CMAKE = "ccache-autoinject.cmake"

class CcacheConan(ConanFile):
    name = "ccache"
    package_type = "application"
    description = (
        "Ccache (or “ccache”) is a compiler cache. It speeds up recompilation "
        "by caching previous compilations and detecting when the same "
        "compilation is being done again."
    )
    license = "GPL-3.0-or-later"
    topics = ("compiler-cache", "recompilation", "cache", "compiler")
    homepage = "https://ccache.dev"
    url = "https://github.com/conan-io/conan-center-index"
    settings = "os", "arch"
    exports_sources = [AUTOIJECT_CMAKE]

    @property
    def _arch(self):
        return str(self.settings.arch) if self.settings.os != "Macos" else "universal"

    def validate(self):
        if self.conan_data["sources"][self.version].get(str(self.settings.os), {}).get(self._arch) is None:
            raise ConanInvalidConfiguration(f"ccache binaries do not support '{self.settings.os} - {self._arch}'")

    def build(self):
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][self._arch],
            destination=self.source_folder, strip_root=True)

    def package_id(self):
        if self.info.settings.os == "Macos":
            self.info.settings.arch = "universal"

    def package(self):
        copy(self, "*GPL-*.txt", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "LICENSE.*", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "ccache*", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"))
        copy(self, AUTOIJECT_CMAKE, src=self.build_folder, dst=self.package_folder)

    def package_info(self):
        self.cpp_info.libdirs = []
        self.cpp_info.includedirs = []
        if self.conf.get("user.ccache:auto_inject", default=True, check_type=bool):
            self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", os.path.join(self.package_folder, AUTOIJECT_CMAKE))

        # Set environment variables to allow ccache work correctly within conan build/create workflow
        base_dir = self.conf.get("user.ccache:base_dir", default=str(Path.home()), check_type=str)
        self.buildenv_info.define("CCACHE_BASEDIR", base_dir)
        self.buildenv_info.define("CCACHE_NOHASHDIR", "1")
