%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


%}

%union {
    char *str;
    int num;
}

%token STAT_TYPE NARRATION_TYPE SAY TURNS ACTION CHECK SUCCESS CONSEQUENCE REST DC_OP EOL
%token OPEN_PAR CLOSE_PAR ADD_OP SUB_OP MUL_OP DIV_OP ASSIGN
%token IDENTIFIER NUMBER STRING

%type <str> IDENTIFIER STRING 
%type <num> NUMBER



%%

program: block
       ;



block: statement_list 
     ;

statement_list: /* empty */
              | statement_list statement
              ;

statement: EOL
    | STAT_TYPE IDENTIFIER EOL
    | NARRATION_TYPE IDENTIFIER EOL
    | NARRATION_TYPE IDENTIFIER ASSIGN STRING EOL
    | IDENTIFIER ASSIGN rel_exp EOL
    | IDENTIFIER ASSIGN STRING EOL
    | STAT_TYPE IDENTIFIER ASSIGN rel_exp EOL
    | SAY OPEN_PAR rel_exp CLOSE_PAR EOL
    | TURNS rel_exp ACTION EOL statement_list REST EOL
    | CHECK rel_exp EOL SUCCESS statement_list CONSEQUENCE EOL statement_list REST EOL
    ;


rel_exp:
    expression
    | rel_exp DC_OP expression
    ;

expression:
    term
    | expression ADD_OP term
    | expression SUB_OP term
    ;

term:
    factor
    | term MUL_OP factor
    | term DIV_OP factor
    ;

factor:
    NUMBER
    | STRING
    | IDENTIFIER
    | ADD_OP factor
    | SUB_OP factor
    | "not" factor
    | OPEN_PAR rel_exp CLOSE_PAR
    | "read" OPEN_PAR CLOSE_PAR
    ;

%%

int yyerror(const char *msg) {
    fprintf(stderr, "Parser Error: %s\n", msg);
    return 0;
}

int main() {
    return yyparse();
}
