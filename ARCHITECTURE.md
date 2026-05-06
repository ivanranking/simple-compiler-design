# SimpleScript Compiler Architecture

## 🏗️ System Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Web Frontend                          │
│  (HTML + CSS + JavaScript with Syntax Highlighting)    │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/JSON
┌─────────────────────────┴────────────────────────────────┐
│              Flask REST API Backend                       │
│              (app.py - Port 5000)                        │
└────────────────────────┬────────────────────────────────┘
                         │
┌─────────────────────────┴────────────────────────────────┐
│           Compiler Pipeline (Sequential)                 │
│                                                          │
│  Phase 1: Lexer.py      → Tokenization                 │
│           ↓                                              │
│  Phase 2: Parser.py     → AST Generation               │
│           ↓                                              │
│  Phase 3: Semantic.py   → Type Checking & Validation   │
│           ↓                                              │
│  Phase 4: Interpreter.py → Code Generation & Execution │
│                                                          │
└─────────────────────────┬────────────────────────────────┘
                         │
┌─────────────────────────┴────────────────────────────────┐
│        Output (Tokens, AST, Output, Errors)             │
└─────────────────────────────────────────────────────────┘
```

## 📊 Detailed Phase Breakdown

### Phase 1: Lexical Analysis (Lexer)

**File**: `backend/lexer.py`

**Purpose**: Convert source code string into a sequence of tokens.

**Key Components**:
- `TokenType` enum - All possible token types (keywords, operators, literals, etc.)
- `Token` dataclass - Represents a single token with type, value, line, column
- `Lexer` class - Main lexical analyzer

**Process**:
```
Source Code String
        ↓
[Character-by-character scanning]
        ↓
