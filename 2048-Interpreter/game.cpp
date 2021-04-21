#include<bits/stdc++.h>
extern "C"
{
    int yyparse(void);
}
using namespace std;

#include "game.h"
int grid[4][4];
int tempGrid[4][4];
int emptyPos[4][4];
int tileCNT = 0;
set<int> emptyTileCNT;
vector<vector<string>> storeVar(17);
int storePos[4][4] = {0};

void printGrid()
{
    cout << endl;
    cout << "_________________"<< endl;
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=0 ; col<4 ; col++)
        {
            cout << "| " << grid[row][col] << " ";
        }
        cout << "|"<<endl;
        cout << "_________________"<< endl;
    }
}

void updateEmptyPos()
{
    emptyPos[4][4]={1};
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=0 ; col<4 ; col++)
        {
            if(grid[row][col]==0)
            {
                emptyPos[row][col]=0;
            }
        }
    }
}

vector<int> generateRandomTile()
{
    vector<pair<int,int>> availPos;
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=0 ; col<4 ; col++)
        {
            if(grid[row][col]==0)
            {
                availPos.push_back(make_pair(row,col));
            }
        }
    }
    int index = rand()%(availPos.size());
    int row = availPos[index].first;
    int col = availPos[index].second;
    if(emptyTileCNT.empty())
    {
        tileCNT++;
        storePos[row][col] = tileCNT;
    }
    else
    {
        storePos[row][col] = *emptyTileCNT.begin();
        emptyTileCNT.erase(storePos[row][col]);
    }
    int prob = rand()%10;
    int number=4;
    if(prob <= 7) number = 2;
    return {row,col,number};
}

void doMove(int op,int dir)
{
    if(dir == 1) doLeft(op);
    if(dir == 2) doRight(op);
    if(dir == 3) doUp(op);
    if(dir == 4) doDown(op);
    cout << endl;
    updateEmptyPos();
    vector<int> randomTile = generateRandomTile();
    int row = randomTile[0];
    int col = randomTile[1];
    int val = randomTile[2];
    grid[row][col]=val;
    cout << "Thanks, left move done, random tile added."<<endl;
    make_stderr(1);
    printGrid();
}

void doLeft(int op)
{
    compressLeft();
    mergeLeft(op);
    compressLeft();
}
void doRight(int op)
{
    compressRight();
    mergeRight(op);
    compressRight();
}
void doUp(int op)
{
    rotateClockwise();
    doRight(op);
    rotateAntiClockwise();
}
void doDown(int op)
{
    rotateClockwise();
    doLeft(op);
    rotateAntiClockwise();
}

int operate(int number,int op)
{
    if(op == 1) return 2*number;
    if(op == 2) return 0;
    if(op == 3) return number*number;
    if(op == 4) return 1;
}

void mergeLeft(int op)
{
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=1 ; col<4 ; col++)
        {
            if(grid[row][col] == 0) break;
            if(grid[row][col-1]==grid[row][col])
            {
                grid[row][col-1] = operate(grid[row][col],op);
                grid[row][col]=0;
                emptyTileCNT.insert(storePos[row][col]);
                vector<string> x = storeVar[storePos[row][col-1]];
                vector<string> y = storeVar[storePos[row][col]];
                for(auto iter: y) 
                {
                    storeVar[storePos[row][col-1]].push_back(iter);
                }                
                storePos[row][col] = 0;
                storeVar[storePos[row][col]].clear();

                if(grid[row][col-1]==0)
                {
                    emptyTileCNT.insert(storePos[row][col-1]);
                    storeVar[storePos[row][col-1]].clear();
                    storePos[row][col-1] = 0;
                }
            }
        }
    }
}

