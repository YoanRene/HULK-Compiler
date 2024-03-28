from Lexer import *
from ParserLR1 import *

def test_lexer():
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))

    print('Non-zero digits:', nonzero_digits)
    print('Letters:', letters)

    lexer = Lexer([
        ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
        ('for' , 'for'),
        ('foreach' , 'foreach'),
        ('space', '  *'),
        ('id', f'({letters})({letters}|0|{nonzero_digits})*')
    ], 'eof')

    text = '5465 for 45foreach fore'
    print(f'\n>>> Tokenizando: "{text}"')
    tokens = lexer(text)
    print(tokens)
    assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
    assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

    text = '4forense forforeach for4foreach foreach 4for'
    print(f'\n>>> Tokenizando: "{text}"')
    tokens = lexer(text)
    print(tokens)
    assert [t.token_type for t in tokens] == ['num', 'id', 'space', 'id', 'space', 'id', 'space', 'foreach', 'space', 'num', 'for', 'eof']
    assert [t.lex for t in tokens] == ['4', 'forense', ' ', 'forforeach', ' ', 'for4foreach', ' ', 'foreach', ' ', '4', 'for', '$']

def test_parser():
    G = Grammar()
    E = G.NonTerminal('E', True)
    A = G.NonTerminal('A')
    equal, plus, num = G.Terminals('= + int')

    E %=  A + equal + A | num
    A %= num + plus + A | num

    firsts = compute_firsts(G)
    firsts[G.EOF] = ContainerSet(G.EOF)

    item = Item(E.productions[0], 0, lookaheads=[G.EOF, plus])

    assert str(expand(G ,item, firsts)) == "[A -> .int+A, {'='}, A -> .int, {'='}]"

    closure = closure_lr1(G, [item, item.NextItem().NextItem()], firsts)

    expected = {
        Item(E.productions[0], 0, lookaheads=(plus, G.EOF)),
        Item(E.productions[0], 2, lookaheads=(plus, G.EOF)),
        Item(A.productions[0], 0, lookaheads=(plus, G.EOF, equal)),
        Item(A.productions[1], 0, lookaheads=(plus, G.EOF, equal)),
    }
    assert closure == expected

    goto = goto_lr1(G ,[item], A, firsts)
    assert  goto == {
        Item(E.productions[0], 1, lookaheads=(plus, G.EOF))
    }

    automaton = build_LR1_automaton(G.AugmentedGrammar())

    assert automaton.recognize('E')
    assert automaton.recognize(['A','=','int'])
    assert automaton.recognize(['int','+','int','+','A'])

    assert not automaton.recognize(['int','+','A','+','int'])
    assert not automaton.recognize(['int','=','int'])

    parser = LR1Parser(G, verbose=True)

    derivation = parser([num, plus, num, equal, num, plus, num, G.EOF])

    assert str(derivation) == '[A -> int, A -> int + A, A -> int, A -> int + A, E -> A = A]'

def test_parser_lexer():

    #lexeando

    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
    lexer = Lexer([
        ('num', f'({nonzero_digits})(0|{nonzero_digits})*'),
        ('for' , 'for'),
        ('foreach' , 'foreach'),
        ('space', '  *'),
        ('plus','+'),
        ('equal','='),
        ('id', f'({letters})({letters}|0|{nonzero_digits})*')
    ], 'eof')
    G= Grammar()

    #text = '5465 for 45foreach fore'

    text= '2+3=4+4'
    tokens = lexer(text)
    # assert [t.token_type for t in tokens] == ['num', 'space', 'for', 'space', 'num', 'foreach', 'space', 'id', 'eof']
    # assert [t.lex for t in tokens] == ['5465', ' ', 'for', ' ', '45', 'foreach', ' ', 'fore', '$']

    E = G.NonTerminal('E', True)
    A = G.NonTerminal('A')
    equal, plus, num , for_,foreach , id, space = G.Terminals('= + int for foreach id space')

    E %=  A + equal + A | num
    A %= num + plus + A | num

    types=[]

    ####NO#####

    for t in tokens:
        if t.token_type == 'num':
            types.append(num)
        elif t.token_type == 'for':
            types.append(for_)
        elif t.token_type == 'foreach':
            types.append(foreach)
        elif t.token_type == 'id':
            types.append(id)
        elif t.token_type == 'plus':
            types.append(plus)
        elif t.token_type == 'eof':
            types.append(G.EOF)
        elif t.token_type== 'equal':
            types.append(equal)
        else:
            types.append(space)

    ##########


    #parseando

    parser = LR1Parser(G, verbose=True)

    derivation = parser(types)

    print(str(derivation))

    #assert str(derivation) == '[A -> int, A -> int + A, A -> int, A -> int + A, E -> A = A]'

