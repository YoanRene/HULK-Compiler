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
    asign_list, destr_expr, asign, let_var, def_func, block_def_function, print_stat, arg_list = G.NonTerminals('<asign-list> <destr-expr> <asignment> <let-var> <def-func> <def-block> <print-stat> <arg-list>')
    expr, term, factor, atom, power= G.NonTerminals('<expr> <term> <factor> <atom> <power>')
    func_call, expr_list, expr_str, block, block_list, block_let, boolean_exp, boolean_or_exp, boolean_not_exp = G.NonTerminals('<func-call> <expr-list> <expr-str> <block-expr> <block-list> <block-let> <boolean-exp> <boolean-or-exp> <boolean-not-exp> ')
    boolean_term_not_equals, boolean_term_equals, boolean_term_less_equals, boolean_term_greater_equals, boolean_term_less, boolean_term_greater = G.NonTerminals('<boolean-term-not-equals> <boolean-term-equals> <boolean-term-less-equals> <boolean-term-greater-equals> <boolean-term-less> <boolean-term-greater>')

    let, function_, printx, in_ = G.Terminals('let function print in')
    sqrt, sin, cos, tan, log, exp, rand = G.Terminals('sqrt sin cos tan log exp rand')
    semi, comma, opar, cpar, arrow, okey, ckey= G.Terminals('; , ( ) => { }')
    equal, plus, minus, star, div, pow, arroba, pow_star, destr = G.Terminals('= + - * / ^ @ ** :=') #######
    greater, less, equals, not_equals, greater_equals, less_equals, and_, or_, not_, true, false = G.Terminals('> < == != >= <= & \\| ! true false')
    idx, num, string_ = G.Terminals('id num str')

    # Productions

    program %= stat_list#, lambda h,s: ProgramNode(s[1])
    program %= block_list#, lambda h,s: ProgramNode(s[1] + s[2])

    block_list %= block + block_list#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)
    block_list %= block#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)


    block %= okey + stat_list + ckey#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)
    block %= block_def_function#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)
    block %= block_let#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)
    block %= block + semi#, lambda h,s: BlockNode([]) # Your code here!!! (add rule)

    block_def_function %= function_ + idx + opar + arg_list + cpar + okey + stat_list + ckey#, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7]) # Your code here!!! (add rule)
    block_let %= let + asign_list + in_ + okey + stat_list + ckey#, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)

    stat_list %= stat + semi#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    stat_list %= stat + semi + stat_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

    
    destr_expr %= idx + destr + boolean_exp#, lambda h,s: AsignNode(s[1], s[3]) # Your code here!!! (add rule)

    stat %= let_var#, lambda h,s: s[1] # Your code here!!! (add rule)
    stat %= def_func#, lambda h,s: s[1] # Your code here!!! (add rule)
    stat %= print_stat#, lambda h,s: s[1] # Your code here!!! (add rule)
    stat %= expr_str
    stat %= destr_expr#, lambda h,s: AsignNode(s[1], s[3]) # Your code here!!! (add rule)

    let_var %= let + asign_list + in_ + stat#, lambda h,s: VarDeclarationNode(s[2], s[4]) # Your code here!!! (add rule)
    let_var %= let + asign_list + in_ + block_let

    def_func %= function_ + idx + opar + arg_list + cpar + arrow + boolean_exp#, lambda h,s: FuncDeclarationNode(s[2], s[4], s[7]) # Your code here!!! (add rule)
    #def_func %= function_ + idx + opar + arg_list + cpar + okey + stat_list + ckey#, lambda h,s: FuncDeclarationNode(s[2], s[4], s[6]) # Your code here!!! (add rule)

    expr_str %= expr_str + arroba + boolean_exp#, lambda h,s: ConcatNode(s[1],s[3]) # Your code here!!! (add rule)
    expr_str %= boolean_exp#, lambda h,s: s[1] # Your code here!!! (add rule)

    
    print_stat %= printx + opar + expr_str + cpar#, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)
    print_stat %= printx + opar + let_var + cpar#, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)
    

    #print_stat %= printx + opar + string_ + cpar#, lambda h,s: PrintNode(s[2]) # Your code here!!! (add rule)
    asign %= idx + equal + expr_str#, lambda h,s: AsignNode(s[1],s[3]) # Your code here!!! (add rule)
    asign %= idx + equal +opar +let_var +cpar#, lambda h,s: AsignNode(s[1],s[3]) # Your code here!!! (add rule)
    asign %= idx + equal +destr_expr#, lambda h,s: AsignNode(s[1],s[3]) # Your code here!!! (add rule)


    asign_list %= asign_list + comma + asign#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)
    asign_list %= asign#, lambda h,s: s[1] # Your code here!!! (add rule)


    arg_list %= idx#, lambda h,s: [s[1]] # Your code here!!! (add rule)
    arg_list %= idx + comma + arg_list#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)

    boolean_exp %= boolean_exp + and_ + boolean_or_exp#, lambda h,s: AndNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_exp %= boolean_or_exp#, lambda h,s: s[1] # Your code here!!! (add rule)

    boolean_or_exp %= boolean_or_exp + or_ + boolean_not_exp#, lambda h,s: OrNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_or_exp %= boolean_not_exp#, lambda h,s: s[1] # Your code here!!! (add rule)

    boolean_not_exp %= not_ + boolean_term_equals#, lambda h,s: s[1] # Your code here!!! (add rule)
    boolean_not_exp %= boolean_term_equals#, lambda h,s: s[1] # Your code here!!! (add rule)
    
    
    boolean_term_equals %= boolean_term_equals + equals + boolean_term_not_equals#, lambda h,s: EqualsNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_term_equals %= boolean_term_not_equals#, lambda h,s: s[1] # Your code here!!! (add rule)

    boolean_term_not_equals %= boolean_term_not_equals+ not_equals + boolean_term_greater#, lambda h,s: NotEqualsNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_term_not_equals %= boolean_term_greater

    boolean_term_greater %= boolean_term_greater+ greater + boolean_term_greater_equals#, lambda h,s: GreaterNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_term_greater %= boolean_term_greater_equals#, lambda h,s: s[1] # Your code here!!! (add rule)
    
    boolean_term_greater_equals %= boolean_term_greater_equals + greater_equals + boolean_term_less#, lambda h,s: GreaterEqualsNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_term_greater_equals %= boolean_term_less#, lambda h,s: s[1] # Your code here!!! (add rule)

    boolean_term_less %= boolean_term_less + less + boolean_term_less_equals#, lambda h,s: LessNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_term_less %= boolean_term_less_equals#, lambda h,s: s[1] # Your code here!!! (add rule)
    
    boolean_term_less_equals %= boolean_term_less_equals + less_equals + expr#, lambda h,s: LessEqualsNode(s[1],s[3]) # Your code here!!! (add rule)
    boolean_term_less_equals %= expr#, lambda h,s: s[1] # Your code here!!! (add rule)

    expr %= expr + plus + term#, lambda h,s: PlusNode(s[1],s[3]) # Your code here!!! (add rule)
    expr %= expr + minus + term#, lambda h,s: MinusNode(s[1],s[3]) # Your code here!!! (add rule)
    expr %= term#, lambda h,s: s[1] # Your code here!!! (add rule)

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
    atom %= idx#, lambda h,s: VariableNode(s[1]) # Your code here!!! (add rule)
    atom %= func_call#, lambda h,s: s[1] # Your code here!!! (add rule)
    atom %= sqrt + opar + expr + cpar#, lambda h,s: SqrtNode(s[3]) # Your code here!!! (add rule)
    atom %= sin + opar + expr + cpar#, lambda h,s: SinNode(s[3]) # Your code here!!! (add rule)
    atom %= cos + opar + expr + cpar#, lambda h,s: CosNode(s[3]) # Your code here!!! (add rule)
    atom %= log + opar + expr + comma + expr + cpar#, lambda h,s: LogNode(s[3]) # Your code here!!! (add rule)
    atom %= exp + opar + expr + cpar#, lambda h,s: ExpNode(s[3]) # Your code here!!! (add rule)
    atom %= rand + opar + cpar#, lambda h,s: RandNode() # Your code here!!! (add rule)
    #atom %= boolean_exp#, lambda h,s: s[1] # Your code here!!! (add rule)

    func_call %= idx + opar + expr_list + cpar#, lambda h,s: CallNode(s[1], s[3]) # Your code here!!! (add rule)

    expr_list %= expr_list + comma + expr#, lambda h,s: [s[1]] + s[3] # Your code here!!! (add rule)
    expr_list %= expr#, lambda h,s: [s[1]] # Your code here!!! (add rule)

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
        (idx, f'({letters})({letters}|0|{nonzero_digits})*')
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


   

   









    

#test_lexer()

#test_parser()
#test_parser_lexer()
#test_hulk()
#loop_grammar()
test_grammar()