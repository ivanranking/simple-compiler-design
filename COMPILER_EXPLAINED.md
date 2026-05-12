# SimpleScript Compiler - Simple Explanation

## What is a Compiler?

A compiler is a program that translates code written in one language (like SimpleScript) into another
language (usually machine code) that computers can execute.

Think of it like a translator:
- You write instructions in SimpleScript (English-like language)
- The compiler translates it into instructions a computer can understand

---

## This Compiler Project

**Language:** SimpleScript (a simple programming language we created)
**Built with:** Python
**Type:** Educational compiler (designed to learn how compilers work)

---

## The Four Main Parts (Compiler Phases)

### 1. LEXICAL ANALYSIS (Lexer)
**What it does:** Breaks your code into small pieces called "tokens"

**Example:**
```
Input:  var x = 10;
Output: [VAR token] [IDENTIFIER "x"] [EQUALS token] [NUMBER 10] [SEMICOLON]
```

**File:** `backend/lexer.py`
**Analogy:** Like splitting a sentence into individual words

---

### 2. SYNTAX ANALYSIS (Parser)
**What it does:** Checks if tokens follow grammar rules and builds a tree structure (AST)

**Example:**
```
Tokens from lexer → AST (Abstract Syntax Tree)
           var x = 10;
              │
         ┌────┴────┐
        var      (=)
         │        │
         x      (10)
```

**File:** `backend/parser.py`
**Analogy:** Checking if a sentence is grammatically correct and understanding its structure

---

### 3. SEMANTIC ANALYSIS (Semantic Analyzer)
**What it does:** Checks for meaning errors (like using undefined variables or wrong types)

**Example:**
```
var x = 10;
print(y);  // ERROR: 'y' was never declared!
```

**File:** `backend/semantic_analyzer.py`
**Analogy:** Making sure the sentence makes logical sense

---

### 4. CODE EXECUTION (Interpreter)
**What it does:** Actually runs the program and produces output

**Example:**
```
Input code:  print("Hello " + "World!");
Output:      Hello World!
```

**File:** `backend/interpreter.py`
**Analogy:** Actually performing the actions the sentence describes

---

## SimpleScript Language Syntax

### Variables
```
var age = 25;
var name = "John";
```

### Functions
```
function greet(person) {
    print("Hello", person);
}
```

### Control Flow
```
if (x > 5) {
    print("x is big");
} else {
    print("x is small");
}

for (var i = 0; i < 10; i = i + 1) {
    print(i);
}
```

### Types
- `int` - whole numbers (10, -5, 100)
- `float` - decimal numbers (3.14, 2.5)
- `string` - text ("hello", "world")
- `boolean` - true/false values

---

## How It All Works Together

```
YOUR CODE (SimpleScript)
        ↓
   ┌────────────┐
   │   LEXER    │ → Turns code into tokens
   └────────────┘
        ↓
   ┌────────────┐
   │   PARSER   │ → Builds Abstract Syntax Tree
   └────────────┘
        ↓
   ┌────────────────────┐
   │ SEMANTIC ANALYZER  │ → Checks for errors
   └────────────────────┘
        ↓
   ┌────────────┐
   │ INTERPRETER│ → Runs the program
   └────────────┘
        ↓
   OUTPUT (result)
```

---

## Files in This Project

### Backend (Python)
- `lexer.py` - Tokenizer (phase 1)
- `parser.py` - Syntax analyzer (phase 2)
- `semantic_analyzer.py` - Type checker (phase 3)
- `interpreter.py` - Code runner (phase 4)
- `app.py` - Web API server

### Documentation
- `LANGUAGE_SPEC.md` - Full SimpleScript language rules
- `README.md` - Project overview
- `ARCHITECTURE.md` - Technical design
- `EXAMPLES.md` - Code examples

---

## Why Build a Compiler?

1. **Understand how programming languages work**
2. **Learn about parsing, tokenization, ASTs**
3. **Create your own language**
4. **Foundation for building real compilers**

---

## Running the Compiler

```bash
# Via web API
python backend/app.py

# Direct execution
python backend/lexer.py     # Just tokenize
python backend/parser.py    # Just parse
python backend/interpreter.py  # Run programs
```

---

## Example: Complete Flow

**Input Code:**
```simple
var x = 5;
var y = 10;
print(x + y);
```

**Step-by-step:**
1. Lexer: `[VAR, "x", "=", 5, ";", VAR, "y", "=", 10, ";", PRINT, "(", "x", "+", "y", ")", ";"]`
2. Parser: Builds tree with variable declarations and print statement
3. Semantic Analyzer: Checks x and y exist, addition is valid
4. Interpreter: Executes → Output: `15`

---

## Key Terms Made Simple

- **Token** - Smallest piece of code (like a word)
- **AST** - Tree showing code structure (like a sentence diagram)
- **Grammar** - Rules for writing valid code (like grammar rules)
- **Semantics** - Meaning of code (logic, not just structure)
- **Interpret** - Run code directly (vs compile to machine code)

---

## Summary

This is a **4-phase educational compiler** written in **Python** for a custom language
called **SimpleScript**. It shows you how real compilers like those for Python, Java, or
C++ work internally, just simplified for learning.
