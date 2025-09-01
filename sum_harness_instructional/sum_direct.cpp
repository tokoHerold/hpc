#include <string.h>

#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

#include "sums.h"

void setup(int64_t N, float A[]) {
	// printf(" inside direct_sum problem_setup, N=%ld \n", N);
}

/**
 * @brief Calculates the sum from 0 to N directly, i.e., using registers.
 */
float sum(int64_t N, float A[]) {
	// Remove printf statement
	// printf(" inside direct_sum perform_sum, N=%ld \n", N);
	float sum = 0;
	for (int i = 0; i < N; ++i) {
		sum += i;
	}
	return sum;
}
