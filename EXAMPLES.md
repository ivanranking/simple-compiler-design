# SimpleScript Compiler - Complete Walkthrough Examples

This document provides detailed, step-by-step examples of how the compiler processes different types of code.

---

## Example 1: Simple Variable Declaration

### Source Code
```javascript
var x = 42;
print(x);
```

### Phase 1: Lexical Analysis

**Tokenization Process**:
```
Input characters: v a r   x   =   4 2 ; p r i n t ( x ) ;

Recognized tokens:
┌─────────────────────┬──────┬──────┬────────┐
│ Token Type          │ Value│ Line │ Column │
├─────────────────────┼──────┼──────┼────────┤
│ VAR                 │ var  │ 1    │ 1      │
│ IDENTIFIER          │ x    │ 1    │ 5      │
│ ASSIGN              │ =    │ 1    │ 7      │
│ INTEGER             │ 42   │ 1    │ 9      │
│ SEMICOLON           │ ;    │ 1    │ 11     │
│ IDENTIFIER (print)  │ print│ 2    │ 1      │
│ LPAREN              │ (    │ 2    │ 6      │
│ IDENTIFIER          │ x    │ 2    │ 7      │
│ RPAREN              │ )    │ 2    │ 8      │
│ SEMICOLON           │ ;    │ 2    │ 9      │
│ EOF                 │ null │ 2    │ 10     │
└─────────────────────┴──────┴──────┴────────┘
```

### Phase 2: Syntax Analysis (Parsing)

**Grammar Rules Applied**:
```
1. program → declaration*
   → [VarDecl, ExprStmt]

2. VarDecl → 'var' IDENTIFIER ('=' expression)? ';'
   → var x = 42 ;
   
   Match: var ✓, x ✓, = ✓
   
   expression → assignment → logical_or → ... → primary
   → Literal(42, 'integer')
   
   Result: VarDecl(name='x', initializer=Literal(42))

3. ExprStmt → expression ';'
   
   expression → assignment → ... → postfix → call
   → Call(
       function=Identifier('print'),
       arguments=[Identifier('x')]
     )
   
   Result: ExprStmt(
     expression=Call(
       function=Identifier('print'),
       arguments=[Identifier('x')]
     )
   )
```

**Generated AST**:
```
Program(
  statements=[
    VarDecl(
      name='x',
      initializer=Literal(value=42, type='integer')
    ),
    ExprStmt(
      expression=Call(
        function=Identifier(name='print'),
        arguments=[Identifier(name='x')]
      )
    )
  ]
)
```

### Phase 3: Semantic Analysis

**Symbol Table Creation**:
```
Global Scope:
├─ 'print' (built-in function)
├─ 'input'  (built-in function)

Analysis Step 1: Process VarDecl('x')
  • Check: Is 'x' already in current scope? NO ✓
  • Infer type: initializer is Literal(42, 'integer') → type is 'int'
  • Create symbol: Symbol(name='x', type='int', is_initialized=True)
  • Add to scope: Global Scope now contains 'x'

Updated Global Scope:
├─ 'print' (built-in)
├─ 'input'  (built-in)
└─ 'x'      : int (initialized)

Analysis Step 2: Process ExprStmt(Call(...))
  • Call: function=Identifier('print'), arguments=[Identifier('x')]
  • Check: Is 'print' defined? YES ✓ (built-in)
  • Check: Is 'print' a function? YES ✓
  • Check argument count: expects ≥0, got 1 ✓
  
  • Inner expression: Identifier('x')
  • Check: Is 'x' defined? YES ✓
  • Check: Is 'x' initialized? YES ✓
  • Type: 'int' ✓

Validation Result: SUCCESS ✓
```

### Phase 4: Interpretation

**Execution Steps**:
```
1. Initialize runtime
   Global scope (runtime): {}

2. Execute VarDecl('x')
   a. Evaluate initializer: Literal(42, 'integer') → 42
   b. Create variable: Global['x'] = 42
   
   Global scope after: {x: 42}

3. Execute ExprStmt(Call(...))
   a. Evaluate Call expression
      i.   Get function: Identifier('print')
           → Built-in print function
      ii.  Evaluate arguments: [Identifier('x')]
           → Look up 'x' in scope: 42
           → Arguments: [42]
      iii. Call built-in print(42)
           → Output: "42"
           → Return: None

Final Output: 42
```

