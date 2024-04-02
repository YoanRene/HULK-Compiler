from Grammar import Grammar
from Lexer import Lexer
from ParserSLR1 import SLR1Parser

G=Grammar()

program = G.NonTerminal('<program>',True)

expr = G.NonTerminal('<expr>')

body = G.NonTerminal('<body>')
function_stats, function_stat, params, params_aux= G.NonTerminals('<function-stats> <function> <params> <params-aux>')
let_expr,if_expr,print_expr  = G.NonTerminals('<let-expr> <if-expr> <print-expr>')
expr_body, expr_list_semi = G.NonTerminals('<expr-body> <expr-list-semi>')
expr_elem, term, factor, pow_expr = G.NonTerminals('<expr-elem> <term> <factor> <pow-expr>')
aritm_expr, comp_expr = G.NonTerminals('<aritm-expr> <comp-expr>')
decl, decls = G.NonTerminals('<decl> <decls>')
id_extend = G.NonTerminal('<id-extend>')

function_, arrow = G.Terminals('function =>')
print_ = G.Terminal('print')
let, asign, in_ = G.Terminals('let = in')
if_, elif_, else_ = G.Terminals('if elif else')
arroba = G.Terminal('@')
plus ,minus, pow_, pow_2, star, div, mod, opar, cpar = G.Terminals('+ - ^ ** * / % ( )')  
and_, or_, not_ = G.Terminals('& | !')  
equals, not_equals, greater, greater_equals, less, less_equals = G.Terminals('== != > >= < <=')  
num, id_, string = G.Terminals('num id string')
okey, ckey = G.Terminals('{ }')
semi, comma, double_dot = G.Terminals('; , :')
sqrt, sin, cos, exp, log, rand = G.Terminals('sqrt sin cos exp log rand')   
e, pi = G.Terminals('E PI')

program %= program + expr + semi
program %= program + function_stat
program %= G.Epsilon

#function_stats %= function_stats + function_stat
#function_stats %= function_stat

function_stat %= function_ + id_ + opar + id_ + cpar + id_extend + body

body %= arrow + expr + semi
body %= okey + expr_list_semi + ckey

params_aux = id_ + id_extend 
params_aux = params_aux + comma + id_ + id_extend

params %= params_aux
params %= G.Epsilon

expr %= let_expr
expr %= print_expr
expr %= expr_elem

print_expr %= print_ + opar + expr + cpar

let_expr %= let + decls + in_ + expr_body

decl %= id_ + id_extend + asign + expr

decls %= decls + comma + decl
decls %= decl

expr_body %= expr 
expr_body %= okey + expr_list_semi + ckey

expr_list_semi %= expr_list_semi + expr + semi
expr_list_semi %= expr + semi

id_extend %= double_dot + id_
id_extend %= G.Epsilon


expr_elem %= expr_elem + arroba + comp_expr
expr_elem %= expr_elem + and_ + comp_expr
expr_elem %= expr_elem + or_ + comp_expr
expr_elem %= not_ + comp_expr
expr_elem %= comp_expr

comp_expr %= comp_expr + equals + aritm_expr
comp_expr %= comp_expr + not_equals + aritm_expr
comp_expr %= comp_expr + greater + aritm_expr
comp_expr %= comp_expr + greater_equals + aritm_expr
comp_expr %= comp_expr + less + aritm_expr
comp_expr %= comp_expr + less_equals + aritm_expr
comp_expr %= aritm_expr

aritm_expr %= aritm_expr + plus + term
aritm_expr %= aritm_expr + minus + term
aritm_expr %= term

term %= term + star + pow_expr
term %= term + div + pow_expr
term %= term + mod + pow_expr
term %= pow_expr

pow_expr %= pow_expr + pow_ + factor
pow_expr %= pow_expr + pow_2 + factor
pow_expr %= factor

factor %= opar + expr_elem + cpar
factor %= num
factor %= id_
factor %= string
factor %= sqrt + opar + expr + cpar
factor %= sin + opar + expr + cpar
factor %= cos + opar + expr + cpar
factor %= exp + opar + expr + cpar
factor %= log + opar + expr + comma + expr + cpar
factor %= rand + opar + cpar
factor %= e
factor %= pi


#region Lexer
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

    (function_,function_.Name),
    (arrow,arrow.Name),

    (arroba,arroba.Name),

    (print_,print_.Name),

    (let,let.Name),
    (asign,asign.Name),
    (in_,in_.Name),

    (if_, if_.Name),
    (elif_,elif_.Name),
    (else_,else_.Name),

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
#endregion

parser = SLR1Parser(G,True)


texts =['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print("Hello World");','print("The message is \"Hello World\"");',
    'print("The meaning of life is " @ 42);','print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));',
    'function tan(x) => sin(x) / cos(x);','function cot(x) => 1 / tan(x);function tan(x) => sin(x) / cos(x);print(tan(PI) ** 2 + cot(PI) ** 2);'
    ]

c=0
for i in texts:
    c+=1
    tokens = lexer(i)
    tokens_type = []
    for j in tokens:
        if j.token_type!='space':
            tokens_type.append(j.token_type)
    if(c==len(texts)):
        print(tokens_type)
    parsed=parser(tokens_type)
    assert parsed!=None