def test_hulk():

    lexer = Lexer([
        ('and','&'),
        ('space', '  *'),
        ('or','\|'),
        ('not','!'),
        ('true','True'),
        ('false','False'),
    ], 'eof')
    
    G=Grammar()
    boolean_expr =G.NonTerminal('boolean_expr',True)
    and_,or_,not_,true,false = G.Terminals('and or not true false')
    boolean_expr %= true
    boolean_expr %=false
    boolean_expr %= boolean_expr + and_ + boolean_expr
    boolean_expr %= boolean_expr + or_ + boolean_expr  
    boolean_expr %= not_ + boolean_expr

    text= 'True & False | ! True'

    tokens = lexer(text)
    for i in tokens:
        print(i.token_type)



def loop_grammar():
    G=Grammar()

    lexer = Lexer([
        ('for','for'),
        ('space', '  *'),
        ('while','while'),
        ('not','!'),
        ('true','True'),
        ('false','False'),
        ('left','\('),
        ('right','\)'),

    ], 'eof')

    program = G.NonTerminal('<program>', startSymbol=True)
    bool_expr = G.NonTerminal('<bool-expr>')
    expr = G.NonTerminal('<expr>')
    block_expr = G.NonTerminal('<block-expr>')
    conditional_expr, loop_expr = G.NonTerminals('<conditional-expr> <loop-expr>')
    while_loop, for_loop = G.NonTerminals('<while-loop> <for-loop>')

    # Terminals
    wloop, floop = G.Terminals('WHILE FOR') 
    boolx = G.Terminal('bool')
    eof = G.EOF

    # Productions
    program %= block_expr
    block_expr %= block_expr + expr
    block_expr %= expr
    expr %= bool_expr
    expr %=loop_expr
    expr %=conditional_expr
    bool_expr %= boolx
    loop_expr %= while_loop
    loop_expr %= for_loop
    while_loop %= wloop + boolx + block_expr
    for_loop %= floop + boolx + block_expr
    conditional_expr %= boolx + block_expr + block_expr

    text= 'while True for False'

    tokens = lexer(text)
    for i in tokens:
        print(i.token_type)


