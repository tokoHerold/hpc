#include <string.h>

#include <algorithm>
#include <cassert>
#include <chrono>
#include <cstdint>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <ratio>
#include <vector>

#include "sums.h"

void setup(int64_t N, float A[]) {
	// Fill array
	for (int i = 0; i < N; ++i) {
		A[i] = i;
	}
	srand48(0x8);
	// Shuffle
	// Use Sattolo's algorithm: https://algo.inria.fr/seminars/summary/Wilson2004b.pdf
	// Specifically, this implementation: https://danluu.com/sattolo/
	for (int i = 0; i < N - 1; ++i) {
		int64_t j = i + 1 + (lrand48() % (N - i - 1));
		float tmp = A[i];
		A[i] = A[j];
		A[j] = tmp;
	}
	fflush(stdout);
}

/**
 * @brief Calculates the sum from 0 to N by accessing random values in A in a random pattern.
 * Only works properly if the problem size is big enough.
 */
float sum(int64_t N, float A[]) {
	int64_t next = N - 1;  // Prevent libc call, use random number directly
	float sum = 0;
	for (int i = 0; i < N; ++i) {
		float tmp = A[next];
		sum += tmp;
		next = (int) tmp;
	}
	return sum;
}
