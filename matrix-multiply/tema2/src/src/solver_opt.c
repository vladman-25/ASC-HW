/*
 * Tema 2 ASC
 * 2023 Spring
 */
#include "utils.h"

#define blockSize 80

/*
 * Add your optimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	printf("OPT SOLVER\n");
	double* C = (double*) calloc(N * N, sizeof(double));


    double* tmp = (double*) calloc(N * N, sizeof(double));

	register double sum = 0.0;
	register int bi=0;
    register int bj=0;
    register int bk=0;
    register int i=0;
    register int j=0;
    register int k=0;

	register int bi_i;
	register int bj_j;
	// register int bk_k;
 
    for(bi=0; bi<N; bi+=blockSize) {
        for(bj=0; bj<N; bj+=blockSize) {
            for(bk=bi; bk<N; bk+=blockSize) {
                for(i=0; i<blockSize; ++i) {
					bi_i = (bi+i) * N;
                    for(j=0; j<blockSize; ++j) {
						bj_j = bj + j;
						sum = 0.0;
                        for(k=0; k<blockSize; ++k) {
							// bk_k = bk + k;
                            sum += A[bi_i + bk + k] * B[(bk + k)*N + bj_j];
						}
						tmp[bi_i + bj_j] += sum;
					}
				}
			}
		}
	}
	register int bj_j_N;
	for(bi=0; bi<N; bi+=blockSize) {
        for(bj=0; bj<N; bj+=blockSize) {
            for(bk=bj; bk<N; bk+=blockSize) {
                for(i=0; i<blockSize; ++i) {
					bi_i = (bi+i) * N;
                    for(j=0; j<blockSize; ++j) {
						bj_j = bj + j;
						bj_j_N = bj_j * N;
						sum = 0.0;
                        for(k=0; k<blockSize; ++k) {
							// bk_k = bk + k;
                            sum += tmp[bi_i + bk + k] * A[bj_j_N + bk + k];
						}
						C[bi_i + bj_j] += sum;
					}
				}
			}
		}
	}

    free(tmp);
	tmp = (double*) calloc(N * N, sizeof(double));
	//Bt*Bt

	register int bi_i_i;

	for(bi=0; bi<N; bi+=blockSize) {
        for(bj=0; bj<N; bj+=blockSize) {
            for(bk=0; bk<N; bk+=blockSize) {
                for(i=0; i<blockSize; ++i) {
					bi_i = (bi+i) * N;
					bi_i_i = bi+i;
                    for(j=0; j<blockSize; ++j) {
						bj_j = bj + j;
						bj_j_N = bj_j * N;
						sum = 0.0;
                        for(k=0; k<blockSize; ++k) {
							// bk_k = bk + k;
                            sum += B[(bk + k) * N + bi_i_i] * B[bj_j_N + bk + k];
						}
						C[bi_i + bj_j] += sum;
					}
				}
			}
		}
	}

    free(tmp);
    return C;
}