Recognize:
  • Whitespace (skip)
  • Comments (// - skip)
  • Keywords (var, if, for, etc.)
  • Identifiers (variable/function names)
  • Literals (numbers, strings)
  • Operators (+, -, ==, etc.)
  • Delimiters ({}, (), ;, ,)
        ↓
Token Stream
```

**Example**:
```
Input:  "var x = 10 + 5;"
Output: [
    Token(VAR, 'var', 1:1),
    Token(IDENTIFIER, 'x', 1:5),
    Token(ASSIGN, '=', 1:7),
    Token(INTEGER, 10, 1:9),
    Token(PLUS, '+', 1:12),
    Token(INTEGER, 5, 1:14),
    Token(SEMICOLON, ';', 1:15),
    Token(EOF, None, 1:16)
]
```

**Error Handling**:
- Unterminated strings
- Invalid characters
- Malformed numbers
- Reports line:column for debugging

---

### Phase 2: Syntax Analysis (Parser)

**File**: `backend/parser.py`

**Purpose**: Transform token stream into an Abstract Syntax Tree (AST).

**Key Components**:
- `ASTNode` - Base class for all AST nodes
- `Statement` subclasses - Program statements (if, for, var, etc.)
- `Expression` subclasses - Expressions (binary ops, literals, calls, etc.)
- `Parser` class - Recursive descent parser

**Grammar Hierarchy** (simplified):
```
Program
  └─ Statement*
      ├─ VarDecl (var x = 10;)
      ├─ FuncDecl (function foo() {...})
      ├─ IfStmt (if (...) {...})
      ├─ WhileStmt (while (...) {...})
      ├─ ForStmt (for (...; ...; ...) {...})
      ├─ Block ({...})
      ├─ ReturnStmt (return ...;)
      ├─ PrintStmt (print(...);)
      ├─ InputStmt (input(...);)
      ├─ BreakStmt
      ├─ ContinueStmt
      └─ ExprStmt (expression;)

Expression (with precedence)
  ├─ Assignment (x = 10)
  ├─ LogicalOr (a or b)
  ├─ LogicalAnd (a and b)
  ├─ Equality (a == b, a != b)
  ├─ Comparison (a < b, a > b, etc.)
  ├─ Additive (a + b, a - b)
  ├─ Multiplicative (a * b, a / b)
  ├─ Unary (-a, not a)
  ├─ Postfix/Call (foo(a, b))
  └─ Primary (42, "hello", x, true, (expr))
```

**Process**:
```
Token Stream
        ↓
[Recursive Descent Parsing]
        ↓
Build hierarchical tree:
  • Match tokens to grammar rules
  • Respect operator precedence
  • Identify statement and expression types
        ↓
Abstract Syntax Tree
```

**Example Parse**:
```
Input tokens: [VAR, x, ASSIGN, 10, PLUS, 5, SEMICOLON]

AST:
  VarDecl(
    name='x',
    initializer=Binary(
      left=Literal(10, 'integer'),
      operator='+',
      right=Literal(5, 'integer')
    )
  )
```

**Error Handling**:
- Missing semicolons
- Mismatched parentheses/braces
- Invalid statement syntax
- Unexpected tokens
- Clear error messages with location

---

### Phase 3: Semantic Analysis

**File**: `backend/semantic_analyzer.py`

**Purpose**: Validate semantic correctness and type safety.

**Key Components**:
- `Symbol` - Symbol table entry with name, type, value
- `Scope` - Represents a lexical scope
- `SemanticAnalyzer` - Main semantic checker

**What It Checks**:

1. **Variable Declaration**
   - No duplicate definitions in same scope
   - Type inference from initializers
   - Usage before declaration

2. **Type Checking**
   - Arithmetic operations on compatible types
   - Comparison always returns boolean
   - Logical operations on booleans
   - Function call argument counts

3. **Scope Validation**
   - Variables accessible in current scope
   - Scope nesting (local overrides global)
   - Function parameters in function scope

4. **Control Flow**
   - Return statements inside functions only
   - Break/continue inside loops only

**Process**:
```
AST
        ↓
[Tree Traversal with Visitor Pattern]
        ↓
For each node:
  • Check declarations (no duplicates)
  • Check types (operations valid)
  • Check scope (variables defined)
  • Check context (return in function, etc.)
        ↓
Validated AST (or SemanticError)
```

**Example Type Checking**:
```
Input Code: var x = "hello" + 5;

Check:
  1. "hello" is string literal
  2. 5 is integer literal
  3. Can we add string + integer?
  4. NO! → SemanticError

Error Message: "Cannot apply + to string and integer"
```

**Scope Tracking**:
```
Global Scope
│
├─ var x: int
├─ function foo()
│  └─ Local Scope 1
│     ├─ param a: int
│     ├─ var result: int
│
└─ function bar()
   └─ Local Scope 2
      ├─ param name: string
```

---

### Phase 4: Code Generation & Interpretation

**File**: `backend/interpreter.py`

**Purpose**: Generate intermediate code and execute the program.

**Key Components**:
- `CodeGenerator` - Generates three-address code (TAC)
- `Interpreter` - Tree-walking interpreter
- Runtime exception classes

**Intermediate Code (Three-Address Code)**:
```
Example:
  x = y + z;
  a = x * 2;
  
TAC:
  _temp1 = y + z
  x = _temp1
  _temp2 = x * 2
  a = _temp2
```

**Interpretation Process**:
```
Validated AST
        ↓
[Tree-Walking Execution]
        ↓
For each statement:
  1. If variable declaration
     → Create variable, store in current scope
  2. If function declaration
     → Store function definition
  3. If expression
     → Evaluate recursively
  4. If control flow (if, for, while)
     → Check conditions and branch/loop
  5. If function call
     → Push new scope, bind parameters, execute body
        ↓
Program Output + Return Value
```

**Runtime Scope Stack**:
```
Execution of:
  function foo(x) {
    var y = x + 1;
    {
      var z = y * 2;
      print(z);
    }
  }
  foo(5);

Stack frames during execution:
  [Global Scope: {foo: <function>}]
    → Call foo(5)
  [Global | Function foo: {x: 5, y: 6, foo: <function>}]
    → Enter block
  [Global | foo | Block: {x: 5, y: 6, z: 12, foo: <function>}]
    → print(12)
    → Exit block
  [Global | foo: {x: 5, y: 6}]
    → Return
  [Global: {foo: <function>}]
```

**Expression Evaluation**:
```
Binary(
  left=Identifier('x'),
  operator='+',
  right=Literal(5, 'integer')
)

Evaluation:
  1. Evaluate left: Identifier('x') → Look up 'x' in scope → Get value 10
  2. Evaluate right: Literal(5) → 5
  3. Apply operator: 10 + 5 → 15
  Result: 15
```

---

## 🔗 Data Flow Example

### Complete Flow: `var x = add(3, 4);`

```
PHASE 1: LEXICAL ANALYSIS
────────────────────────────
Input: "var x = add(3, 4);"

Lexer tokenizes:
  VAR(var)
  IDENTIFIER(x)
  ASSIGN(=)
  IDENTIFIER(add)
  LPAREN(()
  INTEGER(3)
  COMMA(,)
  INTEGER(4)
  RPAREN())
  SEMICOLON(;)


PHASE 2: SYNTAX ANALYSIS
────────────────────────────
Tokens parsed into AST:

VarDecl(
  name='x',
  initializer=Call(
    function=Identifier('add'),
    arguments=[
      Literal(3, 'integer'),
      Literal(4, 'integer')
    ]
  )
)


PHASE 3: SEMANTIC ANALYSIS
────────────────────────────
Validation:
  ✓ Variable 'x' not previously defined
  ✓ Function 'add' is defined
  ✓ Function 'add' accepts 2 arguments
  ✓ Arguments are correct types (int, int)
  ✓ Assignment to variable valid

Result: PASS


PHASE 4: EXECUTION
────────────────────────────
Execution steps:
  1. Create variable 'x' in current scope
  2. Evaluate initializer expression:
     a. Look up function 'add'
     b. Evaluate argument 1: Literal(3) → 3
     c. Evaluate argument 2: Literal(4) → 4
     d. Push new scope with params
     e. Bind add's parameters: a=3, b=4
     f. Execute function body: return 3 + 4
     g. Pop scope
     h. Return value: 7
  3. Store 7 in variable 'x'

Result: x = 7
```

---

## 🌐 Backend REST API

**Server**: Flask on `http://localhost:5000`

### Endpoints

#### 1. Compile & Execute
```
POST /api/compile
Content-Type: application/json

Request Body:
{
  "code": "var x = 10; print(x);"
}

Response:
{
  "success": true/false,
  "tokens": [
    {"type": "VAR", "value": "var", "line": 1, "column": 1},
    ...
  ],
  "ast": "Program\n  statements:\n    VarDecl\n      name: x\n      initializer: Literal\n        value: 10\n        type: integer",
  "output": "10",
  "error": null
}
```

#### 2. Lexical Analysis Only
```
POST /api/lexify
```

#### 3. Parsing Only
```
POST /api/parse
```

#### 4. Language Specification
```
GET /api/language-spec

Response:
{
  "keywords": ["var", "function", "if", ...],
  "operators": ["+", "-", "*", ...],
  "types": ["int", "float", "string", "boolean"]
}
```

---

## 💻 Frontend Architecture

**Technology**: HTML5, CSS3, JavaScript (Vanilla)

**Components**:
1. **Code Editor**
   - Textarea for input
   - Syntax highlighting overlay
   - Auto-save to localStorage
   - Line/column tracking

2. **Output Display**
   - Tabbed interface (Output, Tokens, AST, Errors)
   - Color-coded output
   - Scrollable with code font

3. **UI Controls**
   - Compile button (Ctrl+Enter)
   - Clear, Save, Load buttons
   - Sample program quick-load
   - Language guide reference

4. **Client-Server Communication**
   - Fetch API for HTTP requests
   - JSON request/response
   - Error handling and status messages
   - Async compilation with UI feedback

---

## 🎯 Key Design Decisions

### 1. **Recursive Descent Parsing**
- Easy to understand and modify
- Good for educational purposes
- Sufficient for our grammar complexity
- Alternative: Use ANTLR parser generator

### 2. **Tree-Walking Interpreter**
- Direct AST evaluation
- No intermediate compilation
- Easy debugging and modifications
- Alternative: Bytecode VM for better performance

### 3. **Web-Based Interface**
- No installation needed (just a browser)
- Real-time feedback
- Easy to extend with more features
- Cross-platform compatibility

### 4. **Visitor Pattern for Semantic Analysis**
- Clean separation of concerns
- Easy to add new analyses
- Recursive tree traversal
- Type-safe in statically-typed languages

### 5. **Token Preservation**
- Show tokens to users for learning
- Helps debug lexical issues
- Transparent compilation process

---

## 🔄 Extension Points

### Adding New Features

#### 1. New Language Construct
```
1. Define token in lexer.py TokenType enum
2. Add lexing logic in Lexer.tokenize()
3. Define AST node class in parser.py
4. Add parsing logic in Parser (e.g., parse_new_stmt)
5. Add semantic checking in semantic_analyzer.py
6. Add interpretation logic in interpreter.py
7. Test with sample programs
```

#### 2. New Built-in Function
```
In interpreter.py, extend visit_call() method:
  if func_name == 'new_function':
    # Handle function call
```

#### 3. New Data Type
```
1. Add to TokenType and Lexer
2. Add Literal type to parser.py
3. Add type checking rules to semantic_analyzer.py
4. Add evaluation logic to interpreter.py
```

---

## 🐛 Error Recovery

The compiler uses **fail-fast** error reporting:
1. **Lexer** - Reports first invalid character
2. **Parser** - Stops at first syntax error
3. **Semantic** - Reports all errors found
4. **Runtime** - Reports runtime errors

This approach is suitable for a learning compiler. Production compilers would use error recovery to find multiple errors in one pass.

---

## 📈 Performance Characteristics

- **Small programs** (< 1000 lines): < 10ms
- **Medium programs** (< 10000 lines): 10-100ms
- **Large programs** (> 10000 lines): 100ms+

Bottlenecks:
1. Tokenization - Linear in source length
2. Parsing - Linear in token count
3. Semantic analysis - Linear in AST nodes
4. Interpretation - Linear in statement count

No caching between phases (could be optimized).

---

## 🎓 Learning Outcomes

By studying this compiler, you'll understand:

1. **Tokenization** - Converting characters to tokens
2. **Parsing** - Building hierarchical structures
3. **Type Systems** - Type checking and inference
4. **Scope Management** - Variable/function visibility
5. **Runtime Execution** - Evaluating AST
6. **Error Handling** - Reporting issues clearly
7. **API Design** - REST API patterns
8. **Frontend Integration** - Web interface patterns

---

## 📚 Reference Materials

- **Compiler Design** - Aho, Lam, Sethi, Ullman
- **Crafting Interpreters** - Nystrom (https://craftinginterpreters.com/)
- **Engineering a Compiler** - Cooper, Torczon

---

**This architecture demonstrates a complete, functional compiler pipeline suitable for educational purposes and as a foundation for more advanced language development.**
