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

    texts =['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print("Hello World");','print("The message is \"Hello World\"");',
    'print("The meaning of life is " @ 42);','print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));',
    'function tan(x) => sin(x) / cos(x);','function cot(x) => 1 / tan(x);function tan(x) => sin(x) / cos(x);print(tan(PI) ** 2 + cot(PI) ** 2);',
    'function operate(x, y) {print(x + y);print(x - y);print(x * y);print(x / y);}',
    'let msg = "Hello World" in print(msg);','let number = 42, text = "The meaning of life is" in print(text @ number);',
    'let number = 42 in let text = "The meaning of life is" in print(text @ number);',
    'let number = 42 in (let text = "The meaning of life is" in (print(text @ number)));',
    'let a = 6, b = a * 7 in print(b);','let a = 6 in let b = a * 7 in print(b);',
    'let a = 5, b = 10, c = 20 in {print(a+b);print(b*c);print(c/a);};','let a = (let b = 6 in b * 7) in print(a);',
    'print(let b = 6 in b * 7);','let a = 20 in {let a = 42 in print(a);print(a);};','let a = 7, a = 7 * 6 in print(a);',
    'let a = 7 in let a = 7 * 6 in print(a);','let a = 0 in {print(a);a := 1;print(a);};',
    'let a = 0 in let b = a := 1 in {print(a);print(b);};',
    'let a = 42 in if (a % 2 == 0) print("Even") else print("odd");',
    'while(5){print("hola");};',
    'while(x==1){print("hola");};',
    'if(5){print("hola");}else{print("la");};',
    'if(x==1){print("hola");}else{print("la");};'
    ]

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

    scope = Scope()

    for i in range(len(astlist)):

        semantic_checker = SemanticCheckerVisitor()
        errors = semantic_checker.visit(astlist[i])
        for j, error in enumerate(errors,1):
            print(texts[i])
            print(f'{j}.', error)

    #endregion
    

init()