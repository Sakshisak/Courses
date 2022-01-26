%{
    #include<iostream>
    #include "y.tab.h"
    #include<math.h>
    #include<cstring>
    void yyerror (char *s);
    extern int yyparse();
%}

digit    [0-9]
alpha    [a-zA-Z_]
alphanum ({alpha}|{digit})
ws       [ \t\n]
%%
"calculate"		{ return print; }
"print"			{ return print; }
"exit"			{ return exit_command; }
sin     {return sine;}
cos     {return cose;}
tan     {return tane;}
log     {return loge;}
pow     {return powe;}
{digit}+"."{digit}+	{ yylval.num = atof(yytext); return number; }
{digit}+		{ yylval.num = atof(yytext); return number; }
{alpha}{alphanum}*	{ yylval.id = strdup(yytext); return identifier;}
{ws}                	;
[-+\(\)=/*;]            { return yytext[0]; }
"#".*			;

.                      	{ ECHO;  yyerror("Unexpected Character"); }
%%
int yywrap (void) 	{ return 1; }
int main() 
{ 
  
    extern FILE *yyin, *yyout;
    char* file;
    scanf("%s\n",file);
    yyin = fopen(file, "r"); 
  
    yylex(); 
    yyparse();
    return 0; 
} 
