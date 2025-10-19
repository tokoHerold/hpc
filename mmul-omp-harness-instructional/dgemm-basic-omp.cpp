#include <omp.h>

#include "likwid-stuff.h"

const char* dgemm_desc = "Basic implementation, OpenMP-enabled, three-loop dgemm.";

/*
 * This routine performs a dgemm operation
 *  C := C + A * B
 * where A, B, and C are n-by-n matrices stored in row-major format.
 * On exit, A and B maintain their input values.
 */
void square_dgemm(int n, double* A, double* B, double* C) {
	// insert your code here: implementation of basic matrix multiply with OpenMP parallelism enabled
#pragma omp parallel
	{
#ifdef LIKWID_PERFMON
		LIKWID_MARKER_START(MY_MARKER_REGION_NAME);
#endif
#pragma omp for collapse(2)
		for (int row = 0; row < n; ++row) {
			for (int col = 0; col < n; ++col) {
				int idx_c = row * n + col;
				for (int i = 0; i < n; ++i) {
					int idx_a = row * n + i;
					int idx_b = i * n + col;
					C[idx_c] += A[idx_a] * B[idx_b];
				}
			}
		}
#ifdef LIKWID_PERFMON
		LIKWID_MARKER_STOP(MY_MARKER_REGION_NAME);
#endif
	}

	// be sure to include LIKWID_MARKER_START(MY_MARKER_REGION_NAME) inside the block of parallel code,
	// but before your matrix multiply code, and then include LIKWID_MARKER_STOP(MY_MARKER_REGION_NAME)
	// after the matrix multiply code but before the end of the parallel code block.
}
