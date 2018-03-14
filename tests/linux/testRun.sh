#!/bin/bash

set -e

currentScriptPath=$(readlink -f "$0")
currentDir=$(dirname "$currentScriptPath")

export repoBaseDir=$currentDir/../..

cd $repoBaseDir
echo "Run docker"
docker run conan_gbenchmark /bin/bash -c "cd /test/tests/linux && ./runAllTests.sh"

cd $currentDir
