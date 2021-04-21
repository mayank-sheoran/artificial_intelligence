%{ 
    // DEFINATIONS
    #include<stdio.h>
    #include<string.h>
    #include<stdlib.h>
    // #include "game.h"
    int yylex();
    #include "game.tab.hh"
%}


%%
    // RULES

"ADD"                   {return ADD;}
"SUBTRACT"              {return SUBTRACT;}
"MULTIPLY"              {return MULTIPLY;}
"DIVIDE"                {return DIVIDE;}

"LEFT"                  {return LEFT;}
"RIGHT"                 {return RIGHT;}
"UP"                    {return UP;}
"DOWN"                  {return DOWN;}

"ASSIGN"                {return ASSIGN;}
"VALUE"                 {return VALUE;}
[0-9]+                  {yylval.number = atoi(yytext);return NUMBER;}
"TO"                    {return TO;}
"IN"                    {return IN;}
"IS"                    {return IS;}

"VAR"                   {return VAR;}
[A-Za-z][0-9A-Za-z]*    {yylval.varname = strdup(yytext); return VARNAME;}


","                     {return COMMA;}
"."                     {return EOL;}
[\n]                    {return NEWLINE;}
[ \t]                   {;}


. ;
%%

// CODE SECTION
int yywrap()
{
    return 1;
}

