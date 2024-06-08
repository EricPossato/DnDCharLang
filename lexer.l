%{
#include "parser.tab.h"
#include <stdlib.h>
%}

%%

"stat"          { return STAT_TYPE; }
"narration"     { return NARRATION_TYPE; }
"say"           { return SAY; }
"turns"         { return TURNS; }
"action"        { return ACTION; }
"check"         { return CHECK; }
"success"       { return SUCCESS; }
"consequence"   { return CONSEQUENCE; }
"DC"            { return DC_OP; }
"not"           {return NOT;}
"roll"          {return ROLL;}
"rest"          {return REST;}

"("             { return OPEN_PAR; }
")"             { return CLOSE_PAR; }  

"+"             { return ADD_OP; }
"-"             { return SUB_OP; }
"*"             { return MUL_OP; }
"/"             { return DIV_OP; }
"="             { return ASSIGN; }

[0-9]+      { yylval.num = atoi(yytext); return NUMBER; }
\n      { return EOL; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval.str = strdup(yytext); return IDENTIFIER; }
\"([^"\\]|\\.)*\"       { /* Match strings */
                            /* Remove quotes and escape sequences */
                            yylval.str = malloc(strlen(yytext) - 1); /* -2 for removing quotes */
                            strncpy(yylval.str, yytext + 1, strlen(yytext) - 2); /* Copy without quotes */
                            yylval.str[strlen(yytext) - 2] = '\0'; /* Null-terminate */
                            return STRING;
                        }
[ \t]       ; /* Skip whitespace */
.           { fprintf(stderr, "Invalid character: %s\n", yytext); }

%%

int yywrap() {
    return 1;
}