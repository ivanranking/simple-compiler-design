# SimpleScript Compiler - Complete Implementation

A full-featured compiler for **SimpleScript**, a custom programming language with a user-friendly web interface. Implements all major compiler phases: lexical analysis, parsing, semantic analysis, and execution.

## 📋 Project Overview

### Key Features
- ✅ Complete compiler pipeline with all phases
- ✅ Web-based IDE with syntax highlighting
- ✅ Real-time token display and AST visualization
- ✅ Error detection and reporting
- ✅ Sample programs included
- ✅ Save/Load code files
- ✅ Responsive design

### Compiler Phases Implemented

1. **Lexical Analysis (Lexer)**
   - Tokenizes source code into tokens
   - Recognizes keywords, identifiers, operators, literals
   - Handles comments and string escape sequences
   - Error reporting with line/column information

2. **Syntax Analysis (Parser)**
   - Builds Abstract Syntax Tree (AST) from tokens
   - Implements recursive descent parsing
   - Grammar: expression-based with proper precedence
   - Reports syntax errors with context

3. **Semantic Analysis**
   - Type checking for expressions and operations
   - Variable declaration validation
   - Scope analysis with scope stack
   - Function definition and call validation

4. **Code Generation & Interpretation**
   - Tree-walking interpreter
   - Executes AST directly
   - Supports function calls with parameters
   - Generates intermediate three-address code representation

## 🗂️ Project Structure

```
compiler-design/
├── backend/
│   ├── lexer.py                 # Tokenization
│   ├── parser.py                # AST generation
│   ├── semantic_analyzer.py     # Type checking & validation
│   ├── interpreter.py           # Execution engine
│   └── app.py                   # Flask REST API
├── frontend/
│   ├── index.html               # Main UI
│   ├── style.css                # Styling
│   └── script.js                # Client-side logic
├── samples/
│   ├── hello_world.simple       # Hello World
│   ├── arithmetic.simple        # Basic arithmetic
│   ├── for_loop.simple          # Loop example
│   ├── while_loop.simple        # While loop example
│   ├── functions.simple         # Function demo
│   ├── conditionals.simple      # If/else statements
│   ├── nested_loops.simple      # Nested loops
│   └── factorial.simple         # Recursive functions
├── LANGUAGE_SPEC.md             # Language specification
└── README.md                    # This file
```

## 💻 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Step 1: Clone/Download the Project
```bash
cd "c:\Users\AKOL VERONICA\Desktop\compiler design"
```

### Step 2: Install Python Dependencies
```bash
# Navigate to backend directory
cd backend

# Install required packages
pip install flask flask-cors

# If pip doesn't work, try:
python -m pip install flask flask-cors
```

### Step 3: Start the Backend Server
```bash
# From the backend directory
python app.py
```

You should see output like:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Open the Frontend
Open `frontend/index.html` in your web browser:
```
file:///c:/Users/AKOL%20VERONICA/Desktop/compiler%20design/frontend/index.html
```

Or, use a simple HTTP server to serve the frontend:
```bash
# From the frontend directory
python -m http.server 8000
# Then visit: http://localhost:8000
```

## 📚 Language Specification

### Data Types
- `int` - Integer numbers
- `float` - Floating-point numbers
- `string` - Text strings (in quotes)
- `boolean` - `true` / `false`

### Variables
```javascript
var x = 10;
var name = "Alice";
var pi = 3.14;
var isActive = true;
```

### Operators
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `and`, `or`, `not`
- **Assignment**: `=`

### Control Flow

#### If-Else Statements
```javascript
if (age >= 18) {
    print("You are an adult");
} else {
    print("You are a minor");
}
```

#### For Loops
```javascript
for (var i = 0; i < 10; i = i + 1) {
    print("Iteration ", i);
}
```

#### While Loops
```javascript
while (counter > 0) {
    print("Count: ", counter);
    counter = counter - 1;
}
```

### Functions
```javascript
function add(a, b) {
    return a + b;
}

var result = add(5, 3);
print("Result: ", result);
```

### Input/Output

#### Print Statement
```javascript
print("Hello");
print("Value: ", 42);
print("Multiple", "arguments", "work");
```

#### Input Statement
```javascript
input(username);  // Read user input into variable
```

### Comments
```javascript
// Single line comment
// Everything after // is ignored
```

## 🧪 Example Programs

### Hello World
```javascript
print("Hello, World!");
```

### Arithmetic
```javascript
var a = 10;
var b = 20;
print("Sum: ", a + b);
print("Product: ", a * b);
```

### Loop with Conditional
```javascript
for (var i = 1; i <= 5; i = i + 1) {
    if (i % 2 == 0) {
        print(i, " is even");
    } else {
        print(i, " is odd");
    }
}
```

### Function Example
```javascript
function factorial(n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

print("5! = ", factorial(5));
```

## 🎯 How to Use the IDE

### 1. Write Code
- Type your SimpleScript code in the editor
- Syntax highlighting updates automatically
- Indentation with Tab key is supported

### 2. Compile & Run
- Click **"▶ Compile & Run"** button (or Ctrl+Enter)
- Or load a sample program from the bottom

### 3. View Results
- **Output Tab**: Program output/print statements
- **Tokens Tab**: All tokens from lexical analysis
- **AST Tab**: Abstract Syntax Tree from parser
- **Errors Tab**: Any compilation or runtime errors

