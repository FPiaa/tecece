grammar Dsl;
import Lexer;

plan: trigger (':' conditions)?;

trigger: knowledge;

knowledge: belief # knowledgeBelief | goal # knowledgeGoal;

belief: modifier? 'B' structure;
goal: modifier? 'G' structure;
modifier: '-' | '+';

structure: IDENTIFIER ('(' structure_elements? ')')? source?;
structure_elements: elements (',' elements)*;
source: '[' IDENTIFIER ']';

elements: log_expr # exprElement | '_' # anyElement;

function_params: log_expr (',' log_expr)*;

conditions: condition_list?;
condition_list: condition (',' condition)*;

condition:
	knowledge	# knowledgeCondition
	| log_expr	# exprCondition;

log_expr:
	'not' log_expr			# logical_not
	| log_expr '&' log_expr	# logical_and
	| log_expr '|' log_expr	# logical_or
	| rel_expr				# log_to_rel;

rel_expr:
	rel_expr op = ('<' | '>' | '<=' | '>=' | '=' | '!=') rel_expr	# rel_comparison
	| arith_expr													# rel_to_arith;

arith_expr:
	arith_expr '**' arith_expr						# exp_expr
	| <assoc = right> op = ('-' | '+') arith_expr	# unary_expr
	| arith_expr op = ('*' | '/' | '%') arith_expr	# mult_expr
	| arith_expr op = ('+' | '-') arith_expr		# sum_expr
	| primary										# expr_to_primary;

primary:
	primary '.' IDENTIFIER				# primary_path
	| primary '(' function_params? ')'	# primary_call
	| primary '[' log_expr ']'			# primary_index
	| '(' IDENTIFIER ':=' log_expr ')'	# primary_walrus
	| atom								# primary_to_atom;

atom:
	NUMBER				# atomNumber
	| IDENTIFIER		# atomIdent
	| BOOLEAN			# atomBool
	| 'None'			# atomNone
	| tuple				# atomTuple
	| array				# atomArray
	| dict				# atomDict
	| '(' log_expr ')'	# atomParen
	| ESCAPED_STR		# atomStr;

tuple: '(' tuple_params ')';
tuple_params: (log_expr ',')+ log_expr?;

array: '[' array_params? ']';
array_params: (log_expr ',')* log_expr;

dict: '{' dict_params '}';
dict_params: (dict_pair ',')* dict_pair;
dict_pair: log_expr ':' log_expr;