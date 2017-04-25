#!/bin/bash

set -e

function runCommand()
{
  local compiler=$1
  local compilerVersion=$2
  local libc=$3
  
  echo "-----------------------------------------------------------"
  echo "-----------------------------------------------------------"
  echo "Compiler: $compiler version: $compilerVersion libcxx: $libc"
  echo "-----------------------------------------------------------"

  rm -rf ~/.conan/data/gbenchmark
  conan test_package -s compiler=$compiler -s compiler.version=$compilerVersion -s compiler.libcxx=$libc
}

function runCompilerTest()
{
  local compilerCC=$1
  local compilerCXX=$2
  local compilerVersion=$3
  local compilerConan=$4
  local compilerVersionConan=$5
  export CC=/usr/bin/$compilerCC-$compilerVersion
  export CXX=/usr/bin/$compilerCXX-$compilerVersion

  for (( i=6; i<=$#; i+=1 ))
  do
    runCommand $compilerConan $compilerVersionConan  ${!i}
  done
}

runCompilerTest clang clang++ 4.0 clang 4.0 libc++ libstdc++11 libstdc++
runCompilerTest clang clang++ 3.9 clang 3.9 libc++ libstdc++11 libstdc++
runCompilerTest clang clang++ 3.8 clang 3.8 libc++ libstdc++11 libstdc++

runCompilerTest gcc g++ 6 gcc 6.2 libstdc++ libstdc++11
runCompilerTest gcc g++ 5 gcc 5.4 libstdc++ libstdc++11
runCompilerTest gcc g++ 4.8 gcc 4.8 libstdc++ libstdc++11