### 4. Save/Load Programs
- **Save Button**: Download code as `.simple` file
- **Load Button**: Open a previously saved `.simple` file
- Auto-save to browser's local storage

### 5. Sample Programs
Quick-load example programs:
- Hello World
- Arithmetic Operations
- Loop Examples
- Function Demonstrations
- Conditional Logic

## 🔍 Compiler Internals

### Lexer (`lexer.py`)
- Scans source character by character
- Produces `Token` objects with type, value, line, column
- Handles string literals with escape sequences
- Recognizes all keywords and operators
- Reports errors with precise location

### Parser (`parser.py`)
- Recursive descent parser
- Respects operator precedence
- Builds `Program` → `Statement` → `Expression` tree
- Supports all language constructs
- Generates descriptive error messages

### Semantic Analyzer (`semantic_analyzer.py`)
- Traverses AST with visitor pattern
- Maintains symbol table with scope stack
- Type checks all expressions
- Validates variable/function definitions
- Catches semantic errors early

### Interpreter (`interpreter.py`)
- Tree-walking interpreter
- Evaluates expressions recursively
- Maintains runtime scope stack
- Handles function calls with parameter binding
- Catches runtime errors gracefully

### Backend API (`app.py`)
- Flask REST API server
- Endpoints:
  - `POST /api/compile` - Full compilation & execution
  - `POST /api/lexify` - Lexical analysis only
  - `POST /api/parse` - Parsing only
  - `GET /api/language-spec` - Language info
  - `GET /health` - Health check

## 🐛 Error Handling

### Lexical Errors
- Unterminated strings
- Unexpected characters
- Invalid token sequences

### Syntax Errors
- Missing semicolons
- Unmatched braces/parentheses
- Invalid expressions

### Semantic Errors
- Undefined variables
- Type mismatches
- Function arity (parameter count) mismatch
- Break/continue outside loops
- Return outside functions

### Runtime Errors
- Division by zero
- Type coercion failures
- Undefined function calls

## 🚀 Advanced Usage

### Modify the Language
To add new keywords or operators:

1. **In `lexer.py`**: Add to `keywords` dictionary
2. **In `parser.py`**: Add grammar rules
3. **In `semantic_analyzer.py`**: Add type checking
4. **In `interpreter.py`**: Add evaluation logic

### Extend Grammar
The parser uses recursive descent, making it easy to extend:
```python
def new_statement(self) -> Statement:
    # Your parsing logic here
    pass
```

### Add Optimization Passes
Insert between parsing and interpretation:
- Constant folding
- Dead code elimination
- Unreachable code detection

## 🔧 Troubleshooting

### "Address already in use" error
Port 5000 is occupied. Change the port in `app.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Change 5000 to 5001
```

### Frontend can't connect to backend
Ensure:
1. Backend is running: `python app.py`
2. Backend is on port 5000 (or update API_BASE in `script.js`)
3. CORS is enabled in `app.py` (it is by default)

### CORS errors
Already handled in `app.py` with `CORS(app)`. If issues persist:
```python
CORS(app, resources={r"/api/*": {"origins": "*"}})
```

### Code not executing
Check the **Errors** tab for detailed error messages. Most issues:
- Missing semicolons
- Undefined variables
- Type mismatches

## 📖 Learning Resources

### Phase 1: Lexical Analysis
Learn how the lexer identifies tokens:
1. Open sample program
2. Click "Compile"
3. Switch to "Tokens" tab
4. See how source breaks into tokens

### Phase 2: Parsing
See how parser builds the AST:
1. View the "AST" tab
2. Observe nested structure of statements/expressions
3. Try complex expressions to see precedence

### Phase 3: Semantic Analysis
Understand type checking:
1. Try type mismatches: `var x = "hello" + 5;`
2. View error in "Errors" tab
3. Compiler prevents incorrect operations

### Phase 4: Execution
Watch the interpreter run:
1. Load factorial.simple
2. See recursive calls work correctly
3. Check output in "Output" tab

## 📝 Code Examples

All sample programs in `samples/` folder demonstrate:
- Basic operations
- Control flow
- Function definition
- Recursion
- Complex logic

Examine source files to learn the language syntax.

## 🎓 Educational Value

This project demonstrates:
- ✅ Tokenization algorithms
- ✅ Recursive descent parsing
- ✅ Abstract syntax trees
- ✅ Type systems
- ✅ Scope and symbol tables
- ✅ Interpretation/evaluation
- ✅ Error handling
- ✅ UI/Backend integration

## 📄 License

This is an educational project. Feel free to modify and extend it!

## 🤝 Contributing

Ideas for extensions:
- Add more operators (bitwise, ternary)
- Implement arrays/lists
- Add string manipulation functions
- Create a bytecode compiler instead of tree-walking
- Add debugging features (breakpoints, step-through)
- Optimize with constant folding
- Add more built-in functions

## ✨ Future Enhancements

Potential improvements:
1. **Classes and Objects** - Add OOP support
2. **Better Error Messages** - Add suggestions/fixes
3. **Debugger** - Step through execution
4. **Performance** - Bytecode compilation
5. **Standard Library** - More built-in functions
6. **Module System** - Code reuse across files
7. **REPL Mode** - Interactive shell
8. **Visualization** - Parse tree drawing

---

**Created**: May 2026
**Last Updated**: May 2026
**Version**: 1.0

For questions or improvements, refer to the language specification and compiler documentation within the code!