void mergeRight(int op)
{
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=2 ; col>=0 ; col--)
        {
            if(grid[row][col] == 0) break;
            if(grid[row][col+1]==grid[row][col])
            {
                grid[row][col+1] = operate(grid[row][col],op);
                grid[row][col]=0;
                emptyTileCNT.insert(storePos[row][col]);
                vector<string> x = storeVar[storePos[row][col+1]];
                vector<string> y = storeVar[storePos[row][col]];
                for(auto iter: y) 
                {
                    storeVar[storePos[row][col+1]].push_back(iter);
                }
                storePos[row][col] = 0;
                storeVar[storePos[row][col]].clear();

                if(grid[row][col+1]==0)
                {
                    emptyTileCNT.insert(storePos[row][col+1]);
                    storeVar[storePos[row][col+1]].clear();
                    storePos[row][col+1] = 0;
                }
            }
        }
    }
}

void compressLeft()
{
    for(int row=0 ; row<4 ; row++)
    {
        vector<int> rowElems;
        vector<int> tileNumber;
        for(int col=0 ; col<4 ; col++)
        {
            if(grid[row][col]!=0) 
            {
                rowElems.push_back(grid[row][col]);
                tileNumber.push_back(storePos[row][col]);
            }
        }
        for(int col=0 ; col<rowElems.size() ; col++)
        {
            grid[row][col] = rowElems[col];
            storePos[row][col] = tileNumber[col];
        }
        for(int col=rowElems.size() ; col<4 ; col++)
        {
            grid[row][col] = 0;
            storePos[row][col] = 0;
        }
    }
}

void compressRight()
{
    for(int row=0 ; row<4 ; row++)
    {
        vector<int> rowElems;
        vector<int> tileNumber;
        for(int col=0 ; col<4 ; col++)
        {
            if(grid[row][col]!=0) 
            {
                rowElems.push_back(grid[row][col]);
                tileNumber.push_back(storePos[row][col]);
            }
        }
        for(int col=0 ; col<4-rowElems.size() ; col++)
        {
            grid[row][col] = 0;
            storePos[row][col] = 0;
        }
        for(int col=4-rowElems.size() ; col<4 ; col++)
        {
            grid[row][col] = rowElems[col-4+rowElems.size()];
            storePos[row][col] = tileNumber[col-4+rowElems.size()];
        }
    }
}

void rotateClockwise()
{
    for (int i = 0; i < 4 / 2; i++) 
    {
        for (int j = i; j < 4 - i - 1; j++) 
        {
            int temp = grid[i][j];
            grid[i][j] = grid[4 - 1 - j][i];
            grid[4 - 1 - j][i] = grid[4 - 1 - i][4 - 1 - j];
            grid[4 - 1 - i][4 - 1 - j] = grid[j][4 - 1 - i];
            grid[j][4 - 1 - i] = temp;
        }
    }
    for (int i = 0; i < 4 / 2; i++) 
    {
        for (int j = i; j < 4 - i - 1; j++) 
        {
            int temp = storePos[i][j];
            storePos[i][j] = storePos[4 - 1 - j][i];
            storePos[4 - 1 - j][i] = storePos[4 - 1 - i][4 - 1 - j];
            storePos[4 - 1 - i][4 - 1 - j] = storePos[j][4 - 1 - i];
            storePos[j][4 - 1 - i] = temp;
        }
    }
}
void transpose(int arr[4][4])
{
    for (int i = 0; i < 4; i++)
    for (int j = i; j < 4; j++)
    swap(arr[i][j], arr[j][i]);
}

void reverse_column(int arr[4][4])
{
    int k;
    for (int i = 0; i < 4; i++)
    {
        k = 4-1;
        for (int j = 0; j < k; j++)
        {
            swap(arr[j][i], arr[k][i]);
            k--;
        }
    }
}

void rotateAntiClockwise()
{
    transpose(grid);
    transpose(storePos);
    reverse_column(grid);
    reverse_column(storePos);
}

void assignNum(int num,int x,int y)
{
    if(x>4 || y>4 || x<0 || y<0)
    {
        cout << "There is no tile like that. The tile co-ordinates must be in the range 1,2,3,4." << endl;
        make_stderr(0);
        return;
    }
    grid[x-1][y-1] = num;
    updateEmptyPos();
    cout << "\nThanks, assignment done.\n\n";
    make_stderr(1);
    printGrid(); 
    
}

