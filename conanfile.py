# Author: Marcin Serwach
# https://github.com/iblis-ms/conan_gbenchmark

from conans import ConanFile, CMake, tools
from conans.model.settings import Settings
from conans.model.settings import SettingsItem
from conans.tools import get
import os
import sys

class GbenchmarkConan(ConanFile):
    name = 'GBenchmark'
    version = '1.1.0'
    license = 'MIT Licence'
    url = 'https://github.com/iblis-ms/conan_gbenchmark'
    description = 'Conan.io support for Google Benchmark'
    settings = ['os', 'compiler', 'build_type', 'arch']
    options = {
        'BENCHMARK_ENABLE_TESTING':     [True, False], 
        'BENCHMARK_ENABLE_LTO':         [True, False]
    }
    default_options = ('BENCHMARK_ENABLE_TESTING=False',
                       'BENCHMARK_ENABLE_LTO=False'
                      )
    generators = 'cmake'
    source_root = 'benchmark-%s' % version
    exports = 'CMakeLists.txt'

    def source(self):
        zip_name = 'v%s.zip' % self.version
        get('https://github.com/google/benchmark/archive/%s' % zip_name)

    def build(self):
        
        cmake = CMake(
            settings_or_conanfile = self,
            )

        for (opt, val) in self.options.items():
            if val is not None:
                cmake.definitions[opt] = 'ON' if val == "True" else 'OFF'

        if self.settings.compiler == 'clang' and str(self.settings.compiler.libcxx) == 'libc++':
            cmake.definitions['BENCHMARK_USE_LIBCXX'] = 'ON'

        sys.stdout.write("\ncmake %s %s\n\n" % (cmake.command_line, self._conanfile_directory))
        
        cmake.configure(source_dir=self._conanfile_directory, build_dir='_build')
        
        cmake.build()

    def package(self):
        self.copy(pattern='*.h', dst='include', src='%s/include' % self.source_root, keep_path=True)
        self.copy(pattern='*.lib', dst='lib', src='_build/lib', keep_path=False)
        self.copy(pattern='*.a', dst='lib', src='_build/lib', keep_path=False)

        for docPatter in ['*.md', 'LICENSE', 'AUTHORS', 'CONTRIBUTORS']:
            self.copy(pattern=docPatter, dst='doc', src=self.source_root, keep_path=False)

    def package_info(self):  
        self.cpp_info.libs = ['benchmark']
        if self.settings.os == 'Windows':
            self.cpp_info.libs.extend(['Shlwapi']) 
