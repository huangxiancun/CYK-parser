%{	/*parse.y
	 *自然语言处理导论 作业2
	 *作者：于涵霖
	 *编译工具：win_bison+gcc
	 */
#include <stdio.h>
#include <ctype.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#define YYSTYPE char *
extern FILE *yyin;

%}
%token TOKEN LP RP
%start F
%%
F:S|F S
S:LP TOKEN C RP{
	$$=strdup($2);
	printf("%s->%s\n",$2,$3);
	free($2); free($3);
	//printf("S->(%s C)\n",$$);
}
|LP S RP {
	$$=strdup($2);
	free($2);
	//printf("S->(S)\n");
}

C:TOKEN {
	$$=strdup($1);
	free($1);
	//printf("C->%s\n",$$);*/
}
|X {
	$$=strdup($1);
	free($1);
	//printf("C->X\n");
}

X:S {
	//printf("X->S\n");
	$$=strdup($1);
	free($1);
}
|X S {	
	int len=strlen($1)+strlen($2)+2;
	int len1=strlen($1);
	$$=strdup($1);
	$$=(char*)realloc($$,len*sizeof(char));
	$$[len1]=' ';
	$$[len1+1]=0;
	strcat($$,$2);
	//printf("X->XS\n");
	free($1); free($2);
}

%%

int yyerror(char *msg){
	printf("Error: %s \n", msg);
}

int main(int argc,char** argv){
	if(argc > 1)
        yyin = fopen(argv[1], "r");
    else
        yyin = stdin;
	return yyparse();
}