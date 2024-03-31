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

def test_grammar():
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

    

    # expr %= expr + and_ + comp_expr | expr + or_ + comp_expr | not_ + comp_expr | comp_expr

    # comp_expr %= comp_expr + equals + aritm_expr | comp_expr + not_equals + aritm_expr | comp_expr + less + aritm_expr | comp_expr + less_equals + aritm_expr | comp_expr + greater_equals + aritm_expr | comp_expr + greater + aritm_expr | aritm_expr

    # aritm_expr %= aritm_expr + plus + term | aritm_expr + minus + term | term
    
    # term %= term + star + factor | term + div + factor | factor

    # factor %= num | opar + expr + cpar  


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
    
    #Expressions Functions 
    texts =['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print( "Hello :is+ the@  World" );',
            'print("The message is \"Hello World\"");','print("The meaning of life is " @ 42);',
            'print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));' ,
            '{print(42); print(sin(PI/2)); print("Hello World");}','function tan(x) => sin(x) / cos(x);',
            'function cot(x) => 1 / tan(x);function tan(x) => sin(x) / cos(x);print(tan(PI) ** 2 + cot(PI) ** 2);',
            'function operate(x, y) { print(x + y);print(x - y);print(x * y);print(x / y);}',
            'let msg = "Hello World" in print(msg);',
            'let number = 42, text = "The meaning of life is" in print(text @ number);',
            'let number = 42 in let text = "The meaning of life is" in print(text @ number);'

        ]

    texts1 = ['protocol Equalable extends Hasheable { equals(other: Object):Boolean;}',
              'while (x) { 42;};',
              'for (x in range(0,10)) x;'  ]

    parser=LR1Parser(G)
    c=0
    for i in texts1:
        c+=1
        if c==12: 
            print(i)
        tokens = lexer(i)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        parsed=parser(tokens_type)
        assert parsed!=None