---

## Example 2: Control Flow (If-Else)

### Source Code
```javascript
var age = 20;
if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}
```

### Lexical Analysis Output
```
Tokens (simplified):
VAR, IDENTIFIER(age), ASSIGN, INTEGER(20), SEMICOLON,
IF, LPAREN, IDENTIFIER(age), GREATER_EQUAL, INTEGER(18), RPAREN,
LBRACE,
PRINT, LPAREN, STRING("Adult"), RPAREN, SEMICOLON,
RBRACE,
ELSE,
LBRACE,
PRINT, LPAREN, STRING("Minor"), RPAREN, SEMICOLON,
RBRACE
```

### Parsing Result
```
Program(
  statements=[
    VarDecl(
      name='age',
      initializer=Literal(20, 'integer')
    ),
    IfStmt(
      condition=Binary(
        left=Identifier('age'),
        operator='>=',
        right=Literal(18, 'integer')
      ),
      then_branch=Block(
        statements=[
          PrintStmt(
            arguments=[Literal("Adult", 'string')]
          )
        ]
      ),
      else_branch=Block(
        statements=[
          PrintStmt(
            arguments=[Literal("Minor", 'string')]
          )
        ]
      )
    )
  ]
)
```

### Semantic Analysis
```
1. Validate VarDecl: age is int, initialized ✓

2. Validate IfStmt:
   a. Condition type check:
      Binary(
        left: Identifier('age') → type: int
        operator: >= (comparison operator)
        right: Literal(18) → type: int
      )
      → Comparison result type: boolean ✓
   
   b. Then-branch validation:
      PrintStmt with string literal ✓
   
   c. Else-branch validation:
      PrintStmt with string literal ✓

Result: VALID ✓
```

### Execution
```
Runtime Execution:

1. Execute VarDecl:
   Global scope: {age: 20}

2. Execute IfStmt:
   a. Evaluate condition:
      Binary(left=Identifier('age'), op='>=', right=18)
      → Get age: 20
      → Evaluate: 20 >= 18 → true
      
   b. Condition is truthy:
      → Execute then_branch
      
   c. Execute Block (then_branch):
      Push new scope
      
   d. Execute PrintStmt:
      → Print "Adult"
      
   e. Pop scope
      
   f. Skip else_branch

Output: "Adult"
```

---

## Example 3: Loop with Increment

### Source Code
```javascript
for (var i = 0; i < 3; i = i + 1) {
    print("Iteration: ", i);
}
```

### Parsing Structure
```
ForStmt(
  initializer=VarDecl(
    name='i',
    initializer=Literal(0, 'integer')
  ),
  condition=Binary(
    left=Identifier('i'),
    operator='<',
    right=Literal(3, 'integer')
  ),
  increment=Assignment(
    target='i',
    value=Binary(
      left=Identifier('i'),
      operator='+',
      right=Literal(1, 'integer')
    )
  ),
  body=Block(
    statements=[
      PrintStmt(arguments=[
        Literal("Iteration: ", 'string'),
        Identifier('i')
      ])
    ]
  )
)
```

### Execution Flow
```
Loop Execution Trace:

1. Create loop scope
   Push new scope: Loop_1

2. Execute initializer:
   VarDecl(i = 0)
   Loop_1: {i: 0}

3. ITERATION 1:
   a. Check condition: i < 3
      Evaluate: 0 < 3 → true ✓
   
   b. Execute body:
      PrintStmt("Iteration: ", i)
      → print("Iteration: " + str(0))
      → Output: "Iteration: 0"
   
   c. Execute increment: i = i + 1
      Evaluate: 0 + 1 = 1
      Loop_1: {i: 1}

4. ITERATION 2:
   a. Check condition: i < 3
      Evaluate: 1 < 3 → true ✓
   
   b. Execute body:
      → Output: "Iteration: 1"
   
   c. Execute increment:
      Loop_1: {i: 2}

5. ITERATION 3:
   a. Check condition: i < 3
      Evaluate: 2 < 3 → true ✓
   
   b. Execute body:
      → Output: "Iteration: 2"
   
   c. Execute increment:
      Loop_1: {i: 3}

6. Check condition again: i < 3
   Evaluate: 3 < 3 → false ✗
   → Exit loop

7. Pop loop scope

Final Output:
Iteration: 0
Iteration: 1
Iteration: 2
```

