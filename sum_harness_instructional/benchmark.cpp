//
// (C) 2022-2023, E. Wes Bethel
// benchmark-* harness for running different versions of the sum study
//    over different problem sizes
//
// usage: no command line arguments
// set problem sizes, block sizes in the code below

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <string.h>
#include <vector>

#include "sums.h"

/* The benchmarking program */
int main(int argc, char **argv) {
    std::cout << std::fixed << std::setprecision(2);

#define MAX_PROBLEM_SIZE 1 << 28 //  256M
    std::vector<int64_t> problem_sizes{
        MAX_PROBLEM_SIZE >> 5, MAX_PROBLEM_SIZE >> 4, MAX_PROBLEM_SIZE >> 3,
        MAX_PROBLEM_SIZE >> 2, MAX_PROBLEM_SIZE >> 1, MAX_PROBLEM_SIZE};

#define ITERATIONS 1

    float *A = (float *)malloc(sizeof(float) * MAX_PROBLEM_SIZE);

    // int n_problems = problem_sizes.size(); // unused variable

    /* For each test size */
    for (int64_t n : problem_sizes) {
        float t;
        // printf("Working on problem size N=%ld \n", n);

        // invoke user code to set up the problem
        setup(n, &A[0]);

        // insert your timer code here
        std::chrono::time_point<std::chrono::high_resolution_clock> start_time =
            std::chrono::high_resolution_clock::now();

        // invoke method to perform the sum
		for (int i = 0; i < ITERATIONS; ++i) {
			t = sum(n, &A[0]);
		}

        // insert your end timer code here, and print out elapsed time for this
        // problem size
		std::chrono::time_point<std::chrono::high_resolution_clock> end_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<double> elapsed = end_time - start_time;

        // printf(" Sum result = %lf, time = %f \n", t, elapsed.count() / ITERATIONS);
		// <Problem size>, <time>, <sum result>
		printf("%ld, %f, %lf\n", n, elapsed.count() / ITERATIONS, t);

    } // end loop over problem sizes
}

// EOF
