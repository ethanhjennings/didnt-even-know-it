#include "stdio.h"
#include <stdlib.h>

typedef struct
{
    int * data;
    int size;
    int pos;
} Reg;

Reg * createReg(int size)
{
    Reg * r = (Reg *) malloc(sizeof(Reg));
    r->size = size;
    r->data = (int *) malloc(size*sizeof(int));
    r->pos = -1;   
}

void freeReg(Reg * r)
{
    free(r->data);
    free(r);
}

void pushReg(Reg * r, int val)
{
    r->pos++;
    r->data[r->pos] = val;
    if (r->pos >= r->size - 1)
    {
        r->size *= 2;
        r->data = (int *) realloc(r->data,r->size*sizeof(int));
    }
}

void popReg(Reg * r)
{
    if (r->pos >= 0)
        r->pos--;
}

int peekRegPos(Reg * r, int pos)
{
    if (r->pos >= 0)
        return r->data[pos];
    else
        return -1;
}

int peekReg(Reg * r)
{
    return peekRegPos(r,r->pos);
}

void assignRegPos(Reg *r, int val, int pos)
{
    if (r->pos < 0)
        pushReg(r,0);
    r->data[r->pos] = val;
}
void assignReg(Reg * r, int val) { 
    assignRegPos(r,val,r->pos); 
}

void inputString(Reg * reg)
{
    char * line = NULL;
    reg->size = 0;
    size_t inputlen;
    inputlen = getline(&line,&inputlen,stdin);
    reg->data = (int*)realloc(reg->data,sizeof(int)*inputlen);
    reg->size = inputlen;
    int i;
    for (i = 0; i < inputlen; i++)
    {
        reg->data[i] = (int)line[i];
    }
    reg->pos = reg->size - 1;
    free(line);
}

void inputChar(Reg * reg)
{
    char c;
    scanf("%c", &c);
    assignReg(reg, (int)c);
}

int inputInt(Reg * reg)
{
    int n;
    scanf("%d", &n);
    assignReg(reg, n);
}

void outputIntReg(Reg * reg, int startPos)
{
    int i = startPos;
    for (;i <= reg->pos; i++)
    {
        printf("%d",reg->data[i]);
        if (i < reg->pos - 1) 
            printf(", ");
    }
}

void outputStringReg(Reg * reg, int startPos)
{
    int i = startPos;
    for (;i <= reg->pos; i++)
    {
        printf("%c",(char)reg->data[i]);
    }   
}
