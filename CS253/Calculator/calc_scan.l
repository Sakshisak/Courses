%{
    #include<iostream>
    #include "y.tab.h"
    #include<cstring>
    void yyerror (char *s);
%}

digit    [0-9]
alpha    [a-zA-Z_]
alphanum ({alpha}|{digit})
ws       [ \t\n]
%%
"calculate"		{ return print; }
"print"			{ return print; }
"exit"			{ return exit_command; }
"#".*           {}
{digit}+.{digit}+ {yylval.num = atof(yytext); return number;}
{digit}+		{ yylval.num = atoi(yytext); return number; }
{alpha}{alphanum}*	{ yylval.id = strdup(yytext); return identifier;}
{ws}                	;
[-+\(\)=/*;]            { return yytext[0]; }
.                      	{ ECHO;  yyerror("Unexpected Character"); }
%%
int yywrap (void) 	{ return 1; }
