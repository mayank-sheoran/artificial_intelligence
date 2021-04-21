
#ifndef _GAME_H_
#define _GAME_H_
#include<bits/stdc++.h>
using namespace std;

void yyerror(char *s);
int yylex();

// For 2048 [game.c]

// int grid[4][4];
// int tempGrid[4][4];
// int emptyPos[4][4];
// int tileCNT = 0;
// set<int> emptyTileCNT;
// vector<vector<string>> storeVar(17);
void transpose(int arr[4][4]);
void reverse_column(int arr[4][4]);
// int storePos[4][4] = {0};
void printGrid(int grid[4][4]);
void doMove(int op,int dir);
void doLeft(int op);
void doRight(int op);
void doUp(int op);
void doDown(int op);
void mergeLeft(int op);
void mergeRight(int op);
int operate(int op);
void compressLeft();
void compressRight();
void rotateClockwise();
void rotateAntiClockwise();
void assignNum(int val,int x,int y);
int getValue(int x,int y);
void setVar(char* var, int x, int y);
void findFromVar(char* var);
void make_stderr(int flag);
#endif