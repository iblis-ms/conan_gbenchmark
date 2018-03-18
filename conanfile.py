# Author: Marcin Serwach
# https://github.com/iblis-ms/conan_gbenchmark

from conans import ConanFile, CMake, tools
import os
import sys
import shutil

class GbenchmarkConan(ConanFile):
    name = 'GBenchmark'
    version = '1.3.0'
    license = 'MIT Licence'
    url = 'https://github.com/iblis-ms/conan_gbenchmark'
    description = 'Conan.io support for Google Benchmark'
    settings = ['os', 'compiler', 'build_type', 'arch', 'cppstd']
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
    buildFolder = '_build'

    def source(self):
        zipFileName = "v%s.zip" % self.version
        tools.download("https://github.com/google/benchmark/archive/%s" % zipFileName, zipFileName)
        tools.unzip(zipFileName)
    
    def build(self):
        cmake = CMake(self)

        for (opt, val) in self.options.items():
            if val is not None:
                cmake.definitions[opt] = 'ON' if val == "True" else 'OFF'

        if self.settings.compiler == 'clang' and str(self.settings.compiler.libcxx) == 'libc++':
            cmake.definitions['BENCHMARK_USE_LIBCXX'] = 'YES'

        if str(self.settings.compiler) in ['gcc', 'apple-clang', 'clang', 'sun-cc']:
            if str(self.settings.arch) in ['x86_64', 'sparcv9']:
                cmake.definitions['BENCHMARK_BUILD_32_BITS'] = 'OFF'
            elif str(self.settings.arch) in ['x86', 'sparc']:
                cmake.definitions['BENCHMARK_BUILD_32_BITS'] = 'YES'

        sys.stdout.write("cmake " + str(cmake.command_line) + "\n")

        cmake.configure(source_dir=self.build_folder, build_dir=self.buildFolder)
        
        cmake.build()

    def package(self):
        self.copy(pattern='*.h', dst='include', src='%s/include' % self.source_root, keep_path=True)
        self.copy(pattern='*.lib', dst='lib', src=os.path.join(self.buildFolder,'lib'), keep_path=False)
        self.copy(pattern='*.a', dst='lib', src=os.path.join(self.buildFolder,'lib'), keep_path=False)

        for docPatter in ['*.md', 'LICENSE', 'AUTHORS', 'CONTRIBUTORS']:
            self.copy(pattern=docPatter, dst='doc', src=self.source_root, keep_path=False)

    def package_info(self):  
        self.cpp_info.libs = ['benchmark']
        if self.settings.os == 'Windows':
            self.cpp_info.libs.extend(['Shlwapi']) 
