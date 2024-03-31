from Grammar import *
from Lexer import *


def HulkGrammar():

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
    program %= comparable_expr + semi 
    program %= boolean_expr + semi 
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

    #Generating Lexer
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

    return G,lexer