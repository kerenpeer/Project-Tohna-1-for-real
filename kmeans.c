#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <float.h>

void printMatrix(int rows, int cols, float** matrix);
void printMatrixint(int rows, int cols, int* matrix);
int pointSize(FILE* file);
int howManyLines(FILE* file);
void init(int K, float** datapointsArray, float** centroidsArray, int* whichClusterArray, int* amountOfPointsInCluster, FILE* file);
int findClosestCluster(float* point, float** centroidArray, int K, int sizeOfPoint);
void changeCluster(int i, int newCluster, int* whichClusterArray);
void calcNewCentroids(float** datapointsArray, float** centroidsArray, int* whichClusterArray, int* amountOfPointsInCluster, int N, int sizeOfPoint);
void makeCendroidsAndAmountZero(float** centroidsArray,int* amount, int K, int pointSize);
void free_double_pointer(float **array, int arrayLen);


void init(int K, float** datapointsArray, float** centroidsArray, int* whichClusterArray, int* amountOfPointsInCluster, FILE* file) {
    char* point, *line;
    int i, j;
    fseek(file, 0, SEEK_SET);
    i = 0;
    line = (char*) malloc(1000 * sizeof(char));
    assert(line && "line allocation failed");
    while (fgets(line, 1000, file) != NULL) {
        j = 0;
        point = strtok(line, ",");
        while (point != NULL) {
            datapointsArray[i][j] = atof(point);
            if (i < K) {
                centroidsArray[i][j] = atof(point);
            }
            point = strtok(NULL, ",");
            j = j + 1;
        }
        i = i + 1;
    }
    for (i = 0; i < K; i++) {
        whichClusterArray[i] = i;
        amountOfPointsInCluster[i] = 1;
    }
    free(line);
}

/* counts size of each datapoint */ 
int pointSize(FILE* file) {
    int numOfCords;
    char c;

    numOfCords = 1;
    fseek(file, 0, SEEK_SET);
    for (c = getc(file); c != '\n'; c = getc(file))
        if (c == ',') {
            numOfCords = numOfCords + 1;
        }
    return numOfCords;
}

/* counts lines in file */
int howManyLines(FILE* file) {
    int counterOfLines; /* Line counter (result) */
    char c;  /* To store a character read from file */
    fseek(file, 0, SEEK_SET);
    counterOfLines = 0;  
    /* Extract characters from file and store in character c */
    for (c = getc(file); c != EOF; c = getc(file))
        if (c == '\n') /* Increment count if this character is newline */
            counterOfLines = counterOfLines + 1;

    return counterOfLines;
}

void printMatrix(int rows, int cols, float** matrix) {
    int i, j; 
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            if (j == cols - 1) {
                printf("%.4f", matrix[i][j]);
            }
            else {
                printf("%.4f,", matrix[i][j]);
            }
        }
        printf("\n");
    }
}

void printMatrixint(int rows, int cols, int* matrix) {
    int i, j;
    for (i = 0; i < rows; i++) {
        for (j = 0; j < cols; j++) {
            printf("%d ,", matrix[i]);
        }
        printf("\n");
    }
}

int findClosestCluster(float* point, float** centroidArray, int K, int sizeOfPoint){
    float mindist, sum;
    int newCluster,i,j;
    float* centroidToCheck;

    mindist = FLT_MAX;
    for (i = 0; i < K; i++) {
        sum = 0;
        centroidToCheck = centroidArray[i];
        for (j = 0; j < sizeOfPoint; j++) {
            sum = sum + ((point[j] - centroidToCheck[j]) * (point[j] - centroidToCheck[j]));
        }
        if (sum < mindist) {
            mindist = sum;
            newCluster = i;
        }
    }
    return newCluster;
}

void changeCluster(int i, int newCluster, int* whichClusterArray) {
    whichClusterArray[i] = newCluster;
}

