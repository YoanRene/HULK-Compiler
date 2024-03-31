from HulkGrammar import *
from Automata import *
from Lexer import *
from Parser import *
from Grammar import *
from ParserLR1 import *
from Regex import *
from Semantic_checker import *
from Visitor import *

def init():

    G,lexer= HulkGrammar()
    parser = LR1Parser(G)

    texts=[''] #Text to be parsed

    for i in texts:
        tokens = lexer(i)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parse,operations = parser(tokens_type, get_shift_reduce=True)

    #region Semantic Checker
    # ast = evaluate_reverse_parse(parse, operations, tokens)

    # formatter = FormatVisitor()
    # print(formatter.visit(ast))

    # scope = Scope()

    # semantic_checker = SemanticCheckerVisitor()
    # errors = semantic_checker.visit(ast)
    # for i, error in enumerate(errors,1):
    #     print(f'{i}.', error)

    #endregion
    

