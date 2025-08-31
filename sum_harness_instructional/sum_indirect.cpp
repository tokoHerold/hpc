#include <algorithm>
#include <chrono>
#include <cstdlib>
#include <iomanip>
#include <iostream>
#include <random>
#include <ratio>
#include <string.h>
#include <vector>

#include "sums.h"

void setup(int64_t N, float A[]) {
    printf(" inside sum_indirect problem_setup, N=%ld \n", N);
    for (int i = 0; i < N; ++i) {
        A[i] = (float)(lrand48() % N);
    }
}

float sum(int64_t N, float A[]) {
    int64_t next = N - 1; // Prevent libc call
    float sum = 0;
    for (int i = 0; i < N; ++i) {
        float tmp = A[next];
        sum += tmp;
        next = (int)tmp;
    }
    return sum;
}
