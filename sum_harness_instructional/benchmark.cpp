//
// (C) 2022-2023, E. Wes Bethel
// benchmark-* harness for running different versions of the sum study
//    over different problem sizes
//
// usage: no command line arguments
// set problem sizes, block sizes in the code below

#include <string.h>

#include <algorithm>
#include <chrono>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

#include "sums.h"

#define MAX_PROBLEM_SIZE 1 << 28  //  256M

/* The benchmarking program */
int main(int argc, char **argv) {
	std::cout << std::fixed << std::setprecision(2);

	std::vector<int64_t> problem_sizes{MAX_PROBLEM_SIZE >> 5, MAX_PROBLEM_SIZE >> 4, MAX_PROBLEM_SIZE >> 3,
	                                   MAX_PROBLEM_SIZE >> 2, MAX_PROBLEM_SIZE >> 1, MAX_PROBLEM_SIZE};

	float *A = (float *) malloc(sizeof(float) * MAX_PROBLEM_SIZE);

	// int n_problems = problem_sizes.size(); // unused variable
	printf("N,runtime,expected,result\n");

	/* For each test size */
	for (int64_t n : problem_sizes) {
		float expected = ((float) n * ((float) n - 1.f)) / 2.f;
		float t;
		// printf("Working on problem size N=%ld \n", n);

		// invoke user code to set up the problem
		setup(n, &A[0]);

		// Start time measurement
		auto start_time = std::chrono::high_resolution_clock::now();

		// invoke method to perform the sum
		t = sum(n, &A[0]);

		// stop measurement
		auto end_time = std::chrono::high_resolution_clock::now();
		std::chrono::duration<double> elapsed = end_time - start_time;

		printf("%ld, %f, %f, %lf\n", n, elapsed.count(), expected, t);

	}  // end loop over problem sizes
}

// EOF
