from Lexer import *
from ParserLR1 import *
from Semantic_checker import *

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
    destruct_expr = G.NonTerminal('<destruct_expr>')
    comparative_operator = G.NonTerminal('<comparative_operator>')
    comparable_expr = G.NonTerminal('<comparable_expr>')
    str_expr = G.NonTerminal('<str_expr>')
    math_function = G.NonTerminal('<math_function>')
    function_call, params_list, param = G.NonTerminals('<function_call> <params_list> <param>')
    if_expr, elif_expr, elif_expr_list, else_expr, conditional_expr = G.NonTerminals('<if_expr> <elif_expr> <elif_expr_list> <else_expr> <conditional_expr>')
    expr_list_epsilon = G.NonTerminal('<expr_list_epsilon>')
    iterable, iterable_ext = G.NonTerminals('<iterable> <iterable_ext>')
    while_expr, for_expr = G.NonTerminals('<while_expr> <for_expr>')
    id_ext = G.NonTerminal('<id_ext>')
    method, method_list = G.NonTerminals('<method> <method_list>')
    inherits_id = G.NonTerminal('<inherits_id>')
    type_expr = G.NonTerminal('<type_expr>')
    block_type_elems, block_type_elems_list, block_type_expr = G.NonTerminals('<block_type_elems> <block_type_elems_list> <block_type_expr>')
    assign_type_list = G.NonTerminal('<assign_type_list>')
    protocol_expr = G.NonTerminal('<protocol_expr>')
    protocol_exp_list = G.NonTerminal('<protocol_exp_list>')
    protocol_exp_item = G.NonTerminal('<protocol_exp_item>')
    method_protocol = G.NonTerminal('<method_protocol>')
    method_protocol_list = G.NonTerminal('<method_protocol_list>')
    extends_expr = G.NonTerminal('<extends_expr>')

    function_ = G.Terminal('function')
    opar, cpar, okey, ckey, id_, arrow, semi, comma = G.Terminals(' ( ) { } id => ; ,')

    true_, false_ = G.Terminals('true false')
    and_, or_, not_ = G.Terminals('& \\| !')
    equals, not_equals, greater, less, greater_equals, less_equals = G.Terminals('== != > < >= <=')

    plus, minus, star, div, power, mod = G.Terminals(' + - * / ^ %')
    sqrt, sen, cos, log, exp = G.Terminals('sqrt sin cos log exp')
    num, euler, pi = G.Terminals('num Euler Pi')
    str_, concat, print_ = G.Terminals('str @ print')
    equal, in_, let, dest_op = G.Terminals('= in let :=')
    if_, else_, elif_ = G.Terminals('if else elif')
    while_, for_ = G.Terminals('while for')
    dot = G.Terminal('.')
    double_point = G.Terminal(':')
    inherits = G.Terminal('inherits')
    type_ = G.Terminal('type')
    protocol = G.Terminal('protocol')
    extends = G.Terminal('extends')

    block_list, block_expr, expr_list = G.NonTerminals('<block_list> <block_expr> <expr_list>')

    program %= statment_list + expr + semi
    program %= statment_list
    program %= comparable_expr + semi ######Estoy obligando al punto y coma
    program %= boolean_expr + semi ######Estoy obligando al punto y coma
    program %= let_expr + semi
    program %= for_expr + semi

    statment_list %= stat
    statment_list %= stat + statment_list
    stat %= inline_function
    stat %= block_function
    stat %= type_expr
    stat %= protocol_expr

    inline_function %= function_ + id_ + opar + expr_list + cpar + arrow + expr + semi
    inline_function %= function_ + id_ + opar + cpar + arrow + expr + semi

    block_function %= function_ + id_ + opar + expr_list + cpar + block_expr 
    block_function %=  function_ + id_ + opar + cpar + block_expr
    block_expr %= okey + block_list + ckey
    block_list %= expr + semi
    block_list %= expr + semi + block_list

    expr_list %= id_
    expr_list %= id_ + comma + expr_list

    expr_list_epsilon %= expr_list
    expr_list_epsilon %= G.Epsilon

    iterable %= function_call
    iterable %= id_

    iterable_ext %= iterable + dot + iterable_ext
    iterable_ext %= iterable

    for_expr %= for_ + opar + id_ + in_ + iterable + cpar + block_expr
    for_expr %= for_ + opar + id_ + in_ + iterable + cpar + expr

    while_expr %= while_ + opar + boolean_expr + cpar + block_expr 
    while_expr %= while_ + opar + boolean_expr + cpar + expr
    while_expr %= while_ + opar + iterable_ext + cpar + block_expr
    while_expr %= while_ + opar + iterable_ext + cpar + expr

    function_call %= id_ + opar + params_list + cpar
    function_call %= id_ + opar + cpar

    params_list %= param
    params_list %= param + comma + params_list

    param %= comparable_expr
    param %= boolean_expr

    expr %= comparable_expr
    expr %= boolean_expr
    expr %= print_expr
    expr %= let_expr
    expr %= destruct_expr
    expr %= conditional_expr
    expr %= while_expr
    expr %= for_expr

    comparable_expr %= num_expr
    comparable_expr %= str_expr

    #String expressions
    str_expr %= str_
    #str_expr %= str_ + concat + num_expr
    #str_expr %= str_ + concat + boolean_expr
    #str_expr %= str_ + concat + str_

    print_expr %= print_ + opar + comparable_expr + cpar
    #print_expr %= print_ + opar + id_ + cpar

    let_expr %= let + assign_list + in_ + expr
    let_expr %= let + assign_list + in_ + block_expr

    destruct_expr %= id_ + dest_op + expr
   
    assign_list %= assign
    assign_list %= assign + comma + assign_list

    assign %= id_ + equal + expr

    if_expr %= if_ + opar + boolean_expr + cpar + expr
    if_expr %= if_ + opar + boolean_expr + cpar + block_expr

    else_expr %= else_ + expr
    else_expr %= else_ + block_expr

    #elif_expr %= elif_ + opar + boolean_expr + cpar + expr
    #elif_expr %= elif_ + opar + boolean_expr + cpar + block_expr

    #elif_expr_list %= elif_expr + elif_expr_list #####agregar el else expresion aqui
    #elif_expr_list %= elif_expr

    conditional_expr %= if_expr + elif_ + opar + boolean_expr + cpar + expr + else_expr
    conditional_expr %= if_expr + else_expr
    
    id_ext %= double_point + id_

    # method %= id_ + opar + expr_list + cpar + id_ext + block_expr
    # method %= id_ + opar + expr_list + cpar + block_expr
    # method %= id_ + opar + cpar + id_ext + block_expr
    # method %= id_ + opar + cpar + block_expr
    # method %= id_ + opar + expr_list + cpar + arrow + expr
    # method %= id_ + opar + cpar + arrow + expr

    # method_list %= method + semi + method_list 
    # method_list %= method + semi

    # assign_type_list %= assign + semi
    # assign_type_list %= assign + semi + assign_type_list

    # block_type_expr %= okey + assign_type_list + method_list + ckey
    # block_type_expr %= okey + method_list + ckey
    # block_type_expr %= okey + assign_type_list + ckey

    # inherits_id %= inherits + id_
    # inherits_id %= inherits + function_call

    # type_expr %= type_ + id_ + opar + expr_list + cpar + inherits_id + block_type_expr
    # type_expr %= type_ + id_ + inherits_id + block_type_expr
    # type_expr %= type_ + id_ + opar + expr_list + cpar + block_type_expr
    # type_expr %= type_ + id_ + block_type_expr

    protocol_expr %= protocol + id_ + extends_expr + okey + method_protocol_list + ckey
    protocol_expr %= protocol + id_ + extends_expr + okey + ckey
    protocol_expr %= protocol + id_ + okey + method_protocol_list + ckey
    protocol_expr %= protocol + id_ + okey + ckey

    protocol_exp_list %= protocol_exp_item + comma + protocol_exp_list
    protocol_exp_list %= protocol_exp_item

    protocol_exp_item %= id_ + id_ext

    method_protocol %= id_ + opar + protocol_exp_list + cpar + id_ext + semi
    method_protocol %= id_ + opar + cpar + id_ext + semi

    method_protocol_list %= method_protocol + method_protocol_list
    method_protocol_list %= method_protocol

    extends_expr %= extends + id_


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
    term %= term + mod + factor
    term %= factor

    factor %= factor + power + constant
    factor %= constant

    constant %= opar + num_expr + cpar 
    constant %= num
    constant %= euler
    constant %= pi
    constant %= math_function
    constant %= iterable_ext

    math_function %= sqrt + opar + num_expr + cpar
    math_function %= sen + opar + num_expr + cpar
    math_function %= cos + opar + num_expr + cpar
    math_function %= log + opar + num_expr + comma + num_expr + cpar
    math_function %= exp + opar + num_expr + cpar
    
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
        (mod,mod.Name),
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
        (dest_op, dest_op.Name),
        (if_, if_.Name),
        (else_, else_.Name),
        (elif_, elif_.Name),
        (while_, while_.Name),
        (for_, for_.Name),
        (dot, dot.Name),
        (double_point, double_point.Name),
        (type_, type_.Name),
        (inherits, inherits.Name),
        (extends, extends.Name),
        (protocol, protocol.Name),
        (id_, f'({letters})({letters}|0|{nonzero_digits})*')
    ],G.EOF)

    texts=['type Point { x = 0; y = 0; }',
           'protocol Hashable { hash(): Number; }',
           'protocol Equatable extends Hashable { equals(other: Object): Boolean; }']

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
        print(4)


    print(5)


