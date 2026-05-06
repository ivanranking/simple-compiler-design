# 🔧 SimpleScript Compiler - Professional Edition

A **complete, production-ready compiler interface** with full lexical analysis, syntax parsing, semantic analysis, and code execution. This is a professional-grade tool for learning and using the SimpleScript programming language.

## 🚀 Quick Start

### **1. Start the Server**

Open a terminal and run:
```bash
cd backend
python simple_server.py
```

**Expected output:**
```
🚀 SimpleScript Compiler Server running on http://localhost:5000
📁 Serving frontend from: ...
📖 Open http://localhost:5000 in your browser
```

### **2. Open in Browser**

Navigate to: **http://localhost:5000**

You'll see the interface selector screen. Choose:
- **Professional Edition** - Advanced 3-column layout (recommended)
- **Educational Edition** - Pipeline visualization & learning mode

---

## 💼 Professional Edition Features

### **Layout**
- **Left Column**: Code Editor with syntax highlighting
- **Middle Column**: Compilation Pipeline & Analysis (Tokens, AST, Errors)
- **Right Column**: Program Output/Console

### **Compilation Pipeline**
Visual step-by-step display of:
1. 🔤 **Lexical Analysis** - Tokenization
2. 🌳 **Syntax Analysis** - Parsing
3. 🔍 **Semantic Analysis** - Type checking
4. ⚡ **Execution** - Code interpretation

### **Analysis Tabs**
- **Tokens**: All tokens from lexical analysis with line/column info
- **AST**: Complete abstract syntax tree
- **Errors**: Detailed error messages and diagnostics

### **Features**
- ✅ Real-time syntax highlighting
- ✅ Auto-save to browser storage
- ✅ Dark/Light theme toggle
- ✅ Copy output to clipboard
- ✅ Save/Load code files (.simple)
- ✅ 7 built-in sample programs
- ✅ Compilation time tracking
- ✅ Line & character count
- ✅ Step-by-step compilation mode
- ✅ Keyboard shortcuts

---

## 📚 Language Guide

### **Data Types**
```simplescript
int       // Integer numbers (10, -5, 0)
float     // Decimal numbers (3.14, -2.5)
string    // Text ("Hello, World!")
boolean   // true or false
```

### **Variables**
```simplescript
var x = 10;
var name = "SimpleScript";
var pi = 3.14;
var isActive = true;
```

### **Operators**
- **Arithmetic**: `+`, `-`, `*`, `/`, `%`
- **Comparison**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Logical**: `and`, `or`, `not`

### **Control Flow**
```simplescript
// If/Else
if (x > 10) {
    print("X is greater than 10");
} else {
    print("X is 10 or less");
}

// For Loop
for (var i = 1; i <= 5; i = i + 1) {
    print(i);
}

// While Loop
var count = 0;
while (count < 3) {
    print(count);
    count = count + 1;
}
```

### **Functions**
```simplescript
function greet(name) {
    print("Hello, ", name);
}

function add(a, b) {
    return a + b;
}

greet("World");
var result = add(5, 3);
print(result);  // Output: 8
```

### **Input/Output**
```simplescript
print("Hello");           // Output to console
print(10, 20, 30);       // Multiple values
var num = input();        // Read user input
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | Compile & Run |
| `Ctrl + Shift + Enter` | Step-by-Step Compilation |
| `Ctrl + S` | Save Code |
| `Ctrl + L` | Load Code File |
| `Ctrl + Shift + C` | Clear All |
| `Esc` | Close Modals |

---

## 📖 Example Programs

### **Hello World**
```simplescript
print("Hello, World!");
print("Welcome to SimpleScript!");
```

### **Arithmetic Operations**
```simplescript
var a = 10;
var b = 3;
print("a + b = ", a + b);   // 13
print("a - b = ", a - b);   // 7
print("a * b = ", a * b);   // 30
print("a / b = ", a / b);   // 3
print("a % b = ", a % b);   // 1
```

### **Factorial Function**
```simplescript
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print("Factorial of 5 = ", factorial(5));    // 120
print("Factorial of 6 = ", factorial(6));    // 720
```

### **Loops and Conditions**
```simplescript
// Multiplication Table
for (var i = 1; i <= 5; i = i + 1) {
    for (var j = 1; j <= 5; j = j + 1) {
        print(i, " * ", j, " = ", i * j);
    }
}

