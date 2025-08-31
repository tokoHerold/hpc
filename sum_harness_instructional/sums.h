#ifndef __sum_h_
#define __sum_h_

#include <cstdint>

extern void setup(int64_t N, float A[]);

// Changed this to float, otherwise it won't compile
extern float sum(int64_t N, float A[]);

#endif
