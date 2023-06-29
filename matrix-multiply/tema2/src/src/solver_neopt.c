/*
 * Tema 2 ASC
 * 2023 Spring
 */
#include "utils.h"

/*
 * Add your unoptimized implementation here
 */
double* my_solver(int N, double *A, double* B) {
	printf("NEOPT SOLVER\n");
	double* C = (double*) calloc(N * N, sizeof(double));


    double* tmp = (double*) calloc(N * N, sizeof(double));
	//A*B
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                tmp[i*N+j] += A[i*N+k] * B[k*N+j];
            }
        }
    }
	//*At
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i*N+j] += tmp[i*N+k] * A[j*N+k];
            }
        }
    }

    free(tmp);
	tmp = (double*) calloc(N * N, sizeof(double));
	//Bt*Bt
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i*N+j] += B[k*N+i] * B[j*N+k];
            }
        }
    }

    free(tmp);
    return C;
}
