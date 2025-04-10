import os
from pathlib import Path

from conan import ConanFile
from conan.errors import ConanInvalidConfiguration
from conan.tools.files import get, copy, replace_in_file

required_conan_version = ">=2.7"

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

    def validate(self):
        if self.settings.os != "Macos" and self.settings.arch != "x86_64":
            raise ConanInvalidConfiguration("ccache binaries are only provided for x86_64 architectures")

    def build(self):
        arch = str(self.settings.arch) if self.settings.os != "Macos" else "universal"
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][arch],
            destination=self.source_folder, strip_root=True)

    def package_id(self):
        if self.info.settings.os == "Macos":
            del self.info.settings.arch

    def package(self):
        copy(self, "*GPL-*.txt", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "LICENSE.*", src=self.build_folder, dst=os.path.join(self.package_folder, "licenses"))
        copy(self, "ccache", src=self.build_folder, dst=os.path.join(self.package_folder, "bin"))
        copy(self, AUTOIJECT_CMAKE, src=self.build_folder, dst=self.package_folder)

    def finalize(self):
        copy(self, "*", src=self.immutable_package_folder, dst=self.package_folder)
        # TODO: find a way of retrieving conan home without accessing private API
        # replace_in_file(self, os.path.join(self.package_folder, AUTOIJECT_CMAKE), "<CONAN_HOME>", self._conan_helpers.cache.store)
        replace_in_file(self, os.path.join(self.package_folder, AUTOIJECT_CMAKE), "<CONAN_HOME>", str(Path.home()))

    def package_info(self):
        self.cpp_info.libdirs = []
        self.cpp_info.includedirs = []
        if self.conf.get("user.ccache:auto_inject", default=True, check_type=bool):
            self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", os.path.join(self.package_folder, AUTOIJECT_CMAKE))
