# Author: Marcin Serwach
# https://github.com/iblis-ms/conan_gbenchmark

from conans import ConanFile, CMake
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
        folderNameDownloaded = 'benchmark'
        folderNameWithVersion = 'benchmark-%s' % self.version
     
        if os.environ.get('APPVEYOR') == 'True':
            git = '\"C:\\Program Files\\Git\\mingw64\\bin\\git.exe\"' # git is not present in PATH on AppVeyor
        else:
            git = 'git'
        self.run('%s clone https://github.com/google/benchmark.git' % git)
        shutil.move(folderNameDownloaded, folderNameWithVersion)
        self.run("cd %s && %s checkout tags/v%s -b %s" % (folderNameWithVersion, git, self.version, self.version))
    
    def build(self):
        cmake = CMake(self)

        for (opt, val) in self.options.items():
            if val is not None:
                cmake.definitions[opt] = 'ON' if val == "True" else 'OFF'

        if self.settings.compiler == 'clang' and str(self.settings.compiler.libcxx) == 'libc++':
            cmake.definitions['BENCHMARK_USE_LIBCXX'] = 'YES'

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
