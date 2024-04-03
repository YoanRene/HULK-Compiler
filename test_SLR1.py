from Grammar import Grammar
from Lexer import Lexer
from ParserSLR1 import SLR1Parser

G=Grammar()

program = G.NonTerminal('<program>',True)

expr = G.NonTerminal('<expr>')

body = G.NonTerminal('<body>')
function_stats, function_stat, params, params_aux= G.NonTerminals('<function-stats> <function> <params> <params-aux>')
let_expr,if_expr,print_expr, destr_expr, while_expr, for_expr  = G.NonTerminals('<let-expr> <if-expr> <print-expr> <destr-expr> <while-expr> <for-expr>')
elif_expr, else_expr = G.NonTerminals('<elif-expr> <else-expr>')
expr_body, expr_list_semi = G.NonTerminals('<expr-body> <expr-list-semi>')
expr_elem, term, factor, pow_expr = G.NonTerminals('<expr-elem> <term> <factor> <pow-expr>')
aritm_expr, comp_expr = G.NonTerminals('<aritm-expr> <comp-expr>')
decl, decls = G.NonTerminals('<decl> <decls>')
id_extend = G.NonTerminal('<id-extend>')
args, args_aux, args_in_par = G.NonTerminals('<args> <args-aux> <args-in-par>')
expr_dot = G.NonTerminal('<expr-dot>')
negative = G.NonTerminal('<negative>')

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
okey, ckey, oindex, cindex = G.Terminals('{ } [ ]')
semi, comma, double_dot, dot = G.Terminals('; , : .')
sqrt, sin, cos, exp, log, rand = G.Terminals('sqrt sin cos exp log rand')   
e, pi = G.Terminals('E PI')

program %= program + expr + semi
program %= program + function_stat
program %= G.Epsilon

function_stat %= function_ + id_ + opar + params + cpar + id_extend + body

body %= arrow + expr + semi
body %= okey + expr_list_semi + ckey

params_aux %= id_ + id_extend 
params_aux %= params_aux + comma + id_ + id_extend

params %= params_aux
params %= G.Epsilon

expr %= let_expr
expr %= if_expr
expr %= for_expr
expr %= while_expr
expr %= print_expr
expr %= destr_expr
expr %= expr_elem

print_expr %= print_ + opar + expr + cpar

let_expr %= let + decls + in_ + expr_body

destr_expr %= id_ + destr + expr

while_expr %=  while_ + opar + expr + cpar + expr_body

for_expr %= for_ + opar + id_ + in_ + expr + cpar + expr_body

if_expr %= if_ + opar + expr + cpar + expr_body + elif_expr

elif_expr %= elif_ + opar + expr + cpar + expr_body + elif_expr
elif_expr %= else_expr

else_expr %= else_ + expr_body

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

pow_expr %= pow_expr + pow_ + negative
pow_expr %= pow_expr + pow_2 + negative
pow_expr %= negative

negative %= minus + factor
negative %= factor

factor %= opar + expr + cpar
factor %= num
factor %= string
factor %= sqrt + opar + expr + cpar
factor %= sin + opar + expr + cpar
factor %= cos + opar + expr + cpar
factor %= exp + opar + expr + cpar
factor %= log + opar + expr + comma + expr + cpar
factor %= rand + opar + cpar
factor %= e
factor %= pi
factor %= factor + dot + id_ + args_in_par
factor %= factor + oindex + expr + cindex
factor %= id_ + args_in_par

args_aux %= expr 
args_aux %= args_aux + comma + expr

args %= args_aux
args %= G.Epsilon

args_in_par %= opar + args + cpar
args_in_par %= G.Epsilon



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
    (dot,dot.Name),

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
#endregion

parser = SLR1Parser(G,True)


texts =['42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print("Hello World");','print("The message is \"Hello World\"");',
    'print("The meaning of life is " @ 42);','print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));',
    'function tan(x) => sin(x) / cos(x);','function cot(x) => 1 / tan(x);function tan(x) => sin(x) / cos(x);print(tan(PI) ** 2 + cot(PI) ** 2);',
    'function operate(x, y) {print(x + y);print(x - y);print(x * y);print(x / y);}',
    'let msg = "Hello World" in print(msg);','let number = 42, text = "The meaning of life is" in print(text @ number);',
    'let number = 42 in let text = "The meaning of life is" in print(text @ number);',
    'let number = 42 in (let text = "The meaning of life is" in (print(text @ number)));',
    'let a = 6, b = a * 7 in print(b);','let a = 6 in let b = a * 7 in print(b);',
    'let a = 5, b = 10, c = 20 in {print(a+b);print(b*c);print(c/a);};','let a = (let b = 6 in b * 7) in print(a);',
    'print(let b = 6 in b * 7);','let a = 20 in {let a = 42 in print(a);print(a);};','let a = 7, a = 7 * 6 in print(a);',
    'let a = 7 in let a = 7 * 6 in print(a);','let a = 0 in {print(a);a := 1;print(a);};',
    'let a = 0 in let b = a := 1 in {print(a);print(b);};',
    'let a = 42 in if (a % 2 == 0) print("Even") else print("odd");',
    #'let a = 42 in print(if (a % 2 == 0) "even" else "odd");',error del lexer
    'let a = 42 in if (a % 2 == 0) {print(a);print("Even");}else print("Odd");',
    #'let a = 42, mod = a % 3 in print( if (mod == 0) "Magic" elif (mod % 3 == 1) "Woke" else "Dumb");' error del lexer 
    'let a = 10 in while (a >= 0) {print(a);a := a - 1;};',
    'function gcd(a, b) => while (a > 0) let m = a % b in {b := a;a := m;};',
    'for (x in range(0, 10)) print(x);'
    'let iterable = range(0, 10) in while (iterable.next()) let x = iterable.current() in print(x);'
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




