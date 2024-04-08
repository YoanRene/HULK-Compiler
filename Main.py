from HulkGrammar import *
from Automata import *
from Lexer import *
from Parser import *
from Grammar import *
from ParserLR1 import *
from Regex import *
from Semantic_checker import *
from Visitor import *
from ParserSLR1 import *

def init():

    G,lexer= HulkGrammar()
    parser = SLR1Parser(G,True)

    texts =['let a = 5 in {a; print(9+a); };']

    parserslist = []
    operationslist=[]
    tokenslist = []

    for i in texts:
        tokens = lexer(i)
        tokenslist.append(tokens)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parse,operations = parser(tokens_type, get_shift_reduce=True)
        parserslist.append(parse)
        operationslist.append(operations)

    astlist = []

    for j in range(len(parserslist)):
        new_tokens = []

        for i in tokenslist[j]:
            if(i.token_type!='space'):
                new_tokens.append(i)

        #region Semantic Checker
        ast = evaluate_reverse_parse(parserslist[j], operationslist[j], new_tokens)
        astlist.append(ast)


    formatter = FormatVisitor()
    for i in range(len(astlist)):
        print(formatter.visit(astlist[i]))


    print('Semantic Checker')
    for i in range(len(astlist)):

        semantic_checker = SemanticCheckerVisitor()
        errors = semantic_checker.visit(astlist[i])
        for j, error in enumerate(errors,1):
            print(texts[i])
            print(f'{j}.', error)

    #endregion
    
    for i in range(len(astlist)):
        semantic_checker = SemanticCheckerEvaluate()
        results = semantic_checker.visit(astlist[i])
        print(results)
        # for j, res in enumerate(results,1):
        #     print(texts[i])
        #     print(f'{j}.', res)

init()