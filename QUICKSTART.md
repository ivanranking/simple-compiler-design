# Quick Start Guide - SimpleScript Compiler

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
python app.py
```
Look for: `Running on http://127.0.0.1:5000`

### Step 3: Open Frontend
Open this file in your browser:
```
frontend/index.html
```

## 💡 First Program

1. **Click "Hello World"** sample button
2. **Click "▶ Compile & Run"** button
3. **See output in the "Output" tab**

## 📝 Write Your Own Code

1. Clear the editor (🗑 Clear button)
2. Type SimpleScript code:
```javascript
var message = "Hello!";
print(message);
```
3. Press **Ctrl+Enter** or click compile button
4. Check Output tab for results

## 🎯 Quick Examples

### Print Statement
```javascript
print("Hello, World!");
```

### Variables and Math
```javascript
var x = 10;
var y = 20;
print("Sum: ", x + y);
```

### Loop
```javascript
for (var i = 1; i <= 5; i = i + 1) {
    print("Count: ", i);
}
```

### Function
```javascript
function greet(name) {
    return "Hello, " + name;
}
print(greet("Alice"));
```

## 🔍 View Compilation Phases

After compiling, switch tabs:
- **Output** - See program results
- **Tokens** - See tokenization (lexer output)
- **AST** - See parse tree structure (parser output)
- **Errors** - See any compilation/runtime errors

## 📂 Save & Load Code

- **💾 Save** - Download `.simple` file
- **📂 Load** - Open a `.simple` file

## 🐛 Debug Issues

Check the **Errors** tab for:
- Syntax errors (missing semicolons, etc.)
- Semantic errors (undefined variables, type mismatches)
- Runtime errors (division by zero, etc.)

## 📚 Learn More

See **README.md** for:
- Complete language documentation
- All compiler phases explained
- Advanced features
- Troubleshooting guide

---

**Happy Coding!** 🎉
