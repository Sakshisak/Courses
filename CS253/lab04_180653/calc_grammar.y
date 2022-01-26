%{
    void yyerror (char *s);
    int yylex();

    #include <iostream>
    #include <stdio.h>     /* C declarations used in actions */
    #include <stdlib.h>
    #include <string.h>
    #include <utility>
    #include <math.h>
    #include <ctype.h>
    #include <sstream>
    #include <unordered_map>

    /* Container to store parse values and results. */
    std::unordered_map<std::string, int> symbol_table;

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
%token  sine
%token  cose
%token  tane
%token  loge
%token  powe

//%type stmt_list program assignment
%type <num> exp term

%left '+' '-'
%left '*' '/'
%left loge
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
    | sine '(' exp ')' { $$ = sin($3); }
    | cose '(' exp ')' { $$ = cos($3); }
    | tane '(' exp ')' { $$ = tan($3);}
    | loge '(' exp ')' { $$ = log($3);}
    | powe '(' exp ',' exp ')' {$$ = pow($3,$5);}
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


void yyerror (char *s) {fprintf (stderr, "%s\n", s);} 

