lexer grammar Lexer;

WS: [ \t\n\r]+ -> skip;
IDENTIFIER: LETTER (LETTER | DIGIT | '_')*;

BOOLEAN: 'true' | 'false';
NUMBER: DIGIT+;

fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];
ESCAPED_STR : '\'' .*? '\'';

fragment SEPARATOR: ';';