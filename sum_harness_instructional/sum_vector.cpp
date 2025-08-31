#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <string.h>
#include <vector>

#include "sums.h"

void setup(int64_t N, float A[]) {
    printf(" inside sum_vector problem_setup, N=%ld \n", N);
    for (int i = 0; i < N; ++i) {
        A[i] = (float)i;
    }
}

/**
 * @brief Calculates the sum from 0 to N by accumulating the values in A.
*/  
float sum(int64_t N, float A[]) {
    float sum = 0;
    for (int i = 0; i < N; ++i) {
        sum += A[i];
    }
    return sum;
}