def test_grammar():
    #region Gramatica
    G = Grammar()
    program = G.NonTerminal('<program>', startSymbol=True)
    stat_list, stat = G.NonTerminals('<stat_list> <stat>')
    let_var, def_func, print_stat, arg_list = G.NonTerminals('<let-var> <def-func> <print-stat> <arg-list>')
    expr, term, factor, atom, power= G.NonTerminals('<expr> <term> <factor> <atom> <power>')
    func_call, expr_list, expr_str = G.NonTerminals('<func-call> <expr-list> <expr-str>')


    let, defx, printx = G.Terminals('let def print')
    sqrt, sin, cos, tan, log, exp, rand = G.Terminals('sqrt sin cos tan log exp rand')
    semi, comma, opar, cpar, arrow = G.Terminals('; , ( ) ->')
    equal, plus, minus, star, div, pow, arroba = G.Terminals('= + - * / ^ @') #######
    idx, num, string_ = G.Terminals('id int str')

    # Productions

    program %= stat_list#, lambda h,s: ProgramNode(s[1])

    stat_list %= stat + semi#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    stat_list %= stat + semi + stat_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

    stat %= let_var#, lambda h,s: s[1] # Your code here!!! (add rule)
    stat %= def_func#, lambda h,s: s[1] # Your code here!!! (add rule)
    stat %= print_stat#, lambda h,s: s[1] # Your code here!!! (add rule)
    stat %= expr_str

    let_var %= let + idx + equal + expr#, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)

    def_func %= defx + idx + opar + arg_list + cpar + arrow + expr#, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7]) # Your code here!!! (add rule)

    expr_str %= expr_str + arroba + expr#, lambda h,s: ConcatNode(s[1],s[3]) # Your code here!!! (add rule)
    expr_str %= expr_str + arroba + string_
    expr_str %= string_
    expr_str %= expr#, lambda h,s: s[1] # Your code here!!! (add rule)

    print_stat %= printx + opar + expr_str + cpar#, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)
    #print_stat %= printx + opar + string_ + cpar#, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)

    arg_list %= idx#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    arg_list %= idx + comma + arg_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

    expr %= expr + plus + term#, lambda h,s: PlusNode(s[1],s[3]) # Your code here!!! (add rule)
    expr %= expr + minus + term#, lambda h,s: MinusNode(s[1],s[3]) # Your code here!!! (add rule)
    expr %= term#, lambda h,s: s[1] # Your code here!!! (add rule)

    term %= term + star + power#, lambda h,s: StarNode(s[1],s[3]) # Your code here!!! (add rule)
    term %= term + div + power#, lambda h,s: DivNode(s[1],s[3]) # Your code here!!! (add rule)
    term %= power#, lambda h,s: s[1] # Your code here!!! (add rule)

    power %= power + pow + factor#, lambda h,s: PowNode(s[1],s[3]) # Your code here!!! (add rule)
    power %= factor#, lambda h,s: s[1] # Your code here!!! (add rule)
    
    factor %= atom#, lambda h,s: s[1] # Your code here!!! (add rule)
    factor %= opar + expr + cpar#, lambda h,s: s[2] # Your code here!!! (add rule)
    

    atom %= num#, lambda h,s: ConstantNumNode(s[1]) # Your code here!!! (add rule)
    atom %= idx#, lambda h,s: VariableNode(s[1]) # Your code here!!! (add rule)
    atom %= func_call#, lambda h,s: s[1] # Your code here!!! (add rule)
    atom %= sqrt + opar + expr + cpar#, lambda h,s: SqrtNode(s[3]) # Your code here!!! (add rule)
    atom %= sin + opar + expr + cpar#, lambda h,s: SinNode(s[3]) # Your code here!!! (add rule)
    atom %= cos + opar + expr + cpar#, lambda h,s: CosNode(s[3]) # Your code here!!! (add rule)
    atom %= tan + opar + expr + cpar#, lambda h,s: TanNode(s[3]) # Your code here!!! (add rule)
    atom %= log + opar + expr + comma + expr + cpar#, lambda h,s: LogNode(s[3]) # Your code here!!! (add rule)
    atom %= exp + opar + expr + cpar#, lambda h,s: ExpNode(s[3]) # Your code here!!! (add rule)
    atom %= rand + opar + cpar#, lambda h,s: RandNode() # Your code here!!! (add rule)


    func_call %= idx + opar + expr_list + cpar#, lambda h,s: CallNode(s[1], s[3]) # Your code here!!! (add rule)

    expr_list %= expr#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    expr_list %= expr + comma + expr_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

    #endregion
    #region Lexer
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
    letters = letters +'|'+'|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))  
    symbols="!|@|%|^|&|\\*|_|+|-|/|:|;|<|>|=|,|.|?|~|`|\\(|\\)|[|]|{|}|#|'|\\||¿|¡|º|ª|¬"
    vari = f'\\"({letters}|{nonzero_digits}|{symbols}| |\\")*\\"'
    lexer = Lexer([
        ('space', '  *'),
        (string_, vari),
        (semi,';'),
        (comma,','),
        (plus,plus.Name),
        (minus,minus.Name),
        (opar,'\\'+opar.Name),
        (cpar,'\\'+cpar.Name),
        (let,let.Name),
        (equal,equal.Name),
        (star,'\\'+star.Name),
        (div,div.Name),
        (pow,pow.Name),
        (arrow,arrow.Name),
        (defx,defx.Name),
        (printx,printx.Name),
        (sqrt,sqrt.Name),
        (sin,sin.Name),
        (cos,cos.Name),
        (tan,tan.Name),
        (log,log.Name),
        (exp,exp.Name),
        (arroba,arroba.Name),
        (rand,rand.Name),
        (num, f'({nonzero_digits})(0|{nonzero_digits})*'),
        (idx, f'({letters})({letters}|0|{nonzero_digits})*')
    ],G.EOF)
    #endregion
    
    #Expressions
    texts =['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print( "Hello :is+ the@  World" );',
            'print("The message is \"Hello World\"");','print("The meaning of life is " @ 42);',
            'print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));' ,
            'print(42); print(sin(PI/2)); print("Hello World");' ]

    parser=LR1Parser(G)
    c=0
    for i in texts:
        c+=1
        if c==8: 
            print(i)
        tokens = lexer(i)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parsed=parser(tokens_type)
        assert parsed!=None


   

   









    

#test_lexer()

#test_parser()
#test_parser_lexer()
#test_hulk()
#loop_grammar()
test_grammar()