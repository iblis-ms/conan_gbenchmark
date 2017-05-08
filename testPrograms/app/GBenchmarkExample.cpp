// Author: Marcin Serwach
// https://github.com/iblis-ms/conan_gbenchmark

// adds Google Benchmark header
#include <benchmark/benchmark.h>

#include <string>

void Benchmark_StringConcatenation(benchmark::State& aState) {
    std::string result;

    while (aState.KeepRunning()) { 
        result += "a";
    }
}

BENCHMARK(Benchmark_StringConcatenation);

BENCHMARK_MAIN();

