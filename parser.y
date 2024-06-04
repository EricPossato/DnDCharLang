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
%token IDENTIFIER NUMBER STRING NOT READ

%type <str> IDENTIFIER STRING 
%type <num> NUMBER



%%

program: block {printf("Program parsed\n");}
       ;



block: statement_list {printf("block parsed\n");}
     ;

statement_list: /* empty */
              | statement_list statement {printf("statement parsed\n");}
              ;

statement: EOL
    | STAT_TYPE IDENTIFIER EOL
    | NARRATION_TYPE IDENTIFIER EOL
    | NARRATION_TYPE IDENTIFIER ASSIGN STRING EOL
    | IDENTIFIER ASSIGN rel_exp EOL
    | STAT_TYPE IDENTIFIER ASSIGN rel_exp EOL
    | SAY OPEN_PAR rel_exp CLOSE_PAR EOL {printf("say statement parsed\n");}
    | CHECK rel_exp EOL SUCCESS statement_list CONSEQUENCE EOL statement_list REST;
    | TURNS rel_exp ACTION EOL statement_list REST EOL
    ;


rel_exp:
    expression
    | expression DC_OP expression {printf("expression parsed\n");}
    ;

expression:
    term
    | term ADD_OP term
    | term SUB_OP term
    ;

term:
    factor
    | factor MUL_OP factor
    | factor DIV_OP factor
    ;

factor:
    NUMBER
    | STRING
    | IDENTIFIER
    | ADD_OP factor
    | SUB_OP factor
    | NOT factor
    | OPEN_PAR rel_exp CLOSE_PAR
    | READ OPEN_PAR CLOSE_PAR
    ;

%%

int yyerror(const char *msg) {
    fprintf(stderr, "Parser Error: %s\n", msg);
    return 0;
}

int main() {
    return yyparse();
}