// Grade Calculation
var score = 85;
if (score >= 90) {
    print("Grade: A");
} else if (score >= 80) {
    print("Grade: B");
} else if (score >= 70) {
    print("Grade: C");
} else {
    print("Grade: F");
}
```

---

## 🎯 How It Works

### **Compilation Process**

1. **Lexical Analysis (Lexer)**
   - Converts source code into tokens
   - Identifies keywords, identifiers, operators, literals
   - Reports lexical errors

2. **Syntax Analysis (Parser)**
   - Builds Abstract Syntax Tree (AST)
   - Validates grammar and syntax
   - Reports syntax errors

3. **Semantic Analysis**
   - Type checking
   - Variable scope validation
   - Function signature verification
   - Reports semantic errors

4. **Execution (Interpreter)**
   - Traverses the AST
   - Executes code instructions
   - Produces output
   - Handles runtime errors

### **Output Display**

After compilation, you'll see:
- **Output Tab**: Program console output
- **Tokens Tab**: List of all tokens with types and positions
- **AST Tab**: Tree structure of the parsed code
- **Errors Tab**: Any compilation/runtime errors

---

## 🔧 Troubleshooting

### **"Server not running"**
```bash
# Make sure the server is started:
cd backend
python simple_server.py
```

### **Port 5000 already in use**
```bash
# Kill the process using port 5000:
# Windows: netstat -ano | findstr :5000
# Kill the PID shown above
```

### **Code won't compile**
- Check syntax in the **Errors** tab
- Ensure all variables are declared with `var`
- Check function signatures match their calls
- Use sample programs as reference

### **No output shown**
- Make sure to use `print()` statements
- Check the **Errors** tab for runtime errors
- Verify variables are properly initialized

---

## 🎨 Interface Customization

### **Theme**
Click the 🌙 button in the top-right to toggle between dark and light themes. Your preference is saved automatically.

### **Code Formatting**
The editor automatically:
- Highlights syntax
- Indents properly
- Saves your code to browser storage
- Updates statistics (lines, characters)

---

## 📊 Compiler Architecture

```
Source Code
    ↓
Lexer (Tokenization)
    ↓ [Tokens List]
Parser (Syntax Analysis)
    ↓ [Abstract Syntax Tree]
Semantic Analyzer (Type Checking)
    ↓ [Validated AST]
Interpreter (Execution)
    ↓
Output
```

---

## 🚀 Advanced Features

### **Step-by-Step Compilation**
Use the "👣 Step-by-Step" button to compile one phase at a time and see:
- What tokens are generated
- How the parser structures the code
- Semantic validation results
- Final execution output

### **Real-Time Statistics**
Monitor compilation:
- **Status**: Current compilation state
- **Time**: Milliseconds to compile
- **Tokens**: Number of tokens generated
- **Lines/Chars**: Code statistics

### **Sample Programs**
Quick-load 7 example programs:
- Hello World
- Arithmetic Operations
- For Loop
- Function Demo
- Conditional Logic
- Factorial (Recursion)
- Nested Loops

---

## 🎓 Learning Path

1. **Start with Hello World** - Verify setup
2. **Load samples** - Understand syntax
3. **Try arithmetic** - Learn operators
4. **Test conditions** - Control flow
5. **Write functions** - Code organization
6. **Use step-by-step** - Understand compilation
7. **Read errors carefully** - Debug skills

---

## 📞 Support

For issues or questions:
1. Check the **Errors** tab for error messages
2. Review the **Language Guide** (? button)
3. Try sample programs
4. Use step-by-step compilation mode

---

## 📝 Notes

- Code is saved locally in your browser
- Sample programs use `.simple` file extension
- Maximum output size is limited by browser
- Each compilation is independent
- Theme preference is saved

---

**Version**: 2.0 Professional Edition  
**Status**: ✅ Production Ready  
**Last Updated**: 2026

Enjoy coding with SimpleScript! 🎉