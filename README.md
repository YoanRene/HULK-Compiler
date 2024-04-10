# HULK-Compiler

## Acerca del proyecto

El objetivo del presente proyecto es desarrollar un compilador para el lenguaje de programación HULK. Para ello se han implementado tres componentes principales: Lexer, Parser y Semantic Checker, así como se ha diseñado una Gramática atributada para dicho lenguaje. Además se han implementado una serie de clases y funciones de apoyo a estos componentes. Durante el desarrollo se siguieron muchas de las ideas planteadas en Conferencia y Clase Práctica, resultando de gran apoyo los Notebook orientados a lo largo del curso, y los archivos que fueron proporcionados junto a ellos.

## Estructura

Para mayor organización se ha dividido el código en diferentes archivos. A continuación se listan los mismos con una breve descripción de su funcionalidad.

- Lexer : Contiene la implementación del Lexer, así como la definición de los tokens.
- ParserLR1 : Contiene la implementación de un Parser LR1.
- ParserSLR1 : Contiene la implementación de un Parser SLR1.
- Semantic_checker : Contiene la implementación del Semantic Checker, incluyendo la definción de los diferentes Nodos del AST.
- HulkGrammar : Contiene la definición de la Gramática Atributada para el lenguaje HULK.
- Automata : Contiene diferentes funciones para el trabajo con Autómatas Finitos. Es uno de los archivos utilizados en las Clases Prácticas.
- Regex : Contiene diversas clases y funciones para el trabajo y evaluación de funciones regulares.
- Visitor : Contiene funciones para el trabajo del recorrido del AST.

### Lexer

Para el Análisis Lexicográfico, se tenía el objetivo de construir un mecanismo que dado una descripción de los tokens que aparecen en el lenguaje, y una cadena de entrada, se devolviera los tokens de la cadena, correctamente etiqueados.

Se optó por el diseño de un Generador de Lexer, de manera que se pudiera tener una estructura lo suficientemente poderosa para que, una vez tener una expresión regular que describa el lenguaje, se construyera el Lexer en base a ella. (En caso contrario hubiera que definir a mano el proceso de tokenización lo cual, no solo hubiera resultado engorroso, sino que fuera poco útil ante cualquier cambio en las reglas del lenguaje). Siguiendo las pautas dadas en las Clases Prácticas y la Bibliografía recomendada, se optó por la utilización de Autómatas Finitos para ello.

Toda la funcionalidad descrita se sintetiza en la clase `Lexer` del archivo `Lexer.py`.

La clase `Lexer` recibe dos argumentos en su constructor: `table` que representa un tipo de token y su respectiva expresión regular, y `eof` que representa el símbolo de final de cadena, para indicar el final de texto.

Se utilizan como apoyo otras clases y funciones definidas en los archivos `Regex` y `Automata` que serán descritos posteriormente.

Además, se definen las siguientes funciones:

- `_build_regexs` : Construye una lista de Autómatas Finitos, en función de la lista de expresiones regulares otorgadas en `table`. Itera por los elementos de `table` y por cada uno, crea una instancia de `Regex` para luego construir su autómata correspondiente. Finalmente, por cada estado final se etiqueta con el tipo de token y con un número que representa la prioridad de dicho token, que sigue el orden inicial de la tabla.

- `_build_automaton` : Combina todos los autómatas anteriores en uno solo, agregando un nuevo estado inicial que se enlaza con los restantes estados iniciales mediante epsilon-transiciones. Al realizar esta operación, se obtiene un Autómata Finito no Determinista, por lo que al final, se utiliza la función `to_deterministic()` para convertirlo en un Autómata Finito Determinista.

- `_walk` : Es la función encargada de recorrer la cadena de entrada y el autómata y devolver el estado final, si se ha llegado a él, con el lexema identificado. El recorrido se realiza de la siguiente manera: dado un símbolo de la cadena, se verifica si el estado actual tiene una transición hacia dicho símbolo, en cuyo caso se mueve la siguiente y agrega dicho símbolo al lexema que se tiene hasta el momento. Si se encuentra un estado final, se actualiza el lexema final, si no existe una transición para el símbolo, finaliza el recorrido.
  
- `_tokenize` : Esta función es la encargada de llamar a `walk` y finalmente devolver los tokens encontrador. Para ello entra en un bucle donde se llama a `walk` para procesar el text y obtener el estado final y su lexema final para el token más largo. En caso de no encontrar estado final, produce el símbolo de fin de archivo y sale del bucle.

- `__call__` : Es la encargada de llamar a `tokenize` y devolver en una lista de objetos `Token`.