---

## Example 4: Function Definition and Call

### Source Code
```javascript
function greet(name) {
    print("Hello, ", name);
}

greet("Alice");
```

### Parsing Structure
```
Program(
  statements=[
    FuncDecl(
      name='greet',
      params=['name'],
      body=[
        PrintStmt(arguments=[
          Literal("Hello, ", 'string'),
          Identifier('name')
        ])
      ]
    ),
    ExprStmt(
      expression=Call(
        function=Identifier('greet'),
        arguments=[Literal("Alice", 'string')]
      )
    )
  ]
)
```

### Semantic Analysis
```
1. Process FuncDecl:
   a. Add to global scope: Symbol(
        name='greet',
        type='function',
        params=['name']
      )
   
   b. Create function scope
      Push scope with param 'name'
      
   c. Validate function body:
      PrintStmt: ✓
      
   d. Pop function scope

2. Process ExprStmt/Call:
   a. Look up 'greet' in scope: EXISTS ✓
   
   b. Check is function: type='function' ✓
   
   c. Check param count: expects 1, got 1 ✓
   
   d. Check argument type: String → compatible ✓
```

### Execution
```
1. Process FuncDecl:
   Global scope: {greet: <function object>}

2. Process ExprStmt/Call:
   a. Evaluate Call(greet, ["Alice"])
      i.   Look up function: greet
      ii.  Evaluate arguments:
           Literal("Alice", 'string') → "Alice"
      iii. Create function call:
           • Push new scope (call frame)
           • Bind parameters:
             FuncScope: {name: "Alice"}
           • Execute function body
           
   b. Execute body (in FuncScope):
      PrintStmt("Hello, ", name)
      → Look up 'name': "Alice"
      → Output: "Hello, Alice"
   
   c. Function returns (no explicit return)
      → Pop scope
   
   d. Call expression result: None

Output: "Hello, Alice"
```

---

## Example 5: Type Error Detection

### Source Code
```javascript
var message = "test";
var result = message + 5;
```

### Lexical Analysis
```
Tokens: VAR, IDENTIFIER(message), ASSIGN, STRING("test"), SEMICOLON,
        VAR, IDENTIFIER(result), ASSIGN, IDENTIFIER(message), PLUS, INTEGER(5), SEMICOLON
```

### Parsing
```
Program(
  statements=[
    VarDecl(
      name='message',
      initializer=Literal("test", 'string')
    ),
    VarDecl(
      name='result',
      initializer=Binary(
        left=Identifier('message'),
        operator='+',
        right=Literal(5, 'integer')
      )
    )
  ]
)
```

### Semantic Analysis (FAILS)
```
1. Process first VarDecl:
   Symbol(name='message', type='string', value="test") ✓

2. Process second VarDecl:
   a. Evaluate initializer type:
      Binary(
        left=Identifier('message'),
        operator='+',
        right=Literal(5, 'integer')
      )
      
   b. Type check Binary operator '+':
      • Left operand: Identifier('message')
        → Look up 'message': type='string'
      
      • Operator: '+'
        → Check if valid for (string, int)
        → Arithmetic operator requires (int|float, int|float)
        → TYPE MISMATCH!
      
      ✗ SEMANTIC ERROR:
        "Cannot apply + to string and integer"
        at line 2, column 19
```

**Compiler Output**:
```
{
  "success": false,
  "error": "Semantic Error: Cannot apply + to string and integer",
  "tokens": [...],
  "ast": "...",
  "output": ""
}
```

---

## Example 6: Complex Expression Evaluation

