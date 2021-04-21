%{
    #include <stdio.h>
    #include<stdlib.h>
    #include<string.h>
    #include "game.h"
    #define YYTYPE int
    extern "C"
    {
        int yyparse(void);
    }
    void yyerror(char *c) 
    {
        fprintf(stderr, "Syntax error.\n");
        make_stderr(0);
    }

%}

%union 
{
  int number;
  char *varname;
};


%start statements
%type <number> operation direction

%token VARNAME NUMBER
%type <number> NUMBER
%type <varname> VARNAME
%type <number> value
%type <number> x
%type <number> y
%type <number> all err_st

%token ADD MULTIPLY DIVIDE SUBTRACT
%token LEFT RIGHT UP DOWN
%token IS TO ASSIGN VALUE VAR IN
%token EOL COMMA NEWLINE


%%


statements: statement EOL {;}
          | statement statements EOL {;}
          |
;

statement: operation direction EOL NEWLINE {doMove($1,$2); return 0;}
         | operation direction NEWLINE {printf("You need to end a command with a full-stop.\n"); make_stderr(0); YYACCEPT;}
         | ASSIGN value TO x COMMA y EOL NEWLINE {assignNum($2,$4,$6); return 1;}
         | ASSIGN value TO x COMMA y NEWLINE {printf("You need to end a command with a full-stop.\n");make_stderr(0); YYACCEPT;}
         | VAR VARNAME IS x COMMA y EOL NEWLINE {setVar($2,$4,$6); YYACCEPT;}
         | VAR VARNAME IS x COMMA y NEWLINE {printf("You need to end a command with a full-stop.\n");make_stderr(0); YYACCEPT;}
         | VALUE IN x COMMA y EOL NEWLINE {getValue($3,$5); return 3;}
         | VALUE IN x COMMA y NEWLINE {printf("You need to end a command with a full-stop.\n");make_stderr(0); YYACCEPT;}
         | VALUE IN VARNAME EOL NEWLINE { findFromVar($3); YYACCEPT;}
         | VALUE IN VARNAME NEWLINE {printf("You need to end a command with a full-stop.\n");make_stderr(0); YYACCEPT;}
         | err_st NEWLINE {printf("Syntax error.\n"); YYACCEPT;}
;

operation: ADD {$$ = 1;}
         | SUBTRACT {$$ = 2;}
         | MULTIPLY {$$ = 3;}
         | DIVIDE {$$ = 4;}
;

direction: LEFT {$$ = 1;}
         | RIGHT {$$ = 2;}
         | UP {$$ = 3;}
         | DOWN {$$ = 4;}
;

value: NUMBER
     | VALUE IN x COMMA y {$$ = getValue($3,$5);};

;


x: NUMBER;
y: NUMBER;


err_st: all err_st
    |       all { make_stderr(0);}
    ;

all: ADD | SUBTRACT | MULTIPLY | DIVIDE | LEFT | RIGHT | UP | DOWN | ASSIGN | TO | VAR | IS | VALUE | IN | EOL | NUMBER | COMMA | VARNAME { $$ = 0; };
%%

