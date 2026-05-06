# 🚀 SimpleScript Compiler Web Interface

A beautiful, interactive web interface for the SimpleScript compiler with real-time compilation and educational features.

## ✨ Features

- **🎨 Modern UI**: Dark/Light theme toggle with beautiful design
- **🔄 Visual Pipeline**: See compilation stages in real-time
- **👁️ Live Preview**: Real-time lexical and parse previews as you type
- **👣 Step-by-Step**: Educational compilation walkthrough
- **📝 Code Editor**: Syntax highlighting with auto-save
- **📊 Multiple Views**: Output, Tokens, AST, Errors, and Preview tabs
- **📚 Sample Programs**: Pre-loaded examples to try

## 🚀 Quick Start

### Option 1: One-Click Launcher (Recommended)
1. Double-click `launch_interface.bat`
2. The server will start and your browser will open automatically

### Option 2: Manual Start
1. Open a terminal in the project root
2. Run: `cd backend && python simple_server.py`
3. Open `http://localhost:5000` in your browser

## 🎯 How to Use

### 1. **Enter Code**
- Type your SimpleScript code in the editor
- Syntax highlighting shows keywords, strings, and numbers
- Code is auto-saved locally

### 2. **Compile & Run**
- Click **"▶ Compile & Run"** for full compilation
- Or click **"👣 Step-by-Step"** to see each phase

### 3. **View Results**
- **📤 Output**: See program execution results
- **🔤 Tokens**: View lexical analysis tokens
- **🌳 AST**: See the abstract syntax tree
- **⚠️ Errors**: Check for compilation errors
- **👁️ Preview**: Real-time lexical and parse previews

### 4. **Try Samples**
- Click sample buttons to load example programs
- Includes Hello World, arithmetic, loops, functions, and conditionals

## 🎨 Interface Features

### **Theme Toggle**
- 🌙 Dark mode for coding at night
- ☀️ Light mode for bright environments
- Preference saved automatically

### **Compilation Pipeline**
- Visual indicators for each compilation phase:
  - 🔤 Lexical Analysis
  - 🌳 Syntax Analysis
  - 🔍 Semantic Analysis
  - ⚡ Execution
- Real-time status updates with animations

### **Real-time Preview**
- See tokens appear as you type
- AST preview updates automatically
- 1-second debouncing for performance

## 📖 SimpleScript Language

### Data Types
- `int`, `float`, `string`, `boolean`

### Operators
- Arithmetic: `+`, `-`, `*`, `/`, `%`
- Comparison: `==`, `!=`, `<`, `>`, `<=`, `>=`
- Logical: `and`, `or`, `not`

### Keywords
- `var`, `function`, `if`, `else`, `for`, `while`
- `return`, `print`, `input`, `true`, `false`

### Example Program
```simplescript
// Hello World
print("Hello, SimpleScript!");

// Variables and arithmetic
var a = 10;
var b = 20;
print("Sum:", a + b);

// Functions
function multiply(x, y) {
    return x * y;
}
print("Product:", multiply(a, b));

// Loops
for (var i = 1; i <= 5; i = i + 1) {
    print("Count:", i);
}
```

## 🛠️ Technical Details

- **Backend**: Python HTTP server (Flask-free for Python 3.14+ compatibility)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Compiler**: Complete lexer, parser, semantic analyzer, and interpreter
- **Storage**: Local browser storage for code and preferences

## 🎯 Keyboard Shortcuts

- `Ctrl + Enter`: Compile and run
- `Ctrl + Shift + Enter`: Step-by-step compilation

## 🔧 Troubleshooting

### Server Won't Start
- Make sure Python 3.8+ is installed
- Check that port 5000 is not in use
- Try: `python backend/simple_server.py`

### Interface Not Loading
- Clear browser cache
- Try a different browser
- Check that the server is running on localhost:5000

### Compilation Errors
- Check syntax in the Errors tab
- Try sample programs first
- Use step-by-step mode to debug

## 📁 Project Structure

```
compiler-design/
├── frontend/
│   ├── index.html      # Main interface
│   ├── style.css       # Styling and themes
│   └── script.js       # Frontend logic
├── backend/
│   ├── simple_server.py # HTTP server
│   ├── lexer.py         # Lexical analyzer
│   ├── parser.py        # Syntax parser
│   ├── semantic_analyzer.py
│   ├── interpreter.py   # Code executor
│   └── app.py          # Flask version (legacy)
├── samples/            # Example programs
└── launch_interface.bat # Quick launcher
```

---

**Enjoy coding with SimpleScript! 🎉**