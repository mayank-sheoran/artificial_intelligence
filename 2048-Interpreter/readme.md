# Compiler Construction Assignment
<i>Submission by Mayank Sheoran: 2018A7PS0114G</i>

The assignment is written in ```lex yacc C++``` and compiled using ```g++ bison flex```.



## Code Structure

Following files are used :
 
- <code>game.l</code> : This is the scanner file written in `lex`. This converts the given input into various `Tokens`.
- <code>game.y</code> : This is the parser file written in `yacc`. This receives tokens from the scanner and runs instructions accordingly.
- <code>game.h</code> : header file containing definition for some functions used in game.cpp and is refered by game.y 
- <code>game.cpp</code> : CPP file containing 2048 Game with implementation of All functions and main function.
- <code>makefile</code> : used to compile the program.

## Compiling and Initialization

We can Compile the Code using make command as follows :-

<code>make</code>

This might take 20-30 sec to compile and form output file named as 2048
Therefore to Run the Game run following command !

<code>./2048</code>



## Assumption
 
Given a row ` 4 2 2 4 ` than, SUBTRACT LEFT will result in ` 4 4 0 0 `.