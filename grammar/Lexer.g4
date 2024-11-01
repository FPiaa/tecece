lexer grammar Lexer;

WS: [ \t\n\r]+ -> skip;

BOOLEAN: 'True' | 'False';
IDENTIFIER: LETTER (LETTER | DIGIT | '_')*;
NUMBER: DIGIT+;

fragment DIGIT: [0-9];
fragment LETTER: [a-zA-Z];
ESCAPED_STR: '\'' .*? '\'';

fragment SEPARATOR: ';';