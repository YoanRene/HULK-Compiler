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
    A, B = G.NonTerminals('A B')
    equal, plus, num = G.Terminals('= + int')

    E %=  A + equal + A | A
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
#test_parser()

def test_grammar():
    #region Gramatica

    G = Grammar()
    # Non-Terminals
    program = G.NonTerminal('program', startSymbol=True)
    stat_list, stat, expr_list = G.NonTerminals('<stat_list> <stat> <expr-list>')
    asign_list, destr_expr, asign, def_func, print_expr, arg_list = G.NonTerminals('<asign-list> <destr-expr> <asignment> <def-func> <print-expr> <arg-list>')
    expr, term, factor, atom, power= G.NonTerminals('<expr> <term> <factor> <atom> <power>')
    func_call, block, elem_expr, not_expr, compare_expr = G.NonTerminals('<func-call> <block-expr> <logic-exp> <not-exp> <compare-expr>')
    elem_expr = G.NonTerminal('<elem-expr>')
    concat_expr, aritm_expr, let_expr,args_evaluated = G.NonTerminals('<concat-expr> <aritm-expr> <let-expr> <args-evaluated>')

    # Terminals
    let, function_, printx, in_ = G.Terminals('let function print in')
    sqrt, sin, cos, log, exp, rand = G.Terminals('sqrt sin cos log exp rand')
    semi, comma, opar, cpar, arrow, okey, ckey= G.Terminals('; , ( ) => { }')
    equal, plus, minus, star, div, pow, arroba, pow_star, destr = G.Terminals('= + - * / ^ @ ** :=') #######
    greater, less, equals, not_equals, greater_equals, less_equals, and_, or_, not_, true, false = G.Terminals('> < == != >= <= & \\| ! true false')
    id_, num, string_ = G.Terminals('id num str')


    # Productions
    program %= stat_list #, lambda h,s: ProgramNode(s[1])
    program %= expr_list#, lambda h,s: ProgramNode(s[1] + s[2])

    stat_list %= stat + semi#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    stat_list %= stat + semi + stat_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)
    
    stat %= def_func#, lambda h,s: s[1] # Your code here!!! (add rule)
    
    def_func %= function_ + id_ + opar + arg_list + cpar + arrow + expr#, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7]) # Your code here!!! (add rule)
    def_func %= function_ + id_ + opar + arg_list + cpar + block#, lambda h,s: FuncDeclarationNode(s[2], s[4], s[6]) # Your code here!!! (add rule)
    
    arg_list %= id_#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    arg_list %= id_ + comma + arg_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)
    
    block %= okey + expr_list + ckey#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)

    expr_list %= expr + semi#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    expr_list %= expr + semi + expr_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

    expr %= print_expr
    expr %= destr_expr
    expr %= let_expr
    expr %= elem_expr
    
    print_expr %= printx + opar + expr + cpar#, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)

    destr_expr %= id_ + destr + expr#, lambda h,s: AsignNode(s[1], s[3]) # Your code here!!! (add rule)

    let_expr %= let + asign_list + in_ + expr#, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)
    let_expr %= let + asign_list + in_ + block#, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)

    asign_list %= asign + comma + asign_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)
    asign_list %= asign#, lambda h,s: s[1] # Your code here!!! (add rule)

    asign %= id_ + equal + expr#, lambda h,s: AsignNode(s[1],s[3]) # Your code here!!! (add rule)
    
    elem_expr %= elem_expr + and_ + compare_expr#, lambda h,s: AndNode(s[1],s[3]) # Your code here!!! (add rule)
    elem_expr %= elem_expr + or_ + compare_expr#, lambda h,s: OrNode(s[1],s[3]) # Your code here!!! (add rule)
    elem_expr %= not_ + compare_expr#, lambda h,s: s[1] # Your code here!!! (add rule)
    elem_expr %= compare_expr

    compare_expr %= compare_expr + equals + concat_expr
    compare_expr %= compare_expr + not_equals + concat_expr
    compare_expr %= compare_expr + greater_equals + concat_expr
    compare_expr %= compare_expr + greater + concat_expr
    compare_expr %= compare_expr + less + concat_expr
    compare_expr %= compare_expr + less_equals + concat_expr
    compare_expr %= concat_expr

    concat_expr %= concat_expr + arroba + aritm_expr#, lambda h,s: ConcatNode(s[1],s[3]) # Your code here!!! (add rule)
    concat_expr %= aritm_expr#, lambda h,s: s[1] # Your code here!!! (add rule)

    aritm_expr %= aritm_expr + plus + term#, lambda h,s: PlusNode(s[1],s[3]) # Your code here!!! (add rule)
    aritm_expr %= aritm_expr + minus + term#, lambda h,s: MinusNode(s[1],s[3]) # Your code here!!! (add rule)
    aritm_expr %= term#, lambda h,s: s[1] # Your code here!!! (add rule)

    term %= term + star + power#, lambda h,s: StarNode(s[1],s[3]) # Your code here!!! (add rule)
    term %= term + div + power#, lambda h,s: DivNode(s[1],s[3]) # Your code here!!! (add rule)
    term %= power#, lambda h,s: s[1] # Your code here!!! (add rule)

    power %= power + pow_star + factor#, lambda h,s: PowNode(s[1],s[3]) # Your code here!!! (add rule)
    power %= power + pow + factor#, lambda h,s: PowNode(s[1],s[3]) # Your code here!!! (add rule)
    power %= factor#, lambda h,s: s[1] # Your code here!!! (add rule)

    factor %= atom#, lambda h,s: s[1] # Your code here!!! (add rule)
    factor %= opar + expr + cpar#, lambda h,s: s[2] # Your code here!!! (add rule)
    
    atom %= string_#, lambda h,s: StringNode(s[1]) # Your code here!!! (add rule)
    atom %= true#, lambda h,s: TrueNode() # Your code here!!! (add rule)
    atom %= false#, lambda h,s: FalseNode() # Your code here!!! (add rule)
    atom %= num#, lambda h,s: ConstantNumNode(s[1]) # Your code here!!! (add rule)
    atom %= id_#, lambda h,s: VariableNode(s[1]) # Your code here!!! (add rule)
    atom %= sqrt + opar + expr + cpar#, lambda h,s: SqrtNode(s[3]) # Your code here!!! (add rule)
    atom %= sin + opar + expr + cpar#, lambda h,s: SinNode(s[3]) # Your code here!!! (add rule)
    atom %= cos + opar + expr + cpar#, lambda h,s: CosNode(s[3]) # Your code here!!! (add rule)
    atom %= log + opar + expr + comma + expr + cpar#, lambda h,s: LogNode(s[3]) # Your code here!!! (add rule)
    atom %= exp + opar + expr + cpar#, lambda h,s: ExpNode(s[3]) # Your code here!!! (add rule)
    atom %= rand + opar + cpar#, lambda h,s: RandNode() # Your code here!!! (add rule)
    atom %= func_call#, lambda h,s: s[1] # Your code here!!! (add rule)

    func_call %= id_ + opar + args_evaluated + cpar#, lambda h,s: CallNode(s[1], s[3]) # Your code here!!! (add rule)

    args_evaluated %= expr + comma + args_evaluated#, lambda h,s: [s[1]] + s[2] # Your code here!!! (add rule)
    args_evaluated %= expr#, lambda h,s: [s[1]] # Your code here!!! (add rule)


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
        (equal,equal.Name),
        (star,'\\'+star.Name),
        (div,div.Name),
        (pow,pow.Name),
        (pow_star,'\\'+pow_star.Name+'\\'+pow_star.Name),
        (greater,greater.Name),
        (less,less.Name),
        (greater_equals,greater_equals.Name),
        (less_equals,less_equals.Name),
        (equals,equals.Name),
        (not_equals,not_equals.Name),
        (and_,and_.Name),
        (or_,or_.Name),
        (not_,not_.Name),
        (true,true.Name),
        (false,false.Name),
        (function_,function_.Name),
        (arrow,arrow.Name),
        (function_,function_.Name),
        (printx,printx.Name),
        (let,let.Name),
        (in_,in_.Name),
        (sqrt,sqrt.Name),
        (sin,sin.Name),
        (cos,cos.Name),
        (log,log.Name),
        (exp,exp.Name),
        (destr,destr.Name),
        (arroba,arroba.Name),
        (rand,rand.Name),
        (okey,okey.Name),
        (ckey,ckey.Name),
        (num, f'({nonzero_digits})(0|{nonzero_digits})*|0'),
        (id_, f'({letters})({letters}|0|{nonzero_digits})*')
    ],G.EOF)
    #endregion
    
    #Expressions Functions Variables
    texts =['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print( "Hello :is+ the@  World" );',
            'print("The message is \"Hello World\"");','print("The meaning of life is " @ 42);',
            'print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));' ,
            '{print(42); print(sin(PI/2)); print("Hello World");}','function tan(x) => sin(x) / cos(x);',
            'function cot(x) => 1 / tan(x);function tan(x) => sin(x) / cos(x);print(tan(PI) ** 2 + cot(PI) ** 2);',
            'function operate(x, y) { print(x + y);print(x - y);print(x * y);print(x / y);}',
            'let msg = "Hello World" in print(msg);',
            'let number = 42, text = "The meaning of life is" in print(text @ number);',
            'let number = 42 in let text = "The meaning of life is" in print(text @ number);',
            'let a = (let b = 6 in b * 7) in print(a);',
            'let a = 5, b = 10, c = 20 in {print(a+b); print(b*c); print(c/a);}',
            'let a = (let b = 6 in b * 7) in print(a);',
            'print(let b = 6 in b * 7);',
            'let a = 20 in {let a = 42 in print(a);print(a);}',
            'let a = 7, a = 7 * 6 in print(a);',
            'let a = 7 in let a = 7 * 6 in print(a);',
            'let a = 0 in { print(a); a := 1; print(a);}',
            'let a = 0 in let b = a := 1 in { print(a);print(b);};',
            'true & false;',
            'a | b & !(1 <= 2 & 5); '

        ]

    parser=LR1Parser(G)
    c=0
    for i in texts:
        c+=1
        if c==len(texts): 
            print(i)
        tokens = lexer(i)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parsed=parser(tokens_type)
        assert parsed!=None


