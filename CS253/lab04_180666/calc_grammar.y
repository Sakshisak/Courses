%{
    void yyerror (char *s);
    int yylex();

    #include <iostream>
    #include <stdio.h>     /* C declarations used in actions */
    #include <stdlib.h>
    #include <math.h>
    #include <unistd.h>
    #include <string.h>
    #include <utility>
    #include <ctype.h>
    #include <sstream>
    #include <cmath>
    #include <unordered_map>

    /* Container to store parse values and results. */
    std::unordered_map<std::string, float> symbol_table;

    float symbolVal(const char* symbol);
    void updateSymbolVal(const char* symbol, float val);
    extern int yyparse();
%}

/* Yacc definitions */

%union {float num; const char* id;}         

%start program

%token print
%token exit_command
%token <num> number
%token <id> identifier

//%type stmt_list program assignment
%type <num> exp term
%token SIN COS TAN LOG POW
%token comma

%left '+' '-'
%left '*' '/'
%%

/* descriptions of expected inputs  &   corresponding actions */

program : stmt_list
        ;

stmt_list : stmt_list assignment ';' 
          | stmt_list print exp ';'    {printf("%f\n", $3);}
          | stmt_list exit_command ';' {printf("Exitting...\n"); exit(0);}
          | /* Empty */
          ;

assignment : identifier '=' exp  { updateSymbolVal($1, $3); }
           ;

exp : term        { $$ = $1;}
    | exp '+' exp { $$ = $1 + $3;}
    | exp '-' exp { $$ = $1 - $3;}
    | exp '*' exp { $$ = $1 * $3;}
    | exp '/' exp { $$ = $1 / $3;}
    | '(' exp ')' { $$ = $2; }
    |SIN'('exp')'   {$$=sin($3);}
    |COS'('exp')'   {$$=cos($3);}
    |TAN'('exp')'   {$$=tan($3);}
    |LOG'('exp')'   {$$=log($3);}
    |POW'('exp comma exp')'   {$$=pow($3,$5);}
    ;

term : number     { $$ = $1; }
     | identifier { $$ = symbolVal($1); } 
     ;

%%     

/* returns the value of a given symbol from symbol table */
float symbolVal(const char* symbol)
{
std::string find(symbol);
    return symbol_table[find];
}

/* updates the value of a given symbol in symbol table */
void updateSymbolVal(const char* symbol, float val)
{
    std::string input(symbol);
    symbol_table[input] = val;
}

int main(int argc, char* argv[]) {
	extern FILE *yyin;
    FILE *fh;
    if(argc == 2){
	int result = access(argv[1], F_OK);
	if(result == 0){
		fh = fopen(argv[1], "r");
		yyin = fh;
	}
	else{
		fprintf (stderr, "File doesn't exist\n");
		exit(1);
	}
    }
    return yyparse();
}    

void yyerror (char *s) {fprintf (stderr, "%s\n", s);} 

