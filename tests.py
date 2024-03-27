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

    G=Grammar()
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




    

#test_lexer()

#test_parser()
#test_parser_lexer()
#test_hulk()
loop_grammar()