### Source Code
```javascript
var a = 10;
var b = 20;
var c = a + b * 2 - 5 / 2;
print(c);
```

### Operator Precedence Parsing

**Tokens**: IDENTIFIER(a), INTEGER(10), IDENTIFIER(b), INTEGER(20), IDENTIFIER(a), ...

**AST Generation** (showing precedence):
```
Binary(
  left=Binary(
    left=Identifier('a'),
    operator='+',
    right=Binary(
      left=Identifier('b'),
      operator='*',
      right=Literal(2, 'integer')
    )
  ),
  operator='-',
  right=Binary(
    left=Literal(5, 'integer'),
    operator='/',
    right=Literal(2, 'integer')
  )
)
```

**Evaluation Order**:
```
Expression tree with parentheses equivalent:
((a + (b * 2)) - (5 / 2))

Step 1: Evaluate rightmost first (recursive)
  a. b * 2 = 20 * 2 = 40
  b. 5 / 2 = 5 / 2 = 2 (integer division)
  
Step 2: Evaluate middle levels
  c. a + 40 = 10 + 40 = 50
  
Step 3: Evaluate top level
  d. 50 - 2 = 48

Final result: c = 48
```

---

## Example 7: Runtime Error (Undefined Variable)

### Source Code
```javascript
print(undefined_var);
```

### Compilation Phases

**Phase 1-3**: Parsing and semantic analysis succeed
- Identifier('undefined_var') is valid syntax
- Semantic analyzer cannot validate undefined variables
  (they might be defined at runtime in some languages)

**Phase 4: Runtime Execution**
```
1. Execute ExprStmt(Call(...))
2. Evaluate argument: Identifier('undefined_var')
3. Look up variable in scope:
   - Check current (global) scope: NO
   - Check parent scopes: NONE
   → Variable not found!
   ✗ RUNTIME ERROR:
     "Undefined variable 'undefined_var'"
```

**Error Output**:
```
{
  "success": false,
  "error": "Runtime Error: Undefined variable 'undefined_var'",
  "output": ""
}
```

---

## Example 8: Scope Management

### Source Code
```javascript
var x = 10;

function test() {
    var x = 20;
    print("In function: ", x);
}

test();
print("Global: ", x);
```

### Scope Diagram
```
Global Scope: {x: 10, test: <function>}
    ↓
    └─ Function 'test' creates local scope
       Local Scope: {x: 20}
       
When inside function: look up 'x'
  • Check local scope first: found! x = 20
  • Use local value
  
When outside function: look up 'x'
  • Check global scope: found! x = 10
  • Use global value
```

### Execution Trace
```
1. Global execution:
   Global: {x: 10, test: <function>}
   
2. Function declaration:
   Function stored in global scope
   
3. Call test():
   Push function scope
   Local: {x: 20, test: <function>(inherited)}
   
4. Print in function:
   Identifier('x') → Look up in local scope → 20
   Output: "In function: 20"
   
5. Pop function scope
   Back to Global: {x: 10, test: <function>}
   
6. Print in global:
   Identifier('x') → Look up in global scope → 10
   Output: "Global: 10"
```

**Full Output**:
```
In function: 20
Global: 10
```

---

## Summary: Complete Compilation Process

For any SimpleScript program:

```
Source Code (Text)
        ↓
    LEXER
        ↓
Token Stream
        ↓
    PARSER
        ↓
Abstract Syntax Tree (AST)
        ↓
SEMANTIC ANALYZER
        ↓
Validated AST (or Error)
        ↓
  INTERPRETER
        ↓
Program Output (or Runtime Error)
```

Each phase **adds value**:
- **Lexer**: Recognizes language structure
- **Parser**: Validates grammar and builds hierarchy
- **Semantic Analyzer**: Catches type and scope errors early
- **Interpreter**: Executes the program

This modular approach makes the compiler:
- **Educational**: Easy to learn each phase separately
- **Maintainable**: Changes are localized
- **Extensible**: New features follow the same pattern
- **Debuggable**: Errors are clear and localized

---

**Understanding these examples deeply will give you mastery over compiler design!**
