%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
%}

%union {
    char *str;
    int num;
}

%token STAT MODIFY SAY TURNS CHECK FAIL SUCCESS CONSEQUENCE REST
%token IDENTIFIER NUMBER PLUS MINUS DC COLON LPAREN RPAREN COMMA SEMICOLON

%%

block: '{' statements '}' { printf("Block parsed.\n"); }
     ;

statements: /* empty */
          | statements statement '\n'
          ;

statement: assignment
         | modify
         | say
         | turns
         | check
         ;

assignment: STAT IDENTIFIER rel_exp { printf("Assignment statement parsed.\n"); }
          ;

modify: MODIFY IDENTIFIER PLUS term
      | MODIFY IDENTIFIER MINUS term
      ;

say: SAY LPAREN rel_exp RPAREN { printf("Say statement parsed.\n"); }
   ;

rel_exp: term
       | term DC term { printf("Relational expression parsed.\n"); }
       ;

check: FAIL check
      | CHECK IDENTIFIER DC term '\n' SUCCESS '{' statements '}' CONSEQUENCE '\n' '{' statements '}' REST { printf("Check statement parsed.\n"); }
      ;

turns: TURNS IDENTIFIER term COLON term '\n' '{' statements '}' REST { printf("Turns statement parsed.\n"); }
     ;

term: NUMBER
    | IDENTIFIER
    ;

%%

int yyerror(const char *msg) {
    fprintf(stderr, "Parser Error: %s\n", msg);
    return 0;
}

int main() {
    yyparse();
    return 0;
}
