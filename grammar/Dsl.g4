grammar Dsl;
import Lexer;

prog: ('given' knowledge)? ('where' conditions)?;

knowledge: use (',' use)*;
use: belief
    | goal;
belief: modifier? 'B' structure;
goal: modifier? 'G' structure;
modifier: '-' | '~' | '+';

structure: IDENTIFIER ('(' structure_elements?  ')')? source?;
structure_elements: elements (',' elements)*;
source: 'from' IDENTIFIER;

elements: BOOLEAN
    | NUMBER
    | bind
    | '_';

bind: IDENTIFIER;

function_call: function_path '(' function_params? ')';
function_path: IDENTIFIER ('.' IDENTIFIER)*;
function_params: expr (',' expr)* ;

conditions: condition_list?;
condition_list: condition (',' condition)*;

condition: log_expr
    | pattern_match_expr
    | pattern_match_tuple;

pattern_match_expr: log_expr 'is' pattern ('|' pattern)*;
pattern_match_tuple: tuple 'is' tuple ('|' tuple)*;
//
pattern: pattern 'and' pattern
    | '!=' rel_expr
    | op=('<' | '<=' | '>=' | '>') rel_expr
    | rel_expr
    | array_pattern
    | range_pattern
    | inclusive_range_pattern;

array_pattern: '[' (pattern ',')* ('*' bind?)? (',' pattern)* ']';
range_pattern: expr '..' expr;
inclusive_range_pattern: expr '..=' expr;

tuple: '(' tuple_params ')';
tuple_params: ((log_expr | tuple) ',')+ (log_expr | tuple)?;
tuple_pattern: '(' tuple_pattern_params')';
tuple_pattern_params: ((tuple_pattern | pattern) ',')+ (tuple_pattern | pattern)?;

log_expr: 'not' log_expr
    | log_expr 'and' log_expr
    | log_expr 'or' log_expr
    | '(' log_expr ')'
    | rel_expr;


rel_expr: arith_expr op=('=' | '!=') rel_expr
    | arith_expr op=('<' | '>' | '<=' | '>=') rel_expr
    | arith_expr;

arith_expr: <assoc=right> '-' expr
    | arith_expr '**' arith_expr
    | arith_expr op=('*' | '/') arith_expr
    | arith_expr op=('+' | '-') arith_expr
    | NUMBER
    | IDENTIFIER
    | ESCAPED_STR;

//arith_expr: arith_term '+' arith_expr
//    | arith_term '-' arith_expr
//    | arith_term;
//
//arith_term: arith_factor '*' arith_term
//                | arith_factor '/' arith_term
//                | arith_factor;
//arith_factor: arith_simple ('**' arith_simple)?;
//arith_simple: NUMBER
//    | IDENTIFIER
//    | '-' arith_simple
//    | '(' arith_expr ')';

expr: <assoc=right> ('!' | '-') expr
    | expr op=('*' | '/') expr
    | expr op=('+' | '-') expr
    | expr op=('=' | '!=') expr
    | expr op=('<' | '<=' | '>=' | '>') expr
    | expr 'and' expr
    | expr 'or' expr
    | expr '[' expr ']'
    | expr '.' expr
    | '(' expr ')'
    | function_call
    | IDENTIFIER '.' function_call
    | IDENTIFIER ':=' expr
    | IDENTIFIER
    | BOOLEAN
    | ESCAPED_STR
    | NUMBER
    | '_';
