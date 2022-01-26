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
"#".*                   {}
","                     {return comma; }
"calculate"		{ return print; }
"print"			{ return print; }
"exit"			{ return exit_command; }
[0-9]+(\.[0-9]*)?       { yylval.num = atof(yytext); return number; }
sin                     {return SIN;}    
cos                     {return COS;}    
tan                     {return TAN;}        
log                     {return LOG;}
pow                     {return POW;}        
{alpha}{alphanum}*	{ yylval.id = strdup(yytext); return identifier;}
{ws}                	;
[-+\(\)=/*;]            { return yytext[0]; }
.                      	{ ECHO;  yyerror("Unexpected Character"); }
%%
int yywrap (void) 	{ return 1; }


