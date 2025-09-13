const char* dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *  C := C + A * B
 * where A, B, and C are n-by-n matrices stored in row-major format.
 * On exit, A and B maintain their input values. */
void square_dgemm_blocked(int n, int block_size, double* A, double* B, double* C) {
	// Assume n % block_size == 0
	// Loop over all blocks and perfrom block matmul
	for (int block_i = 0; block_i < n; block_i += block_size) {
		for (int block_j = 0; block_j < n; block_j += block_size) {
			for (int block_k = 0; block_k < n; block_k += block_size) {

				// Perform matrix multiplication on every element inside the block
				for (int i = block_i; i < block_i + block_size; ++i) {
					for (int j = block_j; j < block_j + block_size; ++j) {
						int idx_c = i * n + j;
						for (int k = block_k; k < block_k + block_size; ++k) {
							int idx_a = i * n + k;
							int idx_b = k * n + j;
							C[idx_c] += A[idx_a] * B[idx_b];
						}
					}
				}
			}
		}
	}
}
