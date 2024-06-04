/* A Bison parser, made by GNU Bison 3.8.2.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2021 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <https://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* DO NOT RELY ON FEATURES THAT ARE NOT DOCUMENTED in the manual,
   especially those whose name start with YY_ or yy_.  They are
   private implementation details that can be changed or removed.  */

#ifndef YY_YY_PARSER_TAB_H_INCLUDED
# define YY_YY_PARSER_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token kinds.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    YYEMPTY = -2,
    YYEOF = 0,                     /* "end of file"  */
    YYerror = 256,                 /* error  */
    YYUNDEF = 257,                 /* "invalid token"  */
    STAT_TYPE = 258,               /* STAT_TYPE  */
    NARRATION_TYPE = 259,          /* NARRATION_TYPE  */
    SAY = 260,                     /* SAY  */
    TURNS = 261,                   /* TURNS  */
    ACTION = 262,                  /* ACTION  */
    CHECK = 263,                   /* CHECK  */
    SUCCESS = 264,                 /* SUCCESS  */
    CONSEQUENCE = 265,             /* CONSEQUENCE  */
    REST = 266,                    /* REST  */
    DC_OP = 267,                   /* DC_OP  */
    EOL = 268,                     /* EOL  */
    OPEN_PAR = 269,                /* OPEN_PAR  */
    CLOSE_PAR = 270,               /* CLOSE_PAR  */
    ADD_OP = 271,                  /* ADD_OP  */
    SUB_OP = 272,                  /* SUB_OP  */
    MUL_OP = 273,                  /* MUL_OP  */
    DIV_OP = 274,                  /* DIV_OP  */
    ASSIGN = 275,                  /* ASSIGN  */
    IDENTIFIER = 276,              /* IDENTIFIER  */
    NUMBER = 277,                  /* NUMBER  */
    STRING = 278,                  /* STRING  */
    NOT = 279,                     /* NOT  */
    READ = 280                     /* READ  */
  };
  typedef enum yytokentype yytoken_kind_t;
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 9 "parser.y"

    char *str;
    int num;

#line 94 "parser.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;


int yyparse (void);


#endif /* !YY_YY_PARSER_TAB_H_INCLUDED  */