def semantic_checker_test():

    #region gramatica
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

    #endregion

    #region producciones
    program %= statment_list + expr + semi , lambda h,s: ProgramNode(s[1],s[2])
    program %= statment_list, lambda h,s: ProgramNode(s[1])
    program %= expr + semi , lambda h,s: ProgramNode(s[1])

    statment_list %= stat , lambda h,s: s[1]
    statment_list %= stat + statment_list ,lambda h,s: [s[1]]+s[2]

    stat %= inline_function ,lambda h,s: s[1]
    stat %= block_function ,lambda h,s: s[1]
    stat %= type_expr ,lambda h,s: s[1]
    stat %= protocol_expr  ,lambda h,s: s[1]

    inline_function %= function_ + id_ + opar + expr_list + cpar + arrow + expr + semi ,lambda h,s: FuncDeclarationNode(s[2],s[4],s[7])
    inline_function %= function_ + id_ + opar + cpar + arrow + expr + semi ,lambda h,s: FuncDeclarationNode(s[2],[],s[5])

    block_function %= function_ + id_ + opar + expr_list + cpar + block_expr ,lambda h,s: FuncDeclarationNode(s[2],s[4],s[6])
    block_function %=  function_ + id_ + opar + cpar + block_expr ,lambda h,s: FuncDeclarationNode(s[2],[],s[5])
    block_expr %= okey + block_list + ckey ,lambda h,s: s[2]
    block_list %= expr + semi ,lambda h,s: [s[1]]
    block_list %= expr + semi + block_list ,lambda h,s: [s[1]]+s[3]

    expr_list %= id_ ,lambda h,s: VariableNode(s[1])
    expr_list %= id_ + comma + expr_list ,lambda h,s: [VariableNode(s[1])]+s[3] ####

    # expr_list_epsilon %= expr_list####
    # expr_list_epsilon %= G.Epsilon####

    iterable %= function_call  ,lambda h,s: s[1]
    iterable %= id_ ,lambda h,s: s[1]

    iterable_ext %= iterable + dot + iterable_ext ,lambda h,s: [s[1]]+s[3]
    iterable_ext %= iterable  ,lambda h,s: [s[1]]

    for_expr %= for_ + opar + id_ + in_ + iterable + cpar + block_expr ,lambda h,s: ForNode(s[3],s[5],s[7])
    for_expr %= for_ + opar + id_ + in_ + iterable + cpar + expr ,lambda h,s: ForNode(s[3],s[5],s[7])

    while_expr %= while_ + opar + boolean_expr + cpar + block_expr  ,lambda h,s: WhileNode(s[3],s[5])
    while_expr %= while_ + opar + boolean_expr + cpar + expr ,lambda h,s: WhileNode(s[3],s[5])
    while_expr %= while_ + opar + iterable_ext + cpar + block_expr ,lambda h,s: WhileNode(s[3],s[5])
    while_expr %= while_ + opar + iterable_ext + cpar + expr ,lambda h,s: WhileNode(s[3],s[5])

    function_call %= id_ + opar + params_list + cpar ,lambda h,s: CallNode(s[1],s[3])
    function_call %= id_ + opar + cpar ,lambda h,s: CallNode(s[1],[])

    params_list %= param ,lambda h,s: [s[1]]
    params_list %= param + comma + params_list ,lambda h,s: [s[1]]+s[3]

    param %= comparable_expr ,lambda h,s: s[1]
    param %= boolean_expr ,lambda h,s: s[1]

    expr %= comparable_expr , lambda h,s: ExpressionNode(s[1])
    expr %= boolean_expr , lambda h,s: ExpressionNode(s[1])
    expr %= print_expr , lambda h,s: ExpressionNode(s[1])
    expr %= let_expr , lambda h,s: ExpressionNode(s[1])
    expr %= destruct_expr , lambda h,s: ExpressionNode(s[1])
    expr %= conditional_expr , lambda h,s: ExpressionNode(s[1])
    expr %= while_expr , lambda h,s: ExpressionNode(s[1])
    expr %= for_expr , lambda h,s: ExpressionNode(s[1])

    comparable_expr %= num_expr , lambda h,s: s[1]
    comparable_expr %= str_expr , lambda h,s: s[1]

    #String expressions
    str_expr %= str_ , lambda h,s: s[1]
    #str_expr %= str_ + concat + num_expr
    #str_expr %= str_ + concat + boolean_expr
    #str_expr %= str_ + concat + str_

    print_expr %= print_ + opar + comparable_expr + cpar , lambda h,s: PrintNode(s[3])
    #print_expr %= print_ + opar + id_ + cpar

    let_expr %= let + assign_list + in_ + expr , lambda h,s: VarDeclarationNode(s[2],s[4])
    let_expr %= let + assign_list + in_ + block_expr , lambda h,s: VarDeclarationNode(s[2],s[4])

    destruct_expr %= id_ + dest_op + expr , lambda h,s: DestructNode(s[1],s[3])
   
    assign_list %= assign , lambda h,s: [s[1]]
    assign_list %= assign + comma + assign_list , lambda h,s: [s[1]]+s[3]

    assign %= id_ + equal + expr , lambda h,s: AssignNode(s[1],s[3])

    if_expr %= if_ + opar + boolean_expr + cpar + expr  , lambda h,s: IfNode(s[3],s[5])
    if_expr %= if_ + opar + boolean_expr + cpar + block_expr , lambda h,s: IfNode(s[3],s[5])

    else_expr %= else_ + expr , lambda h,s: ElseNode(s[2])
    else_expr %= else_ + block_expr , lambda h,s: ElseNode(s[2])

    #elif_expr %= elif_ + opar + boolean_expr + cpar + expr
    #elif_expr %= elif_ + opar + boolean_expr + cpar + block_expr

    #elif_expr_list %= elif_expr + elif_expr_list #####agregar el else expresion aqui
    #elif_expr_list %= elif_expr

    conditional_expr %= if_expr + elif_ + opar + boolean_expr + cpar + expr + else_expr  , lambda h,s: Conditional_expr(s[1],s[4],s[6],s[7])
    conditional_expr %= if_expr + else_expr , lambda h,s: Conditional_expr(s[1],None,s[3],s[4])
    
    id_ext %= double_point + id_ , lambda h,s: s[2]

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

    protocol_expr %= protocol + id_ + extends_expr + okey + method_protocol_list + ckey , lambda h,s: ProtocolNode(s[2],s[4])
    protocol_expr %= protocol + id_ + extends_expr + okey + ckey , lambda h,s: ProtocolNode(s[2],[])
    protocol_expr %= protocol + id_ + okey + method_protocol_list + ckey , lambda h,s: ProtocolNode(s[2],s[4])
    protocol_expr %= protocol + id_ + okey + ckey , lambda h,s: ProtocolNode(s[2],[])

    protocol_exp_list %= protocol_exp_item + comma + protocol_exp_list , lambda h,s: [s[1]]+s[3]
    protocol_exp_list %= protocol_exp_item , lambda h,s: [s[1]]

    protocol_exp_item %= id_ + id_ext , lambda h,s: (s[1],s[2])

    method_protocol %= id_ + opar + protocol_exp_list + cpar + id_ext + semi , lambda h,s: MethodNode(s[1],s[3],s[5])
    method_protocol %= id_ + opar + cpar + id_ext + semi , lambda h,s: MethodNode(s[1],[],s[4])

    method_protocol_list %= method_protocol + method_protocol_list , lambda h,s: [s[1]]+s[2]
    method_protocol_list %= method_protocol , lambda h,s: [s[1]]

    extends_expr %= extends + id_ , lambda h,s: s[2]


    #Comparative operators

    comparative_operator %= equals , lambda h,s: s[1]
    comparative_operator %= not_equals , lambda h,s: s[1]
    comparative_operator %= greater , lambda h,s: s[1]
    comparative_operator %= less , lambda h,s: s[1]
    comparative_operator %= greater_equals , lambda h,s: s[1]
    comparative_operator %= less_equals , lambda h,s: s[1]

    #Boolean expressions
    boolean_expr %= boolean_expr + comparative_operator + boolean_term ,lambda h,s: Boolean_expr(s[1],s[2],s[3])
    boolean_expr %= comparable_expr + comparative_operator + comparable_expr ,lambda h,s: Boolean_expr(s[1],s[2],s[3])
    boolean_expr %= boolean_expr + comparative_operator + comparable_expr ,lambda h,s: Boolean_expr(s[1],s[2],s[3])
    boolean_expr %= boolean_expr + and_ + boolean_term ,lambda h,s: AndNode(s[1],s[3])
    boolean_expr %= boolean_expr + or_ + boolean_term ,lambda h,s: OrNode(s[1],s[3])
    boolean_expr %= not_ + boolean_term ,lambda h,s:NotNode (s[2])
    boolean_expr %= boolean_term ,lambda h,s: s[1]

    boolean_term %= opar + boolean_expr + cpar , lambda h,s: s[2]
    boolean_term %= true_ , lambda h,s: True
    boolean_term %= false_ , lambda h,s: False

    # Numerical expressions
    num_expr %= num_expr + plus + term , lambda h,s: PlusNode(s[1],s[3])
    num_expr %= num_expr + minus + term  , lambda h,s: MinusNode(s[1],s[3])
    num_expr %= term , lambda h,s: s[1] 

    term %= term + star + factor , lambda h,s: StarNode(s[1],s[3])
    term %= term + div + factor , lambda h,s: DivNode(s[1],s[3])
    term %= term + mod + factor , lambda h,s: ModNode(s[1],s[3])
    term %= factor , lambda h,s: s[1]

    factor %= factor + power + constant , lambda h,s: PowNode(s[1],s[3])
    factor %= constant , lambda h,s: s[1]

    constant %= opar + num_expr + cpar  , lambda h,s: s[2]
    constant %= num , lambda h,s: ConstantNumNode(s[1])
    constant %= euler  , lambda h,s: ConstantNumNode(euler)
    constant %= pi , lambda h,s: ConstantNumNode(pi)
    constant %= math_function , lambda h,s: s[1]
    constant %= iterable_ext , lambda h,s: s[1]

    math_function %= sqrt + opar + num_expr + cpar ,lambda h,s: SqrtNode(s[3])
    math_function %= sen + opar + num_expr + cpar ,lambda h,s: SinNode(s[3])
    math_function %= cos + opar + num_expr + cpar ,lambda h,s: CosNode(s[3])
    math_function %= log + opar + num_expr + comma + num_expr + cpar ,lambda h,s: LogNode(s[3],s[5])
    math_function %= exp + opar + num_expr + cpar ,lambda h,s: ExpNode(s[3])


    #endregion

    #region Lexer    
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
#test_parser()
#test_parser_lexer()
#test_hulk()
#loop_grammar()
#test_grammar()
semantic_checker_test()