void makeCendroidsAndAmountZero(float** centroidsArray, int* amount, int K, int sizeOfPoint) {
    int i, j;
    for (i = 0; i < K; i++) {
        amount[i] = 0;
        for (j = 0; j < sizeOfPoint; j++) {
            centroidsArray[i][j] = 0.0;
        }
    }
}

void calcNewCentroids(float** datapointsArray, float** centroidsArray, int* whichClusterArray,
    int* amountOfPointsInCluster, int N, int sizeOfPoint) {
    int i, j, newCluster;
    float prevSum, newVal;
    for (i = 0; i < N; i++) {
        newCluster = whichClusterArray[i];
        for (j = 0; j < sizeOfPoint; j++) {
            prevSum = centroidsArray[newCluster][j] * amountOfPointsInCluster[newCluster];
            newVal = (prevSum + datapointsArray[i][j]) / (amountOfPointsInCluster[newCluster] + 1);
            centroidsArray[newCluster][j] = newVal;
        }
        amountOfPointsInCluster[newCluster] = amountOfPointsInCluster[newCluster] + 1;
    }
}

void free_double_pointer(float **array, int arrayLen){
    int i;
    for (i=0; i < arrayLen; i++){
        free(array[i]);
    }
    free(array);
}

int main(int argc, char* argv[]) {
    int i, j, K, itermax, iteration, isChanged, N, sizeOfPoint, * whichClusterArray, currentCluster, newCluster, * amountOfPointsInCluster;
    float** datapointsArray, ** centroidsArray, * point;
    FILE* file;

    file = stdin;

    assert((argc == 2 || argc == 3) && "wrong amount of command line arguments");

    K = atoi(argv[1]);

    if (argc == 3) {
        itermax = atoi(argv[2]);
    }
    else {
        itermax = 200;
    }

    N = howManyLines(file);
    sizeOfPoint = pointSize(file);
    datapointsArray = (float**)malloc((N) * sizeof(float*));
    assert(datapointsArray && "datapointsArray allocation failed");
    for (i = 0; i < N; i++) {
        datapointsArray[i] = (float*)malloc(sizeOfPoint * sizeof(float));
        assert(datapointsArray[i] && "datapointsArray allocation failed");
    }
    whichClusterArray = (int*)calloc(N, sizeof(int));
    assert(whichClusterArray && "whichClusterArray allocation failed");
    amountOfPointsInCluster = (int*)calloc(K, sizeof(int));
    assert(amountOfPointsInCluster && "amountOfPointsArray allocation failed");
    centroidsArray = (float**)malloc(K * sizeof(float*));
    assert(centroidsArray && "centroidsArray allocation failed");
    for (j = 0; j < K; j++) {
        centroidsArray[j] = (float*)malloc(sizeof(float) * sizeOfPoint);
        assert(centroidsArray[j] && "centroidsArray allocation failed");
    }
    init(K, datapointsArray, centroidsArray, whichClusterArray, amountOfPointsInCluster, file);

    isChanged = 1;
    iteration = 0;
    while (isChanged == 1) {
        if (iteration == itermax) {
            printf("main: max iteration reached\n");
            break;
        }
        iteration = iteration + 1;

        isChanged = 0;
        for (i = 0; i < N; i++) {
            point = datapointsArray[i];
            currentCluster = whichClusterArray[i];
            newCluster = findClosestCluster(point, centroidsArray, K, sizeOfPoint);  /* find new cluster by minimal norm */
            if (currentCluster != newCluster) {
                changeCluster(i, newCluster, whichClusterArray);
                isChanged = 1;
            }
        }
        makeCendroidsAndAmountZero(centroidsArray, amountOfPointsInCluster, K, sizeOfPoint);
        calcNewCentroids(datapointsArray, centroidsArray, whichClusterArray, amountOfPointsInCluster, N, sizeOfPoint); /* calc new centroid of new cluster for point[j] */
    }
    printMatrix(K, sizeOfPoint, centroidsArray);

    free(whichClusterArray);
    free(amountOfPointsInCluster);
    free_double_pointer(centroidsArray, K);
    free_double_pointer(datapointsArray, N);

    return 0;
}