### Regex

En el archivo `Regex.py` se definen algunas clases y funciones orientadas a la construcción y evaluación de expresiones regulares. Forma parte de los archivos provistos en los Notebooks orientados a lo largo del curso.

- `evaluate_parse` : Evalúa un conjunto de producciones gramaticales dada una secuencia de tokens. Llama a la función `evaluate` con la primera producción, el resto de producciones y la secuencia de tokens y luego verifica si se ha llegado al final de la cadena, devolviendo el resultado de la evaluación.

- `evaluate` : Realiza la evaluación de una producción específica. Obtiene el símbolo no terminal y la lista de elementos de la producción, así como los atributos asociados a la misma. Se crean dos listas para almacenar tokens y valores heredados. Se recorre la lista de elementos, si el token es terminal, se obtiene el siguiente y se guarda, en caso de que no se obtiene la siguiente producción, el atributo asociado y se aplica una acción semántica para evaluar recursivamente la producción no terminal. Finalmente se obtiene el atributo asociado al inicio de la producción, se aplica una acción semántica final si el atributo existe y se retorna el resultado, o `None` si no hay acción semántica final.

- `regex_tokenizer` : Divide una cadena de texto en tokens basado en la gramática proporcionada. Por defecto omite los espacios en blanco. Procesa una cadena de texto que representa una expresión regular y la convierte en una lista de tokens comprensibles para el analizador de expresiones regulares. Estos tokens representan los elementos básicos que forman la expresión regular.

La clase `Regex` encapsula el concepto de expresión regular y proporciona medios para trabajar con las mismas. En su constructor recibe dos argumentos: `regex` que es la cadena de texto que representa la expresión regular y `skip_whitespaces` que por defecto se encuentra con valor `False`. Se almacena la expresión regular original en el atributo `self.regex` y se llama al método `build_automaton` para construir el Autómata Finito Determinista minimizado a partir de la expresión regular, por último lo guarda en el atributo `self.automaton`.

Dentro de la misma se definen las siguientes funciones:

- `__call__` : Devuelve la respuesta al llamado al método `recognize` que se importa desde `Automata.py` que se explicará posteriormente.

- `build_automaton` : Llama a la función `regex_tokenizer` para convertir la expresióñ regular en una lista de tokens, para luego con ellos construir un Árbol de Análisis Sintáctico (AST) y lo evalúa utilizando la función `evaluate_parse` y obtener un Autómata Finito que representa la expresión regular. Como el autómata resultante será no determinista se llama a la función `nfa_to_dfa` para llevarlo a determinista. Luego se llama a la función `automata_minimization` que dado una serie de pasos, optimiza la cantidad de estados del autómata.

### Automata

En el archivo `Automata.py` se definen diferentes clases y funciones para el trabajo con autómatas finitos y expresiones regulares.

- `move` : Calcula los siguientes estados alcanzables desde un conjunto de estados dado un símbolo.

- `epsilon_closure` : Encuentra las epsilon-clausura de un conjunto de estados del autómata, incluye al estado inicial y todos los estados alcanzables desde él, mediante transiciones epsilon.

- `nfa_to_dfa` : Convierte un Automata Finito No Determinista (AFN) a un Automata Finito Determinista (DFA). Explora cada una de las transiciones posibles con símbolos del vocabulario y considerando el epsilon-clausura para generar los estados del DFA. Evita estados duplicados y valida la construcción de un DFA correcto.

- `distinguish_states` : Identifica si dos estados en un DFA son distinguibles analizando sus transiciones salientes para todos los símbolos del vocabulario. Si dos estados tienen las mismas transiciones salientes para cada símbolo, estarán en la misma clase de equivalencia y se considerarán indistinguibles en términos del lenguaje que aceptan. Es una función de apoyo que es usada en `state_minimization`.

- `state_minimization` : Itera y analiza grupos de estados del DFA, identifica subgrupos de estados verdaderamente indistinguibles y los fusiona en conjuntos únicos dentro de la estructura DisjointSet. El proceso se repite hasta que ya no se puedan realizar más fusiones, lo que indica que se ha obtenido un DFA mínimo con el menor número posible de estados equivalentes.

- `automata_minimization` : Utiliza la función `state_minimization` para construir el DFA con menor cantidad de estados posible. 

- `automata_union` : Representa la Unión entre Autómatas, creando un nuevo Autómata que puede seguir las transiciones tanto del autómata 1 como del autómata 2, reconociendo ambos lenguajes.

- `automata_closure` : Crea un nuevo AFN que permite procesar el lenguaje original de a1 cero o más veces (Clausura de Kleene).

