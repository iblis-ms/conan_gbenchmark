cmake_minimum_required(VERSION 2.8)
project(conanGoogleBenchmark)

include(conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

add_subdirectory("benchmark-1.3.0")
