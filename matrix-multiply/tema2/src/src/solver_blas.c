/*
 * Tema 2 ASC
 * 2023 Spring
 */
#include "utils.h"
#include <cblas.h>
#include <string.h>
/* 
 * Add your BLAS implementation here
 */
double* my_solver(int N, double *A, double *B) {
	printf("BLAS SOLVER\n");
	double alpha = 1.0;
 
    double *C = malloc(N * N * sizeof(double));

    memmove(C, A, N * N * sizeof(double));

	double *B_res = malloc(N * N * sizeof(double));
	memmove(B_res, B, N * N * sizeof(double));


	//cblas_dtrmm(CblasRowMajor, CblasLeft, CblasUpper, CblasNoTrans, CblasNonUnit, N, N, alpha, A, N, B_res, N);
	//cblas_dtrmm(CblasRowMajor, CblasRight, CblasLower, CblasTrans, CblasNonUnit, N, N, alpha, B_res, N, C, N);
    //cblas_dgemm(CblasRowMajor, CblasTrans, CblasTrans, N, N, N, alpha, B, N, B, N, 1.0, C, N);

	cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans, N, N, N, alpha, A, N, B, N, 0.0, C, N);
	cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasTrans, N, N, N, alpha, C, N, A, N, 0.0, C, N);
    cblas_dgemm(CblasRowMajor, CblasTrans, CblasTrans, N, N, N, alpha, B, N, B, N, 1.0, C, N);
	free(B_res);
    return C;
}
