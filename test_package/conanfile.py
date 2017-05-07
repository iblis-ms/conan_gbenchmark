# Author: Marcin Serwach
# https://github.com/iblis-ms/conan_gbenchmark

from conans import ConanFile, CMake
import os

channel = os.getenv("CONAN_CHANNEL", "stable")
username = os.getenv("CONAN_USERNAME", "iblis_ms")

class GbenchmarkTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    requires = "GBenchmark/1.1.0@%s/%s" % (username, channel)
    generators = "cmake"

    def build(self):
        cmake = CMake(self)
        cmake.definitions["CONAN_LIBCXX"] = "libstdc++11"
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        os.chdir("bin")
        self.run(".%sexample" % os.sep)
