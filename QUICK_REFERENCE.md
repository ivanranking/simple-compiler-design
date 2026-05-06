# 🎯 Quick Reference - SimpleScript Compiler Professional

## 🚀 Getting Started

### **1. Launch the Server**
- **Option A**: Double-click `launch_pro.bat`
- **Option B**: Open terminal: `cd backend && python simple_server.py`

### **2. Open in Browser**
- Go to: `http://localhost:5000`
- Choose: **Professional Edition**

---

## 🎮 Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│  SimpleScript Compiler  [🌙] [⚙️] [❓]                      │
├─────────────────────────────────────────────────────────────┤
│ ▶ Run Code | 👣 Step-by-Step | 🗑️ Clear | 💾 Save | 📂 Load │
├──────────────────┬──────────────────┬──────────────────────┤
│   📝 CODE        │  🔄 PIPELINE     │    📤 OUTPUT        │
│   EDITOR         │  & ANALYSIS      │    (Program output)  │
│                  │  ┌────────────┐  │                      │
│  print("Hi");    │  │ 🔤→🌳→🔍→⚡│  │ Hello, World!       │
│                  │  └────────────┘  │                      │
│                  │                  │                      │
│                  │  🔤 Tokens       │                      │
│                  │  🌳 AST          │                      │
│                  │  ⚠️ Errors       │                      │
├──────────────────┴──────────────────┴──────────────────────┤
│ Status: Ready | Time: 15ms | Tokens: 25                    │
└─────────────────────────────────────────────────────────────┘
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl + Enter` | **Compile & Run** |
| `Ctrl + Shift + Enter` | **Step-by-Step** |
| `Ctrl + S` | **Save Code** |
| `Ctrl + L` | **Load Code** |
| `Ctrl + Shift + C` | **Clear All** |
| `Esc` | **Close Modals** |

---

## 📝 Basic Syntax Cheat Sheet

### **Hello World**
```simplescript
print("Hello, World!");
```

### **Variables & Types**
```simplescript
var name = "Alice";      // String
var age = 25;            // Integer
var height = 5.8;        // Float
var active = true;       // Boolean
```

### **Arithmetic**
```simplescript
var sum = 10 + 5;        // 15
var diff = 10 - 3;       // 7
var product = 4 * 3;     // 12
var quotient = 12 / 3;   // 4
var remainder = 10 % 3;  // 1
```

### **Comparisons**
```simplescript
10 == 10      // true
10 != 5       // true
10 > 5        // true
10 <= 10      // true
```

### **If/Else**
```simplescript
if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}
```

### **For Loop**
```simplescript
for (var i = 1; i <= 5; i = i + 1) {
    print(i);
}
```

### **While Loop**
```simplescript
var x = 0;
while (x < 3) {
    print(x);
    x = x + 1;
}
```

### **Function**
```simplescript
function add(a, b) {
    return a + b;
}

var result = add(10, 20);
print(result);      // 30
```

### **Recursive Function**
```simplescript
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print(factorial(5));    // 120
```

---

## 🎯 Common Tasks

### **Run a Simple Program**
1. Type code in the **Code Editor** (left)
2. Click **▶ Run Code** or press `Ctrl + Enter`
3. See output in **Output** column (right)

### **Debug a Program**
1. Click **👣 Step-by-Step**
2. Watch each compilation phase:
   - 🔤 Lexer - Shows tokens
   - 🌳 Parser - Shows AST
   - 🔍 Semantic - Validates types
   - ⚡ Execution - Runs code
3. Check **⚠️ Errors** tab for issues

### **Load a Sample**
1. Click the dropdown: "Load Sample Program..."
2. Select a program (Hello World, Factorial, etc.)
3. Click **▶ Run Code** to see it execute

### **Save Your Code**
1. Write your code
2. Click **💾 Save** or press `Ctrl + S`
3. File downloads as `program.simple`

### **Load Saved Code**
1. Click **📂 Load** or press `Ctrl + L`
2. Select your `.simple` file
3. Code appears in editor

---

## 🔍 Reading the Analysis

### **Tokens Tab**
Shows each token from lexical analysis:
```
KEYWORD: var
IDENTIFIER: x
OPERATOR: =
NUMBER: 10
SEMICOLON: ;
```

### **AST Tab**
Shows code structure:
```
Program
  └── VariableDeclaration
      ├── name: x
      └── value: NumberLiteral(10)
```

### **Errors Tab**
Shows any compilation errors:
```
Syntax Error: Unexpected token at line 3
Semantic Error: Undefined variable 'x'
Runtime Error: Division by zero
```

---

## 🎨 Features at a Glance

| Feature | How to Use |
|---------|-----------|
| **Syntax Highlighting** | Automatic - keywords in blue, strings in orange |
| **Auto-save** | Code saves to browser storage as you type |
| **Dark Mode** | Click 🌙 button (saved automatically) |
| **Line Count** | Shows in status bar (bottom) |
| **Compilation Stats** | See time, token count in status bar |
| **Error Reporting** | Check ⚠️ Errors tab after compilation |
| **Real-time Preview** | Tokens update as you type |
| **Copy Output** | Click 📋 button on output area |

---

## 💡 Pro Tips

1. **Use Step-by-Step for learning** - See exactly how code is compiled
2. **Check Tokens for syntax issues** - Lexer errors show here first
3. **Review AST for structure** - Understand code organization
4. **Save often** - Use `Ctrl + S` or the Save button
5. **Try samples first** - Learn from built-in examples
6. **Read errors carefully** - They tell you exactly what's wrong
7. **Use meaningful names** - Makes code easier to understand

---

## 🚨 Troubleshooting

### **"Can't connect to server"**
- Ensure server is running: `python simple_server.py`
- Check URL: `http://localhost:5000` (not `https`)

### **Code won't compile**
- Check **⚠️ Errors** tab for error messages
- Look for missing semicolons
- Verify variable names match
- Check function signatures

### **No output shown**
- Add `print()` statements to your code
- Check **⚠️ Errors** tab
- Verify variables are initialized
- Look for runtime errors

### **Syntax highlighting not working**
- Refresh browser: `F5`
- Clear cache: `Ctrl + Shift + Delete`
- Reload page

---

## 📚 Learn More

- **Language Guide**: Click **[❓]** → Language Guide
- **Shortcuts**: Click **[❓]** → Keyboard Shortcuts  
- **About**: Click **[❓]** → About

---

## 🎓 Learning Progression

```
Level 1: Basics
├─ Hello World
├─ Variables
└─ Arithmetic

Level 2: Control Flow
├─ If/Else
├─ Loops (For, While)
└─ Boolean Logic

Level 3: Functions
├─ Basic Functions
├─ Parameters & Return
└─ Recursion

Level 4: Advanced
├─ Complex Logic
├─ Data Structures
└─ Algorithm Implementation
```

---

**Ready to code? Open http://localhost:5000 and select Professional Edition! 🚀**