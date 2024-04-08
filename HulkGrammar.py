from Grammar import *
from Lexer import *
from Semantic_checker import *
import math


def HulkGrammar():

    G=Grammar()

    program = G.NonTerminal('<program>',True)

    expr = G.NonTerminal('<expr>')

    body = G.NonTerminal('<body>')
    loc = G.NonTerminal('<loc>')
    logic_concat_expr, as_expr = G.NonTerminals('<logic-concat-expr> <as-expr>')
    decls_methods_semi, method = G.NonTerminals('<decls-methods-semi> <method>')
    method_protocol, method_protocol_list = G.NonTerminals('<method-protocol> <method-protocol-list>')
    protocol_stat, extends_expr = G.NonTerminals('<protocol> <extends>')
    type_stat, inherits_expr = G.NonTerminals('<type> <inherits>')
    function_stat, params, params_aux, params_in_par = G.NonTerminals('<function> <params> <params-aux> <params-in-par>')
    let_expr,if_expr,print_expr, destr_expr, while_expr, for_expr, inst_expr, array_expr  = G.NonTerminals('<let-expr> <if-expr> <print-expr> <destr-expr> <while-expr> <for-expr> <inst-expr> <array-expr>')
    elif_expr, else_expr = G.NonTerminals('<elif-expr> <else-expr>')
    expr_body, expr_list_semi = G.NonTerminals('<expr-body> <expr-list-semi>')
    expr_elem, term, factor, pow_expr = G.NonTerminals('<expr-elem> <term> <factor> <pow-expr>')
    aritm_expr, comp_expr = G.NonTerminals('<aritm-expr> <comp-expr>')
    decl, decls = G.NonTerminals('<decl> <decls>')
    id_extend = G.NonTerminal('<id-extend>')
    args, args_aux, args_in_par = G.NonTerminals('<args> <args-aux> <args-in-par>')
    expr_dot = G.NonTerminal('<expr-dot>')
    negative = G.NonTerminal('<negative>')
    let_optional = G.NonTerminal('<let-optional>')
    block_expr_semi_list = G.NonTerminal('<block-expr-semi-list>')
    

    type_, inherits, extends, protocol, new_ = G.Terminals('type inherits extends protocol new')
    function_, arrow = G.Terminals('function =>')
    print_ = G.Terminal('print')
    let, asign, in_ = G.Terminals('let = in')
    if_, elif_, else_ = G.Terminals('if elif else')
    while_, for_ = G.Terminals('while for')
    arroba, double_arroba, destr = G.Terminals('@ @@ :=')
    plus ,minus, pow_, pow_2, star, div, mod, opar, cpar = G.Terminals('+ - ^ ** * / % ( )')  
    and_, or_, not_ = G.Terminals('& | !')  
    equals, not_equals, greater, greater_equals, less, less_equals = G.Terminals('== != > >= < <=')  
    num, id_, string = G.Terminals('num id string')
    is_, as_ = G.Terminals('is as')
    okey, ckey, oindex, cindex = G.Terminals('{ } [ ]')
    semi, comma, double_dot, dot = G.Terminals('; , : .')
    sqrt, sin, cos, exp, log, rand = G.Terminals('sqrt sin cos exp log rand')   
    e, pi = G.Terminals('E PI')
    that = G.Terminal('||')

    program %= program + expr + semi , lambda h,s: ProgramNode(s[1],s[2])
    program %= program + function_stat , lambda h,s: ProgramNode(s[1],s[2])
    program %= program + protocol_stat , lambda h,s: ProgramNode(s[1],s[2])
    program %= program + type_stat , lambda h,s: ProgramNode(s[1],s[2])
    program %= program + okey + block_expr_semi_list + ckey , lambda h,s: ProgramNode(s[1],s[3])
    program %= G.Epsilon  , lambda h,s: ProgramNode(None,None)

    block_expr_semi_list %= block_expr_semi_list + okey + block_expr_semi_list + ckey, lambda h,s : BlockExprListNode(s[1],s[3])
    block_expr_semi_list %= block_expr_semi_list + expr + semi , lambda h,s : BlockExprListNode(s[1],[s[2]])
    block_expr_semi_list %= G.Epsilon , lambda h,s : BlockExprListNode(None,None)
    
    function_stat %= function_ + id_ + opar + params + cpar + id_extend + body ,lambda h,s: FunctionStatNode(s[2],s[4],s[6],s[7])

    type_stat %= type_ + id_ + params_in_par + inherits_expr + okey + decls_methods_semi  + ckey , lambda h,s: TypeStatNode(s[2],s[4],s[6])

    protocol_stat %= protocol + id_ + extends_expr + okey + method_protocol_list + ckey , lambda h,s: ProtocolStatNode(s[2],s[4],s[6])

    method_protocol %= id_ + opar + params + cpar + id_extend  , lambda h,s: MethodProtocolNode(s[1],s[3],s[5])

    method_protocol_list %= method_protocol_list + method_protocol + semi , lambda h,s: s[1] + [s[2]]
    method_protocol_list %= method_protocol + semi , lambda h,s: [s[1]]

    extends_expr %= extends + id_  , lambda h,s: ExtendsExprNode( s[2])
    extends_expr %= G.Epsilon , lambda h,s: ExtendsExprNode(None)

    inherits_expr %= inherits + id_ + args_in_par  , lambda h,s: InheritsExprNode( s[2], s[3])
    inherits_expr %= G.Epsilon , lambda h,s: InheritsExprNode( None, None)

    decls_methods_semi %= decls_methods_semi + decl + semi , lambda h,s: s[1] + [s[2]] ##
    decls_methods_semi %= decls_methods_semi + method , lambda h,s: s[1] + [s[2]] ##
    decls_methods_semi %= G.Epsilon , lambda h,s: None

    method %= id_ + opar + params + cpar + id_extend + body , lambda h,s: MethodNode(s[1],s[3],s[5],s[6])

    body %= arrow + expr + semi , lambda h,s: BodyNode(s[2])
    body %= okey + expr_list_semi + ckey , lambda h,s: BodyNode(s[2])

    params_aux %= id_ + id_extend  , lambda h,s: [ParamsAuxNode(None,s[1],s[2])]
    params_aux %= params_aux + comma + id_ + id_extend, lambda h,s:s[1]+[ParamsAuxNode(s[1],s[3],s[4])]

    params %= params_aux , lambda h,s: ParamsNode(s[1])
    params %= G.Epsilon , lambda h,s: ParamsNode(None)

    params_in_par %= opar + params + cpar , lambda h,s: ParamsInParNode(s[2])
    params_in_par %= G.Epsilon , lambda h,s: ParamsInParNode(None)

    expr %= let_expr ,lambda h,s: s[1]
    expr %= if_expr ,lambda h,s: s[1]
    expr %= for_expr ,lambda h,s: s[1]
    expr %= while_expr ,lambda h,s: s[1]
    expr %= print_expr ,lambda h,s: s[1]
    expr %= destr_expr ,lambda h,s: s[1]
    expr %= inst_expr ,lambda h,s: s[1]
    expr %= array_expr ,lambda h,s: s[1]
    expr %= expr_elem ,lambda h,s: s[1]

    inst_expr %= new_ + id_ + opar + args + cpar  , lambda h,s: InstExprNode(s[2],s[4])

    array_expr %= new_ + id_ + oindex + expr + cindex , lambda h,s: ArrayExprNode(s[2],s[4])

    print_expr %= print_ + opar + expr + cpar , lambda h,s: PrintExprNode(s[1],s[3])

    let_expr %= let + decls + in_ + expr_body , lambda h,s: LetExprNode(s[2],s[4])

    let_optional %= let , lambda h,s: LetOptionalNode(s[1])
    let_optional %= G.Epsilon , lambda h,s: LetOptionalNode(None)

    destr_expr %= loc + destr + expr , lambda h,s: DestrExprNode(s[1],s[3])

    while_expr %=  while_ + opar + expr + cpar + expr_body , lambda h,s: WhileExprNode(s[3],s[5])

    for_expr %= for_ + opar + id_ + in_ + expr + cpar + expr_body , lambda h,s: ForExprNode(s[3],s[5],s[7])

    if_expr %= if_ + opar + expr + cpar + expr_body + elif_expr , lambda h,s: IfExprNode(s[3],s[5],s[6])

    elif_expr %= elif_ + opar + expr + cpar + expr_body + elif_expr , lambda h,s: ElifExprNode(s[3],s[5],s[6])
    elif_expr %= else_expr , lambda h,s: s[1] #########################3

    else_expr %= else_ + expr_body , lambda h,s: ElseExprNode(s[2])

    decl %= id_ + id_extend + asign + expr , lambda h,s: DeclNode(s[1],s[2],s[4])

    decls %= decls + comma + let_optional+ decl , lambda h,s: s[1] + [s[3]] ############
    decls %= decl , lambda h,s: [s[1]]

    expr_body %= expr  , lambda h,s: ExprBodyNode(s[1])
    expr_body %= okey + expr_list_semi + ckey , lambda h,s: ExprBodyNode(s[2])

    expr_list_semi %= expr_list_semi + expr + semi , lambda h,s: ExprListSemiNode(s[1],s[2])
    expr_list_semi %= expr + semi , lambda h,s: ExprListSemiNode(None,s[1])

    id_extend %= double_dot + id_ , lambda h,s: IdExtendNode(s[2])
    id_extend %= G.Epsilon , lambda h,s: IdExtendNode(None)

    expr_elem %= expr_elem + is_ + as_expr , lambda h,s: ExprElemNode(s[1],s[3], True)
    expr_elem %= as_expr  , lambda h,s: ExprElemNode(s[1],None, False)

    as_expr %= as_expr + as_ + logic_concat_expr , lambda h,s: AsExprNode(s[1],s[3])
    as_expr %= logic_concat_expr , lambda h,s: AsExprNode(s[1],None)

    logic_concat_expr %= logic_concat_expr + arroba + comp_expr , lambda h,s: LogicConcatExprNode(s[1],s[3],"@")
    logic_concat_expr %= logic_concat_expr + double_arroba + comp_expr , lambda h,s: LogicConcatExprNode(s[1],s[3], "@@")
    logic_concat_expr %= logic_concat_expr + and_ + comp_expr , lambda h,s: AndNode(s[1],s[3])
    logic_concat_expr %= logic_concat_expr + or_ + comp_expr , lambda h,s: OrNode(s[1],s[3])
    logic_concat_expr %= not_ + comp_expr , lambda h,s: NotNode(s[2])
    logic_concat_expr %= comp_expr , lambda h,s: LogicConcatExprNode(s[1],None,None)

    comp_expr %= comp_expr + equals + aritm_expr , lambda h,s: EqualsNode(s[1],s[3])
    comp_expr %= comp_expr + not_equals + aritm_expr , lambda h,s: NotEqualsNode(s[1],s[3])
    comp_expr %= comp_expr + greater + aritm_expr , lambda h,s: GreaterNode(s[1],s[3])
    comp_expr %= comp_expr + greater_equals + aritm_expr , lambda h,s: GreaterEqualsNode(s[1],s[3])
    comp_expr %= comp_expr + less + aritm_expr , lambda h,s: LessNode(s[1],s[3])
    comp_expr %= comp_expr + less_equals + aritm_expr , lambda h,s: LessEqualsNode(s[1],s[3])
    comp_expr %= aritm_expr , lambda h,s: CompExprNode(s[1],None)

    aritm_expr %= aritm_expr + plus + term , lambda h,s: SumNode(s[1],s[3]) ##seria sum node
    aritm_expr %= aritm_expr + minus + term , lambda h,s: MinusNode(s[1],s[3]) ##
    aritm_expr %= term , lambda h,s: AritmExprNode(s[1],None) ##

    term %= term + star + pow_expr , lambda h,s: MultNode(s[1],s[3]) ##
    term %= term + div + pow_expr , lambda h,s: DivNode(s[1],s[3]) ##
    term %= term + mod + pow_expr , lambda h,s: ModNode(s[1],s[3]) ##
    term %= pow_expr , lambda h,s: TermNode(s[1],None) ##

    pow_expr %= pow_expr + pow_ + negative , lambda h,s: PowExprNode(s[1],s[3]) ##
    pow_expr %= pow_expr + pow_2 + negative , lambda h,s: PowExprNode(s[1],s[3]) ##
    pow_expr %= negative , lambda h,s: PowExprNode(s[1],None) ##

    negative %= minus + factor , lambda h,s: NegativeNode(s[2], True)
    negative %= factor , lambda h,s: NegativeNode(s[1], False)

    factor %= opar + expr + cpar , lambda h,s: FactorNode(s[2],None,None)
    factor %= num , lambda h,s: NumNode(s[1],None, None)
    factor %= string , lambda h,s: StrNode(s[1])
    factor %= sqrt + opar + expr + cpar , lambda h,s: NumNode(s[3],None,s[1])
    factor %= sin + opar + expr + cpar , lambda h,s: NumNode(s[3],None,s[1])
    factor %= cos + opar + expr + cpar , lambda h,s: NumNode(s[3],None,s[1])
    factor %= exp + opar + expr + cpar , lambda h,s: NumNode(s[3],None,s[1])
    factor %= log + opar + expr + comma + expr + cpar , lambda h,s:NumNode(s[3],s[5],s[1])
    factor %= rand + opar + cpar , lambda h,s: NumNode(None,None,s[1])
    factor %= e , lambda h,s: NumNode(math.e , None, None)
    factor %= pi , lambda h,s: NumNode(math.pi , None, None)
    factor %= loc , lambda h,s: FactorNode(s[1],None,None)
    factor %= oindex + args + cindex  , lambda h,s: VectorNode(s[2],None,None)
    factor %= oindex + expr + that + params_aux + in_ + expr + cindex , lambda h,s: VectorNode(s[2],s[4],s[6]) 

    loc %= loc + dot + id_ + args_in_par , lambda h,s: LocNode(s[1],s[3],s[4])
    loc %= loc + oindex + expr + cindex , lambda h,s: LocNode(s[1],s[3],None)
    loc %= id_ + args_in_par , lambda h,s: LocNode(None, s[1], s[2])

    args_aux %= expr  , lambda h,s: ArgsAuxNode(s[1],None)
    args_aux %= args_aux + comma + expr , lambda h,s: ArgsAuxNode(s[1],s[3])

    args %= args_aux , lambda h,s: ArgsNode(s[1])
    args %= G.Epsilon , lambda h,s: ArgsNode(None)

    args_in_par %= opar + args + cpar , lambda h,s: ArgsInParNode(s[2])
    args_in_par %= G.Epsilon , lambda h,s: ArgsInParNode(None)

    #Generating Lexer
    nonzero_digits = '|'.join(str(n) for n in range(1,10))
    integers_no_zero = f'({nonzero_digits})(0|{nonzero_digits})*'
    floats = f'{integers_no_zero}.(0|{nonzero_digits})(0|{nonzero_digits})*|0.(0|{nonzero_digits})(0|{nonzero_digits})*'

    letters = '|'.join(chr(n) for n in range(ord('a'),ord('z')+1))
    letters = letters +'|'+'|'.join(chr(n) for n in range(ord('A'),ord('Z')+1))
    symbols="!|@|%|^|&|\\*|_|+|-|/|:|;|<|>|=|,|.|?|~|`|\\(|\\)|[|]|{|}|#|'|\\||¿|¡|º|ª|¬"
    string_re = f'\\"({letters}|{nonzero_digits}|{symbols}| |\\")*\\"'

    lexer = Lexer([
        ('space',' *'),

        (semi,semi.Name),
        (comma, comma.Name),
        (double_dot,double_dot.Name),
        (dot,dot.Name),

        (type_,type_.Name),
        (inherits,inherits.Name),
        (extends,extends.Name),
        (protocol,protocol.Name),
        (new_, new_.Name),

        (is_,is_.Name),
        (as_,as_.Name),

        (function_,function_.Name),
        (arrow,arrow.Name),

        (arroba,arroba.Name),
        (double_arroba,double_arroba.Name),
        (destr,destr.Name),

        (print_,print_.Name),

        (let,let.Name),
        (asign,asign.Name),
        (in_,in_.Name),

        (if_, if_.Name),
        (elif_,elif_.Name),
        (else_,else_.Name),

        (while_,while_.Name),
        (for_,for_.Name),

        (that,'\\|\\|'),

        (pow_,pow_.Name),
        (pow_2,'\\*\\*'),

        (star,'\\'+star.Name),
        (div,div.Name),
        (mod,mod.Name),

        (plus,plus.Name),
        (minus, minus.Name),

        (opar,'\\'+opar.Name),
        (cpar,'\\'+cpar.Name),

        (okey,okey.Name),
        (ckey,ckey.Name),
        (oindex,oindex.Name),
        (cindex,cindex.Name),

        (and_,and_.Name),
        (or_,'\\'+or_.Name),
        (not_,not_.Name),

        (equals,equals.Name),
        (not_equals,not_equals.Name),
        (greater,greater.Name),
        (greater_equals,greater_equals.Name),
        (less,less.Name),
        (less_equals,less_equals.Name),

        (sqrt,sqrt.Name),
        (sin,sin.Name),
        (cos,cos.Name),
        (exp,exp.Name),
        (log,log.Name),
        (rand,rand.Name),

        (e,e.Name),
        (pi,pi.Name),

        (num, f'{integers_no_zero}|{floats}|0'),
        (id_, f'({letters})({letters}|0|{nonzero_digits})*'),
        (string, string_re)
    ],G.EOF) 

    return G,lexer