def semantic_checker_test():

    #region Gramatica
    G = Grammar()
    program = G.NonTerminal('<program>', startSymbol=True)
    stat_list, stat = G.NonTerminals('<stat_list> <stat>')
    extends_expr, id_extension, inherits_id_epsilon, args_in_par_epsilon ,args,args_epsilon,attr_list, attr,attr_f, let_var, def_func, def_func_block, print_stat, params,params_Epsilon = G.NonTerminals('<extends-expr> <id-extension> <inherits-id-epsilon> <args-in-par-epsilon> <args> <args-epsilon> <attr-list> <attr> <attr-f> <let-var> <def-func> <def-block> <print-stat> <params-list> <params-list-f>')
    aritm_expr, comp_expr, expr, term, factor, atom, power= G.NonTerminals('<aritm-expr> <comp-expr> <expr> <term> <factor> <atom> <power>')
    while_expr, iterable, expr_body, for_expr, method_protocol,method_protocol_list,protocol_expr, method_attr_list, method_list, method, body, func_call,type_expr, expr_list, expr_str, block, block_list, params_in_par_epsilon = G.NonTerminals('<while-expr> <iterable> <expr-body> <for-expr> <method-protocol> <method-protocol-list> <protocol-expr> <method-attr-list> <method-list> <method> <body> <func-call> <type-expr> <expr-list> <expr-str> <block-expr> <block-list> <params-in-par-epsilon>')


    let, function_, printx, in_, for_, while_ = G.Terminals('let function print in for while')
    sqrt, sin, cos, tan, log, exp, rand = G.Terminals('sqrt sin cos tan log exp rand')
    semi, comma, opar, cpar, arrow, okey, ckey= G.Terminals('; , ( ) => { }')
    and_, or_ ,not_ = G.Terminals('& | !')
    greater, greater_equals, equals, less, less_equals, not_equals = G.Terminals('> >= == < <= !=')
    equal, plus, minus, star, div, pow, arroba, pow_star,double_dot = G.Terminals('= + - * / ^ @ ** :') #######
    id_, num, string_ = G.Terminals('id num str')
    type_, protocol, inherits, extends = G.Terminals('type protocol inherits extends')

    # Productions

    program %= expr + semi | type_expr | protocol_expr | for_expr + semi | while_expr + semi

    type_expr %= type_ + id_ + params_in_par_epsilon + inherits_id_epsilon + okey + attr_list + ckey

    id_extension %= double_dot + id_ | G.Epsilon
    
    params %= id_ + id_extension | id_ + id_extension + comma + params 

    params_Epsilon %= params | G.Epsilon

    params_in_par_epsilon %= opar + params_Epsilon + cpar | G.Epsilon

    args %= expr | expr + comma + args 

    args_epsilon %= args | G.Epsilon

    args_in_par_epsilon %= opar + args_epsilon + cpar | G.Epsilon

    inherits_id_epsilon %= inherits + id_ + args_in_par_epsilon | G.Epsilon

    attr %= id_ + id_extension + equal + expr 

    attr_list %= attr + semi + attr_list | G.Epsilon 

    expr_list %= expr + semi | expr + semi + expr_list 

    method %= id_ + opar + params_Epsilon + cpar + id_extension + body  

    method_list %= method + method_list | G.Epsilon

    body %= arrow + expr + semi | okey + expr_list + ckey

    protocol_expr %= protocol + id_ + extends_expr + okey + method_protocol_list + ckey

    method_protocol %= id_ + opar + params_Epsilon + cpar + id_extension + semi

    method_protocol_list %= method_protocol + method_protocol_list | G.Epsilon

    extends_expr %= extends + id_ | G.Epsilon

    for_expr %= for_ + opar + id_ + in_ + iterable + cpar + expr_body

    while_expr %= while_ + opar + iterable + cpar + expr_body 

    iterable %= id_ + args_in_par_epsilon

    expr_body %= okey + expr_list + ckey
    expr_body %= expr

    expr %= num
    expr %= id_

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
        (and_,and_.Name),
        (or_,'\\'+or_.Name),
        (not_,not_.Name),
        (equals,equals.Name),
        (not_equals,not_equals.Name),
        (greater,greater.Name),
        (greater_equals,greater_equals.Name),
        (less,less.Name),
        (less_equals,less_equals.Name),
        (minus,minus.Name),
        (opar,'\\'+opar.Name),
        (cpar,'\\'+cpar.Name),
        (equal,equal.Name),
        (star,'\\'+star.Name),
        (div,div.Name),
        (pow,pow.Name),
        (pow_star,'\\'+pow_star.Name+'\\'+pow_star.Name),
        (function_,function_.Name),
        (arrow,arrow.Name),
        (function_,function_.Name),
        (printx,printx.Name),
        (let,let.Name),
        (for_,for_.Name),
        (while_,while_.Name),
        (in_,in_.Name),
        (sqrt,sqrt.Name),
        (sin,sin.Name),
        (cos,cos.Name),
        (log,log.Name),
        (exp,exp.Name),
        (double_dot,double_dot.Name),
        (arroba,arroba.Name),
        (rand,rand.Name),
        (okey,okey.Name),
        (ckey,ckey.Name),
        (type_,type_.Name),
        (protocol,protocol.Name),
        (extends,extends.Name),
        (inherits,inherits.Name),
        (num, f'({nonzero_digits})(0|{nonzero_digits})*|0'),
        (id_, f'({letters})({letters}|0|{nonzero_digits})*')
    ],G.EOF)
    #endregion

    texts=['5+4;']

    #region Parser
    parser = LR1Parser(G)
    for i in texts:
        tokens = lexer(i)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parse,operations = parser(tokens_type, get_shift_reduce=True)
    #endregion
    
    #region Semantic Checker
    ast = evaluate_reverse_parse(parse, operations, tokens)

    formatter = FormatVisitor()
    print(formatter.visit(ast))

    scope = Scope()

    semantic_checker = SemanticCheckerVisitor()
    errors = semantic_checker.visit(ast)
    for i, error in enumerate(errors,1):
        print(f'{i}.', error)

    #endregion





    

#test_lexer()
#hulk_grammar()
#test_parser()
#test_parser_lexer()
#test_hulk()
#loop_grammar()
#test_grammar()
semantic_checker_test()