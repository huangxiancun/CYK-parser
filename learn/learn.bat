win_bison -d parse.y
win_flex word.lex
gcc -o learn parse.tab.c lex.yy.c -std=c99
learn.exe
