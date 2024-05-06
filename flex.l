%{
#include "parser.tab.h"
%}

%%
[ \t]              ; // Ignore whitespace
\n                 { return '\n'; }

"stat"             { return STAT; }
"modify"           { return MODIFY; }
"say"              { return SAY; }
"turns"            { return TURNS; }
"check"            { return CHECK; }
"fail"             { return FAIL; }
"success"          { return SUCCESS; }
"consequence"      { return CONSEQUENCE; }
"rest"             { return REST; }

[a-zA-Z][a-zA-Z0-9_]*   { yylval.str = strdup(yytext); return IDENTIFIER; }
[0-9]+                  { yylval.num = atoi(yytext); return NUMBER; }
"+"                     { return PLUS; }
"-"                     { return MINUS; }
"DC"                    { return DC; }
":"                     { return COLON; }
"("                     { return LPAREN; }
")"                     { return RPAREN; }
","                     { return COMMA; }
";"                     { return SEMICOLON; }
.                       { /* Ignore other characters */ }

%%

int yywrap() {
    return 1;
}
