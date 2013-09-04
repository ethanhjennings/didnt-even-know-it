#include "stdio.h"
#include <stdlib.h>

int main()
{
    char * line = NULL;
    size_t inputlen = 0;
    inputlen = getline(&line,&inputlen,stdin) - 1;
    int * nums = (int*)malloc(sizeof(int)*inputlen);
    int i;
    for (i = 0; i < inputlen; i++)
    {
        nums[i] = (int)line[i];
        printf("%d, ", nums[i]);
    }
}
