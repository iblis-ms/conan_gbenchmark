# Conan.io with Google Benchmark

Linux/OSx
[![Build Status](https://travis-ci.org/iblis-ms/conan_gbenchmark.svg?branch=master)](https://travis-ci.org/iblis-ms/conan_gbenchmark)
Windows
[![Build status](https://ci.appveyor.com/api/projects/status/mdcs9fi2rj4qdoxs/branch/master?svg=true)](https://ci.appveyor.com/project/iblis-ms/conan-gbenchmark/branch/master)


Conan.io ([version 1.1.1](https://www.conan.io/downloads)) is a C/C++ package manager. It allows downloading, compiling external libraries for specific operating system, architecture or with given compilation flags. Conan.io can be extremely helpful with big project with many components by automatic downloading (and building if required) dependency components.
This repository contains configuration files to use Google Benchmark 1.3.0 with your code. 

# How to use it?

Conan.io's documentation of uploading packages to your server is on [http://docs.conan.io/en/latest/packaging/upload.html].
However, you can easily follow steps below:
* Download this repository
* Check if you have write permission in file *~/.conan_server/server.conf* (there is a meaningful description about its syntax). If you don't have this file (or entire folder), run Conan.io server.
* run Conan.io server: 
```
conan_server&
```
* Login to your Conan.io server (default: password: *demo* login *demo* - you can add users in *~/.conan_server/server.conf*):
```
conan user -p demo -r local demo
```
* Add local server to remote list:
```
conan remote add local http://localhost:9300
```
* Enter to directory with *conanfile.py*.
* Export *conanfile.py* to cache:
```
conan export ${REPO_ROOT} iblis_ms/stable
```
* Upload package:
```
conan upload GBenchmark/1.3.0@iblis_ms/stable --all -r=local
```
* To test if it is working correctly. Enter to *tests/app* folder.
* Run Conan.io to link program with Google Benchmark
```
conan install . --build -s compiler=gcc -s compiler.version=7.3 -s compiler.libcxx=libstdc++11
```
* See *conaninfo.txt* to check what you have already built. All settings options are in *~/.conan/settings.yaml*.

# Supported platforms and compilers

## Windows 7 64bits

CMake version: 3.8.1

* MinGW x86_64
  * version: 6.3.0
    - conan test test_package -s compiler=gcc -s compiler.version=6.3 -s compiler.libcxx=libstdc++11
    - conan test test_package -s compiler=gcc -s compiler.version=6.3 -s compiler.libcxx=libstdc++
* Visual Studio Community 
  * version: 2017
    - conan test test_package -s compiler="Visual Studio" -s compiler.version=15 -s compiler.runtime=MD
  * version: 2015
    - conan test test_package -s compiler="Visual Studio" -s compiler.version=14 -s compiler.runtime=MD

## Ubuntu 16.04 64bits

CMake version: 3.10.2

* GCC
  * version: 7.3
    - conan test test_package -s compiler=gcc -s compiler.version=7.3 -s compiler.libcxx=libstdc++
    - conan test test_package -s compiler=gcc -s compiler.version=7.3 -s compiler.libcxx=libstdc++11

* Clang
  * version: 5.0
    - conan test test_package -s compiler=clang -s compiler.version=5.0 -s compiler.libcxx=libc++
    - conan test test_package -s compiler=clang -s compiler.version=5.0 -s compiler.libcxx=libstdc++
    - conan test test_package -s compiler=clang -s compiler.version=5.0 -s compiler.libcxx=libstdc++11

## OSX Sierra 64bits

CMake version: 3.8.2

* Clang (apple-clang in Conan.io)
  * version: Apple LLVM version 8.1.0 (clang-802.0.42)
    - conan test_package -s compiler=apple-clang -s compiler.version=8.1 -s compiler.libcxx=libc++

## Linter Warnings

There are few warnings, that can be ignored - code is OK.

> Linter warnings
>    WARN: Linter. Line 4: Unable to import 'conans'
>    WARN: Linter. Line 5: Unable to import 'os'
>    WARN: Linter. Line 7: Unable to import 'shutil'
>    WARN: Linter. Line 47: Instance of 'list' has no 'compiler' member
>    WARN: Linter. Line 47: Instance of 'list' has no 'compiler' member
>    WARN: Linter. Line 66: Instance of 'list' has no 'os' member

