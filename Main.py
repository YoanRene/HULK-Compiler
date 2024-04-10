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


    #region Inicialization of the grammar

    G,lexer= HulkGrammar()
    parser = SLR1Parser(G,True)


    #Pruebas sin errores

    texts=['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print("Hello World");','print("The message is \"Hello World\"");',
    'print("The meaning of life is " @ 42);','print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));',
    'function tan(x) => sin(x) / cos(x);',
    'function operate(x, y) {print(x + y);print(x - y);print(x * y);print(x / y);}',
    'let ifmsg = "Hello World" in print(ifmsg);','let number = 42, text = "The meaning of life is" in print(text @ number);',
    'let number = 42 in let text = "The meaning of life is" in print(text @ number);',
    'let number = 42 in (let text = "The meaning of life is" in (print(text @ number)));',
    'let a = 6, b = a * 7 in print(b);','let a = 6 in let b = a * 7 in print(b);',
    'let a = 5, b = 10, c = 20 in {print(a+b);print(b*c);print(c/a);};','let a = (let b = 6 in b * 7) in print(a);',
    'print(let b = 6 in b * 7);','let a = 20 in {let a = 42 in print(a);print(a);};','let a = 7, a = 7 * 6 in print(a);',
    'let a = 7 in let a = 7 * 6 in print(a);','let a = 0 in {print(a);a := 1;print(a);};',
    'let a = 42 in if (a % 2 == 0) print("Even") else print("odd");',
    'if(5>4){print("es mayor");}else{print("es menor");};',
    'let a=2 in while(a<5){print(a);a:=a+1;};',
    'let b=[1,2,3,4,5] in for(i in b){print(i);};',
    'function tan(x) {sin(x) / cos(x);} tan(23);',
    'function lala(x) {print(x);print(x+1);} lala(5);',
    'let a=2,b=3 in if(a<b & a!=5){print("hola");}else{print("adios");};'
    ]

    #Pruebas con errores


    # texts=['while(5){print("hola");};',
    # 'if(5){print("hola");}else{print("la");};',
    # ' 5 + (b & c);',
    # '(200< sqrt(25)) + 20;',
    # 'let a=2 in if(a<3){print("hola");}elif(4){print("adios");} else{print("hola");};'
    # ]
    

    #endregion

    #region Parsing
    parserslist = []
    operationslist=[]
    tokenslist = []

    for i in texts:
        l=1
        lines=[]
        tokens = lexer(i)
        tokenslist.append(tokens)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space' and j.token_type!='line':
                tokens_type.append(j.token_type)
                lines.append(l)
            if j.token_type=='line':
                l+=1
        parse,operations = parser(tokens_type, lines, get_shift_reduce=True)
        parserslist.append(parse)
        operationslist.append(operations)

    #endregion

    #region Semantic Checker

    astlist = []

    for j in range(len(parserslist)):
        new_tokens = []

        for i in tokenslist[j]:
            if(i.token_type!='space' and i.token_type!='line'):
                new_tokens.append(i)
        ast = evaluate_reverse_parse(parserslist[j], operationslist[j], new_tokens)
        astlist.append(ast)
     
    print("AST: \n")

    formatter = FormatVisitor()
    for i in range(len(astlist)):
        print(formatter.visit(astlist[i]))

    print("\n")

    print("Semantic Checker Errors: \n")

    for i in range(len(astlist)):
        print(texts[i])

        semantic_checker = SemanticCheckerVisitor()
        errors = semantic_checker.visit(astlist[i])
        for j, error in enumerate(errors,1):
            
            print(f'{j}.', error)

    #endregion
    
    #region Semantic Checker Evaluate

    print("\nSemantic Checker Evaluate: \n")
    
    for i in range(len(astlist)):
        print(texts[i]+" : \n")
        semantic_checker = SemanticCheckerEvaluate()
        results = semantic_checker.visit(astlist[i])
        results=semantic_checker.results
        for j, res in enumerate(results,1):
            if(res != None):
                print(res)
        print ("\n")
    #endregion

init()