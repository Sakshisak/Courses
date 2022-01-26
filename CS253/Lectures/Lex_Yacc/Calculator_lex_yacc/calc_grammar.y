%{
    void yyerror (char *s);
    int yylex();

    #include <iostream>
    #include <stdio.h>     /* C declarations used in actions */
    #include <stdlib.h>
    #include <string.h>
    #include <utility>
    #include <ctype.h>
    #include <sstream>
    #include <unordered_map>

    /* Container to store parse values and results. */
    std::unordered_map<std::string, int> symbol_table;

    int symbolVal(const char* symbol);
    void updateSymbolVal(const char* symbol, int val);
    extern int yyparse();
%}

/* Yacc definitions */

%union {int num; const char* id;}         

%start program

%token print
%token exit_command
%token <num> number
%token <id> identifier

//%type stmt_list program assignment
%type <num> exp term

%left '+' '-'
%left '*' '/'
%%

/* descriptions of expected inputs  &   corresponding actions */

program : stmt_list
        ;

stmt_list : stmt_list assignment ';' 
          | stmt_list print exp ';'    {printf("%d\n", $3);}
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
    ;

term : number     { $$ = $1; }
     | identifier { $$ = symbolVal($1); } 
     ;

%%     

/* returns the value of a given symbol from symbol table */
int symbolVal(const char* symbol)
{
std::string find(symbol);
    return symbol_table[find];
}

/* updates the value of a given symbol in symbol table */
void updateSymbolVal(const char* symbol, int val)
{
    std::string input(symbol);
    symbol_table[input] = val;
}

int main (void) {
    return yyparse();
}

void yyerror (char *s) {fprintf (stderr, "%s\n", s);} 