int getValue(int x,int y)
{
    cout << "Value at [" << x << "," << y << "] is " << grid[x-1][y-1] << endl;
    make_stderr(1);
    return grid[x-1][y-1];
}

void setVar(char* var, int x, int y)
{
    int tileNo = storePos[x-1][y-1];
    if(tileNo == 0)
    {
        cout << "Empty Tile Detected\n" << endl;
        make_stderr(0);
        return;
    }
    string addVar(var);
    storeVar[tileNo].push_back(addVar);
    cout << "Var -> " << addVar << " has been set to [" << x << "," << y << "] \n";
    cout << endl;
    make_stderr(1);
}

void findFromVar(char* var)
{
    string check(var);
    for(int tile=1 ; tile<17 ; tile++)
    {   
        for(auto variable: storeVar[tile])
        {
            if(check == variable)
            {
                for(int row=0 ; row<4 ; row++)
                {
                    for(int col=0 ; col<4 ; col++)
                    {
                        if(storePos[row][col] == tile)
                        {
                            cout << "Value for " << var << " is -> " << grid[row][col] << "Found At [" << row << "," << col << "]\n" << endl;
                            return;
                        }
                    }
                }
                
            }
        }
    }
    cout << "Sorry No Such Var is Assigned !\n";
}

pair<int,int> findLoc(int tile)
{
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=0 ; col<4 ; col++)
        {
            if(storePos[row][col]==tile)
            {
                return make_pair(row,col);
            }
        }
    }
    return make_pair(-1,-1);
}

typedef struct 
{
    pair<int,int> rc;
    vector<string> vars;
} sortElem;

bool cmpSort(sortElem a, sortElem b)
{
    if(a.rc.first == b.rc.first)
        return a.rc.first < b.rc.first;
    return a.rc.second < b.rc.second;
}

void make_stderr(int flag)
{
    if(flag == 1)
    {
        for(int row=0 ; row<4 ; row++)
        {
            for(int col=0 ; col<4 ; col++)
            {
                fprintf(stderr,"%d ",grid[row][col]);
            }
        }
        sortElem temp[17];
        int index=0;
        for(int i=1;i<17;i++)
        {
            vector<string> vars = storeVar[i];
            if(vars.size()!=0)
            {
                temp[index].rc = findLoc(i);
                temp[index].vars = storeVar[i];
                index++;
            }
        }
        sort(temp,temp+index,cmpSort);
        for(int i=0 ; i<index ; i++)
        {
            fprintf(stderr,"%d,%d",temp[i].rc.first+1,temp[i].rc.second+1);
            string str;
            char* prnt;
            for(int j=0 ; j<temp[i].vars.size()-1 ; j++)
            {
                str = temp[i].vars[j];
                prnt = strcpy(new char[str.length() + 1], str.c_str());
                fprintf(stderr,"%s,",prnt);
            }
            str = temp[i].vars[temp[i].vars.size()-1];
            prnt = strcpy(new char[str.length() + 1], str.c_str());
            fprintf(stderr,"%s ",prnt);
        }
        fprintf(stderr,"\n");
        
    }
    else
    {
        fprintf(stderr,"%d\n",-1);
    }
}

int main()
{
    // GRID INIT
    cout << "Hi, I am the 2048-game Engine." <<endl;
    cout << "The start state is:" <<endl;
    for(int row=0 ; row<4 ; row++)
    {
        for(int col=0 ; col<4 ; col++)
        {
            grid[row][col] = 0;
        }
    }
    vector<int> randomTile = generateRandomTile();
    int row = randomTile[0];
    int col = randomTile[1];
    int val = randomTile[2];
    grid[row][col]=val;
    updateEmptyPos();
    printGrid();
    while(1)
    {
        cout << "\nPlease type a command." <<endl << "----> ";
        int ret = yyparse();
    }

    return 0;


}