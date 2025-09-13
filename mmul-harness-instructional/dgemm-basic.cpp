const char* dgemm_desc = "Basic implementation, three-loop dgemm.";

/*
 * This routine performs a dgemm operation
 *  C := C + A * B
 * where A, B, and C are n-by-n matrices stored in row-major format.
 * On exit, A and B maintain their input values.
 */
void square_dgemm(int n, double* A, double* B, double* C) {
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
}
