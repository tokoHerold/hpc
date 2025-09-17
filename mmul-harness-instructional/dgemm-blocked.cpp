#include <cstring>
const char* dgemm_desc = "Blocked dgemm.";

/* This routine performs a dgemm operation
 *  C := C + A * B
 * where A, B, and C are n-by-n matrices stored in row-major format.
 * On exit, A and B maintain their input values. */
// void square_dgemm_blocked(int n, int block_size, double* __restrict A, double* __restrict B, double* __restrict C) {
void square_dgemm_blocked(int n, int block_size, double* A, double* B, double* C) {
	double* row_tile_buffer = new double[n * block_size];
	double* col_tile_buffer = new double[n * block_size];
	double* tile_buffer = new double[block_size * block_size];

	for (int block_i = 0; block_i < n; block_i += block_size) {
		// Copy optimization: Load A[block_i:block_i+block_size, 0:n] into buffer
		memcpy(row_tile_buffer, &A[block_i * n], (size_t) block_size * n * sizeof(double));

		for (int block_j = 0; block_j < n; block_j += block_size) {
			// Copy optimization: Load B[0:n, block_j:block_j+block_size] into buffer
			for (int row = 0, dst_offset = 0; row < n; ++row, dst_offset += block_size) {
				memcpy(&col_tile_buffer[row * block_size], &B[row * n + block_j], block_size * sizeof(double));
			}
			// Copy optimization: Load C[block_i:block_i+block_size, block_j:block_j+block_size] into buffer
			for (int row = 0; row < block_size; ++row) {
				memcpy(&tile_buffer[row * block_size], &C[(block_i + row) * n + block_j], block_size * sizeof(double));
			}

			for (int block_k = 0; block_k < n; block_k += block_size) {

				// Perform matrix multiplication on every element inside the block
				for (int i = 0; i < block_size; ++i) {
					for (int j = 0; j < block_size; ++j) {
						int idx_c = i * block_size + j;
						for (int k = 0; k < block_size; ++k) {
							int idx_a = i * n + (block_k + k);
							int idx_b = (block_k + k) * block_size + j;
							tile_buffer[idx_c] += row_tile_buffer[idx_a] * col_tile_buffer[idx_b];
						}
					}
				}  // End inner multiplication
			}

			// Write back tile to C
			for (int row = 0; row < block_size; ++row) {
				memcpy(&C[(block_i + row) * n + block_j], &tile_buffer[row * block_size], block_size * sizeof(double));
			}
		}
	}
		delete[] row_tile_buffer;
		delete[] col_tile_buffer;
		delete[] tile_buffer;
}