def hulk_grammar():
    G = Grammar()
    program = G.NonTerminal('<program>',True)
    expr, statment_list, stat, inline_function, block_function = G.NonTerminals('<expr> <statment_list> <stat> <inline_function> <block_function>')
    num_expr, term, factor, constant = G.NonTerminals('<num_expr> <term> <factor> <constant>')
    boolean_expr, boolean_term = G.NonTerminals('<boolean_expr> <boolean_term>')
    print_expr = G.NonTerminal('<print_expr>')
    let_expr, assign_list, assign = G.NonTerminals('<let_expr> <assign_list> <assign>')
    destruct_expr, dest = G.NonTerminals('<destruct_expr> <dest>')
    comparative_operator = G.NonTerminal('<comparative_operator>')
    comparable_expr = G.NonTerminal('<comparable_expr>')
    str_expr = G.NonTerminal('<str_expr>')
    math_function = G.NonTerminal('<math_function>')
    function_call, params_list = G.NonTerminals('<function_call> <params_list>')

    function_ = G.Terminal('function')
    opar, cpar, okey, ckey, id_, arrow, semi, comma = G.Terminals(' ( ) { } id => ; ,')

    true_, false_ = G.Terminals('true false')
    and_, or_, not_ = G.Terminals('& \\| !')
    equals, not_equals, greater, less, greater_equals, less_equals = G.Terminals('== != > < >= <=')

    plus, minus, star, div, power = G.Terminals(' + - * / ^')
    sqrt, sen, cos, log, exp = G.Terminals('sqrt sin cos log exp')
    num, euler, pi = G.Terminals('num Euler Pi')
    str_, concat, print_ = G.Terminals('str @ print')
    equal, in_, let, dest_op = G.Terminals('= in let :=')

    block_list, block_expr, expr_list = G.NonTerminals('<block_list> <block_expr> <expr_list>')

    #########################################

    program %= statment_list + expr
    program %= statment_list
    program %= expr + semi ######Estoy obligando al punto y coma

    statment_list %= stat
    statment_list %= stat + statment_list
    stat %= inline_function
    stat %= block_function
    #poner typedef

    inline_function %= function_ + id_ + opar + expr_list + cpar + arrow + expr + semi
    inline_function %= function_ + id_ + opar + cpar + arrow + expr + semi

    block_function %= function_ + id_ + opar + expr_list + cpar + block_expr 
    block_function %=  function_ + id_ + opar + cpar + block_expr
    block_expr %= okey + block_list + ckey
    block_list %= expr + semi
    block_list %= expr + semi + block_list
    expr_list %= id_
    expr_list %= id_ + comma + expr_list

    function_call %= id_ + opar + params_list + cpar
    params_list %= expr
    params_list %= expr + comma + params_list

    expr %= comparable_expr
    expr %= boolean_expr
    expr %= print_expr
    expr %= let_expr
    expr %= destruct_expr

    comparable_expr %= num_expr
    comparable_expr %= str_expr

    #String expressions
    str_expr %= str_
    #str_expr %= str_ + concat + num_expr
    #str_expr %= str_ + concat + boolean_expr
    #str_expr %= str_ + concat + str_

    print_expr %= print_ + opar + str_expr + cpar
    print_expr %= print_ + opar + id_ + cpar

    let_expr %= let + assign_list + in_ + expr
    let_expr %= let + assign_list + in_ + block_expr

    destruct_expr %= dest 
    destruct_expr %= dest + comma + destruct_expr

    dest %= id_ + dest_op + expr

    assign_list %= assign
    assign_list %= assign + comma + assign_list

    assign %= id_ + equal + expr

    #Comparative operators

    comparative_operator %= equals
    comparative_operator %= not_equals
    comparative_operator %= greater
    comparative_operator %= less
    comparative_operator %= greater_equals
    comparative_operator %= less_equals

    #Boolean expressions
    boolean_expr %= boolean_expr + comparative_operator + boolean_term
    boolean_expr %= comparable_expr + comparative_operator + comparable_expr
    boolean_expr %= boolean_expr + comparative_operator + comparable_expr
    boolean_expr %= boolean_expr + and_ + boolean_term
    boolean_expr %= boolean_expr + or_ + boolean_term
    boolean_expr %= not_ + boolean_term
    boolean_expr %= boolean_term

    boolean_term %= opar + boolean_expr + cpar
    boolean_term %= true_
    boolean_term %= false_

    # Numerical expressions
    num_expr %= num_expr + plus + term
    num_expr %= num_expr + minus + term 
    num_expr %= term

    term %= term + star + factor
    term %= term + div + factor
    term %= factor

    factor %= factor + power + constant
    factor %= constant

    constant %= opar + num_expr + cpar 
    constant %= num
    constant %= euler
    constant %= pi
    constant %= math_function
    constant %= id_
    constant %= function_call

    math_function %= sqrt + opar + num_expr + cpar
    math_function %= sen + opar + num_expr + cpar
    math_function %= cos + opar + num_expr + cpar
    math_function %= log + opar + num_expr + comma + num_expr + cpar
    math_function %= exp + opar + num_expr + cpar

    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    
    
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
    letters = letters +'|'+'|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))  
    symbols="!|@|%|^|&|\\*|_|+|-|/|:|;|\\<|\\>|\\=|,|.|?|~|`|\\(|\\)|[|]|{|}|#|'|\\||¿|¡|º|ª|¬"
    vari = f'\\"({letters}|{nonzero_digits}|{symbols}| |\\")*\\"'
    lexer = Lexer([
        ('space', '  *'),
        (semi,';'),
        (comma,','),
        (plus,plus.Name),
        (minus,minus.Name),
        (opar,'\\'+opar.Name),
        (cpar,'\\'+cpar.Name),
        (star,'\\'+star.Name),
        (div,div.Name),
        (power,power.Name),
        (sqrt,sqrt.Name),
        (sen,sen.Name),
        (cos,cos.Name),
        (log,log.Name),
        (exp,exp.Name),
        (function_,function_.Name),
        (arrow,arrow.Name),
        (okey,okey.Name),
        (ckey,ckey.Name),
        (not_, not_.Name),
        (and_, and_.Name),
        (or_, or_.Name),
        (true_,true_.Name),
        (false_,false_.Name),
        (equals,equals.Name),
        (not_equals,not_equals.Name),
        (greater,greater.Name),
        (less,less.Name),
        (greater_equals,greater_equals.Name),
        (less_equals,less_equals.Name),
        (num, f'({nonzero_digits})(0|{nonzero_digits})*|0'),
        (euler, euler.Name),
        (pi, pi.Name),
        (str_, vari),
        (concat, concat.Name),
        (print_, print_.Name),
        (let, let.Name),
        (in_, in_.Name),
        (equal, equal.Name),
        (dest, dest.Name),
        (id_, f'({letters})({letters}|0|{nonzero_digits})*')
    ],G.EOF)

    texts=['let number = 42, text = "The meaning of life is" in print(text);',
            'let number = 42 in let text = "The meaning of life is" in print(number);',
            'let a = 5, b = 10, c = 20 in {print(a);};']

    parser=LR1Parser(G)
    c=0
    for i in texts:
        c+=1
        if c==len(texts): 
            print(i)
        tokens = lexer(i)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parsed=parser(tokens_type)
        assert parsed!=None


    print(5)








    

#test_lexer()
hulk_grammar()
#test_parser()
#test_parser_lexer()
#test_hulk()
#loop_grammar()
#test_grammar()