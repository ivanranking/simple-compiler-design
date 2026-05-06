# SimpleScript Language Specification

## Overview
SimpleScript is a simple imperative programming language with basic data types, control flow, and functions.

## Data Types
- `int` - Integer numbers
- `float` - Floating-point numbers  
- `string` - Text strings
- `boolean` - True/False values

## Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `and`, `or`, `not`
- **Assignment**: `=`

## Keywords
- `var` - Variable declaration
- `if`, `else` - Conditional
- `for`, `while` - Loops
- `break`, `continue` - Loop control
- `function` - Function declaration
- `return` - Function return
- `input` - Read from user
- `print` - Output
- `true`, `false` - Boolean literals

## Grammar (EBNF)

```
program     ::= (declaration | statement)*
declaration ::= var_decl | func_decl
var_decl    ::= 'var' IDENTIFIER ('=' expression)? ';'
func_decl   ::= 'function' IDENTIFIER '(' params? ')' '{' statement* '}'
params      ::= IDENTIFIER (',' IDENTIFIER)*

statement   ::= expr_stmt | if_stmt | while_stmt | for_stmt | block | return_stmt | print_stmt | input_stmt | break_stmt | continue_stmt

expr_stmt   ::= expression ';'
if_stmt     ::= 'if' '(' expression ')' statement ('else' statement)?
while_stmt  ::= 'while' '(' expression ')' statement
for_stmt    ::= 'for' '(' expr_stmt expression ';' expression ')' statement
block       ::= '{' statement* '}'
return_stmt ::= 'return' expression? ';'
print_stmt  ::= 'print' '(' expression (',' expression)* ')' ';'
input_stmt  ::= 'input' '(' IDENTIFIER ')' ';'
break_stmt  ::= 'break' ';'
continue_stmt ::= 'continue' ';'

expression  ::= assignment
assignment  ::= logical_or ('=' assignment)?
logical_or  ::= logical_and ('or' logical_and)*
logical_and ::= equality ('and' equality)*
equality    ::= comparison (('==' | '!=') comparison)*
comparison  ::= additive (('<' | '>' | '<=' | '>=') additive)*
additive    ::= multiplicative (('+' | '-') multiplicative)*
multiplicative ::= unary (('*' | '/' | '%') unary)*
unary       ::= ('not' | '-')? postfix
postfix     ::= call
call        ::= primary ('(' arguments? ')')*
primary     ::= NUMBER | STRING | IDENTIFIER | 'true' | 'false' | '(' expression ')'

arguments   ::= expression (',' expression)*
```

## Example Program

```
function add(a, b) {
    return a + b;
}

var x = 10;
var y = 20;
var result = add(x, y);
print("Result: ", result);

if (result > 20) {
    print("Greater than 20");
} else {
    print("Not greater than 20");
}

for (var i = 0; i < 5; i = i + 1) {
    print("Iteration ", i);
}
```