- `automata_concatenation` :  Representa la concatenación de los respectivos lenguajes de los autómatas de entrada. 

En el archivo `Automata.py` también se encuentran las definiciones de las clases utilizadas en muchas de las funciones anteriormente mencionadas. A continuación se listan las mismas con una breve descripción de su funcionalidad

- `NFA` : Encapsula la definición de Autómata Finito no Determinista. Almacena sus componentes esenciales: número total de estados, estado inicial, conjunto de estados finales, y un diccionario que mapea las transiciones. También calcula el alfabeto utilizado y ofrece métodos varios para el trabajo con el autómata, como verificar transiciones epsilon.

- `DFA` : La clase DFA hereda de NFA y representa un Autómata Finito Determinista (DFA). Almacena estados, estados finales, transiciones y el estado inicial. Sin embargo, un DFA tiene restricciones: las transiciones solo pueden llevar a un único estado destino para cada símbolo, y la longitud del símbolo de entrada debe ser mayor a cero. La clase también mantiene un estado actual que se va modificando a medida que se procesa una cadena de entrada.

- `Token` : Representación del concepto de Token.

- `State` : Representa un estado en un autómata finito, con atributos como identificador, si es final, transiciones, formato personalizado y forma visual. Ofrece métodos para: agregar y consultar transiciones, reconocer cadenas, convertir a DFA, crear desde un NFA, obtener el epsilon-closure e iterar sobre el estado y sus transiciones.

### Parser

En el proyecto se encuentran las implementaciones para los Parser LR(1) Canónico y SLR(1). En principio, el proyecto se pensó con el primero de estos, sin embargo se decidió hacer la segunda implementación debido a la demora en que resultaba la construcción del Parser. A continuación, una breve explicación de cada uno, su funcionamiento y las ideas seguidas para sus respectivas implementaciones.

#### Parser LR(1)

Un parser LR(1) canónico es un tipo de analizador sintáctico ascendente utilizado en la construcción de compiladores e intérpretes. Funciona construyendo una tabla de análisis a partir de la gramática y utilizando esta tabla para guiar el proceso de análisis. La tabla de análisis se construye aplicando el algoritmo canónico LR(1) a la gramática de entrada. Este algoritmo calcula los conjuntos de núcleos LR(1) canónicos, que representan los posibles estados del analizador. Para cada estado, la tabla indica qué acción tomar (desplazar, reducir o aceptar) en función del siguiente símbolo de entrada y el núcleo LR(1). Durante el análisis, el parser mantiene una pila que contiene una secuencia de estados. Inicialmente, la pila contiene solo el estado inicial. Luego, en cada paso, el parser consulta la tabla de análisis usando el estado en la cima de la pila y el siguiente símbolo de entrada. La acción indicada por la tabla se realiza de la siguiente manera, Desplazar, Reducir, Aceptar, se apila el nuevo estado y se consume el símbolo de entrada, se reemplaza la parte superior de la pila con el lado derecho de la producción, aplicando la regla de la gramática. Se apila el nuevo estado correspondiente y se acepta la cadena de entrada si la pila contiene el estado de aceptación, respectivamente.

Para su implementación se siguieron las siguientes ideas:

Para la construcción del Autómata LR(1) se utilizan las siguientes funciones:

- `closure_lr1` : Calcula el cierre LR(1) de un conjunto de items, aplicando las reglas de expansión y agregando los conjuntos de continuación (lookaheads).
  
- `goto_lr1` : Calcula el conjunto de items resultante de hacer una transición desde un conjunto de items dado con un símbolo específico.
  
- `build_LR1_automaton` : Construye el autómata LR(1) canónico a partir de la gramática, calculando los conjuntos de núcleos LR(1) y las transiciones entre ellos.

Para la construcción de la tabla de análisis, se aumenta la gramática agregando un nuevo símbolo inicial. Se construye el autómata LR(1) canónico utilizando `build_LR1_automaton`. Se recorren los estados del autómata y registra las acciones de desplazamiento, reducción y aceptación en las tablas `self.action` y `self.goto`.

El método `__call__` de `ShiftReduceParser` implementa el algoritmo de análisis LR(1) utilizando las tablas construidas. Mantiene una pila de estados y, en cada paso, consulta las tablas para determinar la acción a realizar (desplazar, reducir o aceptar) según el estado actual y el siguiente símbolo de entrada. En resumen, este código implementa la construcción del autómata LR(1) canónico y la tabla de análisis correspondiente, así como el proceso de análisis de cadenas de entrada utilizando dicha tabla.
