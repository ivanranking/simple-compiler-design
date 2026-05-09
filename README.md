# SimpleScript Compiler

A complete educational compiler with lexical analysis, parsing, semantic analysis, and interpretation.

## Features

- **Lexical Analysis (Lexer)**: Tokenizes source code
- **Syntax Analysis (Parser)**: Builds Abstract Syntax Tree
- **Semantic Analysis**: Type checking and validation  
- **Code Execution (Interpreter)**: Tree-walking interpreter

## Language Syntax

```simple
// Variables
var x = 10;
var name = "Hello";

// Functions
function add(a, b) {
    return a + b;
}

// Control flow
if (x > 5) {
    print("x is greater than 5");
}

for (var i = 1; i <= 10; i = i + 1) {
    print(i);
}

// Print
print("Hello, World!");
```

## Deployment

Deployed on Render with gunicorn. See `render.yaml` for configuration.

## API Endpoints

- `POST /api/compile` - Compile and run code
- `POST /api/lexify` - Lexical analysis only
- `POST /api/parse` - Parse only
- `GET /api/language-spec` - Language specification
- `GET /health` - Health check