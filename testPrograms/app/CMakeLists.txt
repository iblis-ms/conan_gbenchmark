# Author: Marcin Serwach
# https://github.com/iblis-ms/conan_gbenchmark

cmake_minimum_required(VERSION 2.8.12)

project(GBenchmarkTestProgram CXX)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(PROGRAM_NAME "${PROJECT_NAME}_${CMAKE_SYSTEM_NAME}_${CMAKE_CXX_COMPILER_ID}")

message(STATUS "Program name: ${PROGRAM_NAME}")

add_executable(${PROGRAM_NAME} GBenchmarkExample.cpp)

find_package(Threads)

target_link_libraries(${PROGRAM_NAME} PRIVATE ${CONAN_LIBS} PRIVATE ${CMAKE_THREAD_LIBS_INIT})

set_target_properties(${PROGRAM_NAME} PROPERTIES CXX_STANDARD 11)

