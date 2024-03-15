%{
#include <stdio.h>
%}

%token NUMBER
%left '+' '-'
%left '*' '/'

%%

expression : expression '+' expression
           | expression '-' expression
           | expression '*' expression
           | expression '/' expression
           | '(' expression ')'
           | NUMBER
           ;

%%

int yyerror(char *s) {
    printf("Parser Error: %s\n", s);
    return 0;
}

int yylex(void) {
    int c = getchar();
    if (c == EOF) return 0;
    if (c == '+' || c == '-' || c == '*' || c == '/' || c == '(' || c == ')') return c;
    if (c >= '0' && c <= '9') {
        yylval = c - '0';
        while ((c = getchar()) >= '0' && c <= '9') {
            yylval = yylval * 10 + (c - '0');
        }
        ungetc(c, stdin);
        return NUMBER;
    }
    return 0;
}

int main() {
    yyparse();
    return 0;
}

/* yacc -d parser.y
gcc -o parser y.tab.c -ly -lm
./parser 
-------
lex lexer.l
gcc -o parser y.tab.c lex.yy.c -ll
./parser
*/
