# Author: Marcin Serwach
# https://github.com/iblis-ms/conan_gbenchmark

from conans import ConanFile, CMake, tools
from conans.model.settings import Settings
from conans.tools import get
import os

from conans import *


class GbenchmarkConan(ConanFile):
    name = 'gbenchmark'
    version = '1.1.0'
    license = 'MIT LIcence'
    url = 'https://github.com/iblis-ms/conan_gbenchmark/tree/development'
    description = 'Conan.io support for Google Benchmark'
    settings = ['os', 'compiler', 'build_type', 'arch']
    options = {
        'BENCHMARK_ENABLE_TESTING':   ['ON', 'OFF'], 
        'BENCHMARK_ENABLE_LTO':       ['ON', 'OFF'],
        'BENCHMARK_USE_LIBCXX':       ['ON', 'OFF']
    }
    default_options = ('BENCHMARK_ENABLE_TESTING=OFF',
                       'BENCHMARK_ENABLE_LTO=OFF',
                       'BENCHMARK_USE_LIBCXX=OFF')
    generators = 'cmake'
    source_root = 'benchmark-%s' % version

    def source(self):
        zip_name = 'v%s.zip' % self.version
        get('https://github.com/google/benchmark/archive/%s' % zip_name)

    def build(self):
        cmake = CMake(self)

        for (opt, val) in self.options.items():
            if val is not None:
                cmake.definitions[opt] = val

        settingsConverted = Settings()
        if settingsConverted.get_safe('compiler.libcxx') == 'libc++':
            cmake.definitions['BENCHMARK_USE_LIBCXX'] = 'ON'

        codePath = os.path.join(self._conanfile_directory, self.source_root)
        cmake.configure(source_dir=codePath, build_dir='_build')
        
        cmake.build()

    def package(self):
        self.copy(pattern='*.h', dst='include', src='%s/include' % self.source_root, keep_path=True)
        self.copy(pattern='*.lib', dst='lib', src='_build/src', keep_path=False)
        self.copy(pattern='*.a', dst='lib', src='_build/src', keep_path=False)

        for docPatter in ['*.md', 'LICENSE', 'AUTHORS', 'CONTRIBUTORS']:
            self.copy(pattern=docPatter, dst='doc', src=self.source_root, keep_path=False)

    def package_info(self):  
        self.cpp_info.libs = ['benchmark']
        if Settings().get_safe('os') == 'Windows':
            self.cpp_info.libs.extend(['Shlwapi']) 
