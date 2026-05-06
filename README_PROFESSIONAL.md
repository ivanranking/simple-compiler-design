# 🔧 SimpleScript Compiler - Professional Edition

> **A complete, production-ready compiler with a professional 3-column IDE interface, full lexical analysis, syntax parsing, semantic analysis, and code execution.**

---

## 📋 Table of Contents

1. [🚀 Quick Start](#-quick-start)
2. [📚 What's Included](#-whats-included)
3. [🎯 Feature Overview](#-feature-overview)
4. [🏗️ Architecture](#-architecture)
5. [📖 Documentation](#-documentation)
6. [🧪 Testing](#-testing)
7. [🔧 Troubleshooting](#-troubleshooting)

---

## 🚀 Quick Start

### **1. Prerequisites**
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)
- No additional dependencies required!

### **2. Start the Server**

**Option A: Automatic (Windows)**
```bash
double-click launch_pro.bat
```

**Option B: Manual**
```bash
cd backend
python simple_server.py
```

**Expected Output:**
```
🚀 SimpleScript Compiler Server running on http://localhost:5000
📁 Serving frontend from: [path]/frontend
📖 Open http://localhost:5000 in your browser
```

### **3. Open in Browser**

Visit: **http://localhost:5000**

You'll see the **Interface Selector** page. Click **Professional Edition** to access the 3-column IDE.

### **4. Write Your First Program**

```simplescript
print("Hello, World!");
```

Click **▶ Run Code** (or press `Ctrl + Enter`) and see the output!

---

## 📚 What's Included

### **Backend (Python)**
```
backend/
├── simple_server.py      ← Flask-free HTTP server (Python 3.14 compatible)
├── lexer.py              ← Tokenization engine
├── parser.py             ← Syntax tree builder
├── semantic_analyzer.py  ← Type checking & validation
├── interpreter.py        ← Code execution engine
└── requirements.txt      ← Dependencies (if needed)
```

### **Frontend (Web)**
```
frontend/
├── home.html            ← Interface selector (landing page)
├── pro.html             ← Professional 3-column IDE
├── style-pro.css        ← Professional styling
├── script-pro.js        ← IDE functionality
├── index.html           ← Educational interface
├── script.js            ← Educational functionality
└── style.css            ← Educational styling
```

### **Documentation**
```
├── README.md                ← This file
├── PROFESSIONAL_GUIDE.md    ← Complete user guide
├── QUICK_REFERENCE.md       ← Syntax & shortcuts cheat sheet
├── TESTING_GUIDE.md         ← Test suite & validation
├── START_HERE.md            ← Project quickstart
├── ARCHITECTURE.md          ← System design
└── LANGUAGE_SPEC.md         ← SimpleScript language specification
```

### **Samples**
```
samples/
├── hello_world.simple       ← Basic print
├── arithmetic.simple        ← Operators & math
├── conditionals.simple      ← If/else statements
├── for_loop.simple          ← For loops
├── while_loop.simple        ← While loops
├── functions.simple         ← Function definitions
└── factorial.simple         ← Recursion example
```

---

## 🎯 Feature Overview

### **Professional Edition (3-Column IDE)**

#### **Left Column: Code Editor**
- 📝 Full-featured textarea
- 🎨 Real-time syntax highlighting (keywords, strings, numbers, comments)
- 📊 Live statistics (lines, characters, tokens)
- 💾 Auto-save to browser storage
- 🎯 Tab support, auto-indentation

#### **Middle Column: Analysis Pipeline**
- 🔄 **Visual Pipeline**: 4-stage compilation display
  - 🔤 Lexical Analysis (Tokenization)
  - 🌳 Syntax Analysis (Parsing)
  - 🔍 Semantic Analysis (Type Checking)
  - ⚡ Execution (Code Running)
  
- 📊 **Three Analysis Tabs**:
  - **🔤 Tokens**: All tokens from lexer with line/column info
  - **🌳 AST**: Complete abstract syntax tree visualization
  - **⚠️ Errors**: Detailed compilation/runtime error messages

#### **Right Column: Output Console**
- 📤 Program output display
- 📋 Copy to clipboard button
- 🎨 Dark theme for readability
- 🔄 Clear output button

#### **Toolbar Features**
- ▶ **Run Code** - Full compilation & execution
- 👣 **Step-by-Step** - Sequential phase execution with delays
- 🗑️ **Clear** - Clear editor
- 💾 **Save** - Download code as `.simple` file
- 📂 **Load** - Import code from file
- 📚 **Samples** - 7 pre-loaded example programs

#### **Top Navigation**
- 🌙 **Theme Toggle** - Dark/Light mode (saved)
- ⚙️ **Settings** - Configuration options
- ❓ **Help** - Language guide, shortcuts, about

#### **Status Bar**
- Current compilation status
- Execution time in milliseconds
- Token count
- Real-time statistics

---

## 🏗️ Architecture

### **System Design**

```
┌─────────────────────────────────────────────────────┐
│           BROWSER (HTML/CSS/JavaScript)             │
│                                                      │
│  ┌────────────────────────────────────────────────┐ │
│  │         Professional IDE Interface              │ │
│  │  [Editor] [Pipeline + Analysis] [Output]       │ │
│  └────────────────────────────────────────────────┘ │
│                        ↕ JSON API                    │
└────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│      Node: localhost:5000 (simple_server.py)       │
│                                                      │
│  HTTP Server (Python http.server)                  │
│  ├── GET /           → home.html                   │
│  ├── GET /pro.html   → Professional IDE            │
│  └── POST /api/compile → Compile & Run             │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│         COMPILER PIPELINE (Python Backend)         │
│                                                      │
│  Lexer → Parser → Semantic Analyzer → Interpreter  │
│                                                      │
│  ├── lexer.py              (Tokenization)          │
│  ├── parser.py             (Syntax Tree)           │
│  ├── semantic_analyzer.py  (Type Checking)        │
│  └── interpreter.py        (Execution)             │
└─────────────────────────────────────────────────────┘
```

### **Compilation Pipeline**

```
Source Code
    ↓
LEXER (Tokenization)
    • Converts code into tokens
    • Output: Token list
    ↓
PARSER (Syntax Analysis)
    • Builds Abstract Syntax Tree
    • Validates grammar
    • Output: AST
    ↓
SEMANTIC ANALYZER
    • Type checking
    • Variable scope validation
    • Function signature verification
    • Output: Validated AST + Diagnostics
    ↓
INTERPRETER (Execution)
    • Traverses AST
    • Executes instructions
    • Output: Program output
```

### **API Endpoints**

| Method | Endpoint | Input | Output |
|--------|----------|-------|--------|
| POST | `/api/compile` | `{code: string}` | `{success, tokens[], ast, output, error}` |
| GET | `/health` | - | `{status: "ok"}` |
| GET | `/` | - | home.html |
| GET | `/pro.html` | - | professional IDE |

### **Data Flow Example**

```
JavaScript → POST /api/compile with {code: "var x = 10;"}
                ↓
    simple_server.py receives request
                ↓
    Calls lexer.tokenize(code) → [{type: 'KEYWORD', value: 'var'}, ...]
                ↓
    Calls parser.parse(tokens) → AST tree
                ↓
    Calls semantic_analyzer.analyze(ast) → Validated AST
                ↓
    Calls interpreter.interpret(ast) → Output
                ↓
    Returns JSON: {success: true, tokens: [...], ast: "...", output: "", error: ""}
                ↓
    JavaScript parses response and updates UI
```

---

## 📖 Documentation

### **For Users**
| Document | Purpose |
|----------|---------|
| [PROFESSIONAL_GUIDE.md](PROFESSIONAL_GUIDE.md) | Complete user guide with examples |
| [QUICK_REFERENCE.md](QUICK_REFERENCE.md) | Syntax cheat sheet & keyboard shortcuts |
| [TESTING_GUIDE.md](TESTING_GUIDE.md) | Verification checklist (20 tests) |

### **For Developers**
| Document | Purpose |
|----------|---------|
| [ARCHITECTURE.md](ARCHITECTURE.md) | System design & component details |
| [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md) | SimpleScript language specification |
| [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) | Project overview & status |

### **Quick Navigation**
- 📖 **Getting Started**: See [PROFESSIONAL_GUIDE.md](PROFESSIONAL_GUIDE.md)
- ⌨️ **Keyboard Shortcuts**: See [QUICK_REFERENCE.md](QUICK_REFERENCE.md)
- 🧪 **Verify Installation**: See [TESTING_GUIDE.md](TESTING_GUIDE.md)
- 🏗️ **System Design**: See [ARCHITECTURE.md](ARCHITECTURE.md)

---

## 🧪 Testing

### **Quick Validation**

Run a test program to verify everything works:

```simplescript
print("Hello, World!");
var x = 10;
var y = 20;
print("Sum: ", x + y);
```

**Expected Output:**
```
Hello, World!
Sum: 30
```

### **Full Test Suite**

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for:
- 20 comprehensive tests
- Test cases for each feature
- Debugging procedures
- Expected results checklist

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

## 💻 Basic Language Examples

### **Variables and Types**
```simplescript
var name = "Alice";      // String
var age = 25;            // Integer
var height = 5.8;        // Float
var isActive = true;     // Boolean
```

### **Control Flow**
```simplescript
if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}

for (var i = 1; i <= 5; i = i + 1) {
    print(i);
}

while (count < 10) {
    count = count + 1;
}
```

### **Functions**
```simplescript
function add(a, b) {
    return a + b;
}

var result = add(5, 3);
print(result);    // 8
```

---

## 🎓 Learning Path

1. **Level 1: Basics**
   - Hello World program
   - Variables and types
   - Arithmetic operations
   - Use sample programs

2. **Level 2: Control Flow**
   - If/else conditions
   - For loops
   - While loops
   - Boolean operators

3. **Level 3: Functions**
   - Function definition
   - Parameters and return values
   - Function calls
   - Variable scope

4. **Level 4: Advanced**
   - Recursion
   - Complex logic
   - Nested structures
   - Algorithm implementation

---

## 🔧 Troubleshooting

### **Server Issues**

**"Port 5000 already in use"**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with the number shown)
taskkill /PID <PID> /F
```

**"Python not found"**
- Install Python 3.8+ from https://www.python.org/
- Add Python to PATH during installation

**Server crashes after a few compilations**
- Restart server: `Ctrl + C` then `python simple_server.py`
- Check for memory issues with large programs

### **Compilation Issues**

**"Unexpected token" error**
- Check syntax in the **⚠️ Errors** tab
- Review [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md) for correct syntax
- Compare with sample programs

**"Undefined variable" error**
- Ensure variable is declared with `var` keyword
- Check variable name spelling
- Variable must be declared before use

**No output shown**
- Add `print()` statements to your code
- Check **⚠️ Errors** tab for errors
- Try running a sample program

### **Browser Issues**

**Interface not loading**
- Refresh page: `F5`
- Clear browser cache: `Ctrl + Shift + Delete`
- Try different browser
- Check URL: `http://localhost:5000` (not https)

**Keyboard shortcuts not working**
- Make sure editor is focused (click in code area)
- Try refreshing page
- Check browser extensions blocking shortcuts

---

## 🚀 Features Summary

### ✅ Implemented
- [x] 3-column professional IDE interface
- [x] Real-time syntax highlighting
- [x] Token analysis display
- [x] AST visualization
- [x] Error reporting system
- [x] Step-by-step compilation
- [x] Dark/Light theme toggle
- [x] Save/Load code files
- [x] 7 sample programs
- [x] Keyboard shortcuts
- [x] Copy output to clipboard
- [x] Real-time statistics
- [x] Python 3.14 compatible server
- [x] Complete documentation

### 🎯 Ready for
- Learning SimpleScript
- Compiler education
- Code debugging
- Algorithm development
- Language experimentation

---

## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| **Backend Files** | 5 Python modules |
| **Frontend Files** | 8 HTML/CSS/JS files |
| **Documentation** | 8 markdown files |
| **Sample Programs** | 7 examples |
| **Test Cases** | 20 comprehensive tests |
| **Lines of Code** | 2000+ |
| **Keyboard Shortcuts** | 6 |
| **Analysis Tabs** | 3 |
| **Compiler Stages** | 4 |

---

## 📝 License & Credits

**SimpleScript Compiler Professional Edition**

This is an educational project demonstrating:
- Compiler design principles
- Lexical analysis techniques
- Syntax parsing methods
- Semantic analysis
- Web-based IDE development
- Professional UI/UX design

---

## 🎉 Getting Started Now

### **Quick Launch:**
1. Double-click `launch_pro.bat` (Windows)
2. Or: `cd backend && python simple_server.py`
3. Open: `http://localhost:5000`
4. Click: **Professional Edition**
5. Code: Write your first SimpleScript program!

### **Need Help?**
- 📖 [PROFESSIONAL_GUIDE.md](PROFESSIONAL_GUIDE.md) - Full user guide
- ⌨️ [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Syntax & shortcuts
- 🧪 [TESTING_GUIDE.md](TESTING_GUIDE.md) - Verification guide
- 🏗️ [ARCHITECTURE.md](ARCHITECTURE.md) - System design
- 📝 [LANGUAGE_SPEC.md](LANGUAGE_SPEC.md) - Language reference

---

## 🌟 Highlights

```
╔════════════════════════════════════════════════════════════╗
║        🔧 SimpleScript Compiler Professional Edition       ║
║                                                            ║
║   ✅ Full Compiler Implementation (Lexer→Parser→Semantic)  ║
║   ✅ Professional 3-Column IDE Interface                  ║
║   ✅ Real-Time Analysis & Visualization                   ║
║   ✅ Complete Error Reporting System                      ║
║   ✅ No External Dependencies Required                    ║
║   ✅ Python 3.14+ Compatible                             ║
║   ✅ Production-Ready Code Quality                        ║
║   ✅ Comprehensive Documentation                         ║
║                                                            ║
║   Ready to compile? Visit: http://localhost:5000 🚀       ║
╚════════════════════════════════════════════════════════════╝
```

---

**Made with ❤️ for learning and innovation**

*Version 2.0 - Professional Edition*  
*Status: ✅ Production Ready*