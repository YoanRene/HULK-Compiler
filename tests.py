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


   

   









    

#test_lexer()

#test_parser()
#test_parser_lexer()
#test_hulk()
#loop_grammar()
test_grammar()