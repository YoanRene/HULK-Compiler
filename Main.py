from HulkGrammar import *
from Automata import *
from Lexer import *
from Parser import *
from Grammar import *
from ParserLR1 import *
from Regex import *
from Semantic_checker import *
from Visitor import *
from ParserSLR1 import *

def init():

    G,lexer= HulkGrammar()
    parser = SLR1Parser(G,True)

    text_good = 'function tan(x: Number): Number => sin(x) / cos(x); function cot(x) => 1 / tan(x); function operate(x, y) {print(x + y); print(x - y); print(x * y); print(x / y);}  function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2); function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;function gcd(a, b) => while (a > 0) let m = a / b in { b := a; a := m; }; protocol Hashable { hash(): Number;} protocol Equatable extends Hashable { equals(other: Object): Boolean;} protocol Iterable { next() : Boolean; current() : Object;} type Range(min:Number, max:Number) {min = min; max = max; current = min - 1; next(): Boolean => (self.current := self.current + 1) < self.max; current(): Number => self.current; } type Point(x,y) { x = x; y = y; getX() => self.x; getY() => self.y; setX(x) => self.x := x; setY(y) => self.y := y;} type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) { rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);} type Knight inherits Person { name() => "Sir" @@ base();} type Person(firstname, lastname) { firstname = firstname; lastname = lastname; name() => self.firstname @@ self.lastname; hash() : Number { 5;}} type Superman {} type Bird {} type Plane {} type A { hello() => print("A");} type B inherits A { hello() => print("B");} type C inherits A {hello() => print("C");} {42; print(42); print((((1 + 2) ^ 3) * 4) / 5); print("Hello World"); print("The message is \"Hello World\""); print("The meaning of life is " @ 42); print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64))); {print(42); print(sin(PI/2)); print("Hello World");} print(tan(PI) ** 2 + cot(PI) ** 2); let msg = "Hello World" in print(msg); let number = 42, text = "The meaning of life is" in print(text @ number); let number = 42 in let text = "The meaning of life is" in print(text @ number); let number = 42 in ( let text = "The meaning of life is" in ( print(text @ number))); let a = 6, b = a * 7 in print(b); let a = 6 in let b = a * 7 in print(b); let a = 5, b = 10, c = 20 in { print(a+b); print(b*c); print(c/a);}; let a = (let b = 6 in b * 7) in print(a); print(let b = 6 in b * 7); let a = 20 in { let a = 42 in print(a); print(a);}; let a = 7, a = 7 * 6 in print(a); let a = 7 in let a = 7 * 6 in print(a); let a = 0 in { print(a); a := 1; print(a);}; let a = 0 in let b = a := 1 in { print(a); print(b);}; let a = 42 in if (a % 2 == 0) print("Even") else print("odd"); let a = 42 in if (a % 2 == 0) { print(a); print("Even");} else print("Odd");  for (x in range(0, 10)) print(x); let iterable = range(0, 10) in while (iterable.next()) let x = iterable.current() in print(x); let pt = new Point() in print("x: " @ pt.getX() @ "; y: " @ pt.getY()); let pt = new Point(3,4) in print("x: " @ pt.getX() @ "; y: " @ pt.getY()); let pt = new PolarPoint(3,4) in print("rho: " @ pt.rho()); let p = new Knight("Phil", "Collins") in print(p.name()); let p: Person = new Knight("Phil", "Collins") in print(p.name()); let x: Number = 42 in print(x);  let x = 42 in print(x);  let x : A = if (rand() < 0.5) new B() else new C() in if (x is B) let y : B = x as B in { y.hello();} else { print("x cannot be downcasted to B");}; let numbers = [1,2,3,4,5,6,7,8,9] in for (x in numbers) print(x); let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]); let squares = [x^2 || x in range(1,10)] in print(x); let x : Hashable = new Person() in print(x.hash()); let x : Hashable = new Point(0,0) in print(x.hash());}'
    text_bad = 'let a = 42, let mod = a % 3 in print( if (mod == 0) "Magic" elif (mod % 3 == 1) "Woke" else "Dumb"); let a = 42 in print(if (a % 2 == 0) "even" else "odd"); let a = 10 in while (a >= 0) { print(a); a := a - 1;} let total = { print("Total"); 5; } + 6 in print(total); let x = new Superman() in print( if (x is Bird) "It is bird!" elif (x is Plane) "It is a plane!" else "No, it is Superman!");'
    texts =[#'42;' ,'print(42);','print((((1 + 2) ^ 3) * 4) / 5);','print("Hello World");','print("The message is \"Hello World\"");',
    #'print("The meaning of life is " @ 42);','print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64)));',
    #'function tan(x) => sin(x) / cos(x);','function cot(x) => 1 / tan(x);function tan(x) => sin(x) / cos(x);print(tan(PI) ** 2 + cot(PI) ** 2);',
    #'function operate(x, y) {print(x + y);print(x - y);print(x * y);print(x / y);}',
    #'let msg = "Hello World" in print(msg);','let number = 42, text = "The meaning of life is" in print(text @ number);',
    #'let number = 42 in let text = "The meaning of life is" in print(text @ number);',
    #'let number = 42 in (let text = "The meaning of life is" in (print(text @ number)));',
    #'let a = 6, b = a * 7 in print(b);','let a = 6 in let b = a * 7 in print(b);',
    #'let a = 5, b = 10, c = 20 in {print(a+b);print(b*c);print(c/a);};','let a = (let b = 6 in b * 7) in print(a);',
    #'print(let b = 6 in b * 7);','let a = 20 in {let a = 42 in print(a);print(a);};','let a = 7, a = 7 * 6 in print(a);',
    #'let a = 7 in let a = 7 * 6 in print(a);','let a = 0 in {print(a);a := 1;print(a);};',
    #'let a = 0 in let b = a := 1 in {print(a);print(b);};',
    #'let a = 42 in if (a % 2 == 0) print("Even") else print("odd");',
    #'while(5){print("hola");};',
    #'while(x==1){print("hola");};',
    #'if(5){print("hola");}else{print("la");};',
    #'if(x==1){print("hola");}else{print("la");};',
    #'(a & b) == (b & c);',
    #'print("The message is \\"Hello World\\"");',
    text_good
    #'function tan(x: Number): Number => sin(x) / cos(x); function cot(x) => 1 / tan(x); function operate(x, y) {print(x + y); print(x - y); print(x * y); print(x / y);}  function fib(n) => if (n == 0 | n == 1) 1 else fib(n-1) + fib(n-2); function fact(x) => let f = 1 in for (i in range(1, x+1)) f := f * i;function gcd(a, b) => while (a > 0) let m = a / b in { b := a; a := m; }; protocol Hashable { hash(): Number;} protocol Equatable extends Hashable { equals(other: Object): Boolean;} protocol Iterable { next() : Boolean; current() : Object;} type Range(min:Number, max:Number) {min = min; max = max; current = min - 1; next(): Boolean => (self.current := self.current + 1) < self.max; current(): Number => self.current; } type Point(x,y) { x = x; y = y; getX() => self.x; getY() => self.y; setX(x) => self.x := x; setY(y) => self.y := y;} type PolarPoint(phi, rho) inherits Point(rho * sin(phi), rho * cos(phi)) { rho() => sqrt(self.getX() ^ 2 + self.getY() ^ 2);} type Knight inherits Person { name() => "Sir" @@ base();} type Person(firstname, lastname) { firstname = firstname; lastname = lastname; name() => self.firstname @@ self.lastname; hash() : Number { 5;}} type Superman {} type Bird {} type Plane {} type A { hello() => print("A");} type B inherits A { hello() => print("B");} type C inherits A {hello() => print("C");} {42; print(42); print((((1 + 2) ^ 3) * 4) / 5); print("Hello World"); print("The message is \"Hello World\""); print("The meaning of life is " @ 42); print(sin(2 * PI) ^ 2 + cos(3 * PI / log(4, 64))); {print(42); print(sin(PI/2)); print("Hello World");} print(tan(PI) ** 2 + cot(PI) ** 2); let msg = "Hello World" in print(msg); let number = 42, text = "The meaning of life is" in print(text @ number); let number = 42 in let text = "The meaning of life is" in print(text @ number); let number = 42 in ( let text = "The meaning of life is" in ( print(text @ number))); let a = 6, b = a * 7 in print(b); let a = 6 in let b = a * 7 in print(b); let a = 5, b = 10, c = 20 in { print(a+b); print(b*c); print(c/a);}; let a = (let b = 6 in b * 7) in print(a); print(let b = 6 in b * 7); let a = 20 in { let a = 42 in print(a); print(a);}; let a = 7, a = 7 * 6 in print(a); let a = 7 in let a = 7 * 6 in print(a); let a = 0 in { print(a); a := 1; print(a);}; let a = 0 in let b = a := 1 in { print(a); print(b);}; let a = 42 in if (a % 2 == 0) print("Even") else print("odd"); let a = 42 in print(if (a % 2 == 0) "even" else "odd"); let a = 42 in if (a % 2 == 0) { print(a); print("Even");} else print("Odd"); let a = 42, let mod = a % 3 in print( if (mod == 0) "Magic" elif (mod % 3 == 1) "Woke" else "Dumb");  for (x in range(0, 10)) print(x); let iterable = range(0, 10) in while (iterable.next()) let x = iterable.current() in print(x); let pt = new Point() in print("x: " @ pt.getX() @ "; y: " @ pt.getY()); let pt = new Point(3,4) in print("x: " @ pt.getX() @ "; y: " @ pt.getY()); let pt = new PolarPoint(3,4) in print("rho: " @ pt.rho()); let p = new Knight("Phil", "Collins") in print(p.name()); let p: Person = new Knight("Phil", "Collins") in print(p.name()); let x: Number = 42 in print(x); let x = new Superman() in print( if (x is Bird) "It is bird!" elif (x is Plane) "It is a plane!" else "No, it is Superman!"); let x = 42 in print(x); let total = { print("Total"); 5; } + 6 in print(total); let x : A = if (rand() < 0.5) new B() else new C() in if (x is B) let y : B = x as B in { y.hello();} else { print("x cannot be downcasted to B");}; let numbers = [1,2,3,4,5,6,7,8,9] in for (x in numbers) print(x); let numbers = [1,2,3,4,5,6,7,8,9] in print(numbers[7]); let squares = [x^2 || x in range(1,10)] in print(x); let x : Hashable = new Person() in print(x.hash()); let x : Hashable = new Point(0,0) in print(x.hash());}'
    ]


    parserslist = []
    operationslist=[]
    tokenslist = []

    c=0
    for i in texts:
        c+=1
        tokens = lexer(i)
        tokenslist.append(tokens)
        tokens_type = []
        for j in tokens:
            if j.token_type!='space':
                tokens_type.append(j.token_type)
        if(c==len(texts)):
            print(tokens_type)
        parse,operations = parser(tokens_type, get_shift_reduce=True)
        parserslist.append(parse)
        operationslist.append(operations)

    astlist = []

    for j in range(len(parserslist)):
        new_tokens = []

        for i in tokenslist[j]:
            if(i.token_type!='space'):
                new_tokens.append(i)

        #region Semantic Checker
        ast = evaluate_reverse_parse(parserslist[j], operationslist[j], new_tokens)
        astlist.append(ast)


    formatter = FormatVisitor()
    for i in range(len(astlist)):
        print(formatter.visit(astlist[i]))

    scope = Scope()

    for i in range(len(astlist)):

        semantic_checker = SemanticCheckerVisitor()
        errors = semantic_checker.visit(astlist[i])
        for j, error in enumerate(errors,1):
            print(texts[i])
            print(f'{j}.', error)

    #endregion
    

init()