//
// (C) 2022-2023, E. Wes Bethel
// benchmark-* harness for running different versions of the sum study
//    over different problem sizes
//
// usage: no command line arguments
// set problem sizes, block sizes in the code below

#include <algorithm>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <random>
#include <string.h>
#include <vector>

#include "sums.h"

#define MAX_PROBLEM_SIZE 1 << 28 //  256M
#define RUNTIME 10.0

/* The benchmarking program */
int main(int argc, char **argv) {
  std::cout << std::fixed << std::setprecision(2);

  std::vector<int64_t> problem_sizes{MAX_PROBLEM_SIZE >> 5, MAX_PROBLEM_SIZE >> 4, MAX_PROBLEM_SIZE >> 3,
                                     MAX_PROBLEM_SIZE >> 2, MAX_PROBLEM_SIZE >> 1, MAX_PROBLEM_SIZE};

  float *A = (float *)malloc(sizeof(float) * MAX_PROBLEM_SIZE);

  // int n_problems = problem_sizes.size(); // unused variable

  /* For each test size */
  for (int64_t n : problem_sizes) {
    float t;
    // printf("Working on problem size N=%ld \n", n);

    // invoke user code to set up the problem
    setup(n, &A[0]);

    // Measure time for one run
    std::chrono::time_point<std::chrono::high_resolution_clock> start_time = std::chrono::high_resolution_clock::now();
    t = sum(n, &A[0]);
    std::chrono::time_point<std::chrono::high_resolution_clock> end_time = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = end_time - start_time;

    // Number of  iteraions required to last RUNTIME seconds
    int iterations = (int)std::ceil(RUNTIME / elapsed.count());

    // == Actual Measurement ==
    // Start time measurement
    start_time = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < iterations; ++i) {
      // invoke method to perform the sum
      t = sum(n, &A[0]);
    }
    // stop measurement
    end_time = std::chrono::high_resolution_clock::now();

    printf("%ld, %f, %lf\n", n, elapsed.count() / iterations, t);

  } // end loop over problem sizes
}

// EOF
