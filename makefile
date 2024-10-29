build_grammar: 
	antlr4 -Dlanguage=Python3 -o dsl/ -visitor -no-listener grammar/Dsl.g4