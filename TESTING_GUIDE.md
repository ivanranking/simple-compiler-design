# ✅ Testing Guide - SimpleScript Compiler Professional

This guide will help you verify that your SimpleScript compiler is working correctly.

---

## 🔧 Pre-Flight Checklist

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Navigate to backend folder
- [ ] Run `python simple_server.py`
- [ ] Server shows: "🚀 SimpleScript Compiler Server running on http://localhost:5000"
- [ ] Browser opened to `http://localhost:5000`
- [ ] Interface selector page visible

---

## 🧪 Test Suite

### **TEST 1: Server Startup**

**Objective**: Verify the server starts without errors

**Steps**:
1. Open terminal
2. `cd backend`
3. `python simple_server.py`

**Expected Result**:
```
🚀 SimpleScript Compiler Server running on http://localhost:5000
📁 Serving frontend from: [path]/frontend
📖 Open http://localhost:5000 in your browser
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 2: Home Page Load**

**Objective**: Verify interface selector loads

**Steps**:
1. Go to `http://localhost:5000`

**Expected Result**:
- See "SimpleScript Compiler" title
- Two cards: Professional Edition & Educational Edition
- Status shows "✅ Server is running and ready!"
- Both buttons clickable

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 3: Professional Edition Load**

**Objective**: Verify professional interface loads

**Steps**:
1. On home page, click "Professional Edition" button
2. Should redirect to `http://localhost:5000/pro.html`

**Expected Result**:
- 3-column layout visible
- Code editor on left
- Pipeline visualization in middle
- Output area on right
- All buttons functional
- No JavaScript errors in browser console (F12)

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 4: Hello World Program**

**Objective**: Verify basic compilation and output

**Code**:
```simplescript
print("Hello, World!");
```

**Steps**:
1. Paste code into editor
2. Click **▶ Run Code** (or `Ctrl + Enter`)
3. Wait for compilation

**Expected Result**:
- Status changes to "Processing"
- Output area shows: `Hello, World!`
- Status shows: "Ready" with compilation time
- No errors in ⚠️ Errors tab

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 5: Variable Declaration & Arithmetic**

**Objective**: Verify variables and operators work

**Code**:
```simplescript
var x = 10;
var y = 20;
var sum = x + y;
print("Sum: ", sum);
print("Product: ", x * y);
```

**Steps**:
1. Clear editor
2. Paste code
3. Click **▶ Run Code**

**Expected Result**:
```
Sum: 30
Product: 200
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 6: If/Else Statement**

**Objective**: Verify conditional logic

**Code**:
```simplescript
var age = 25;
if (age >= 18) {
    print("Adult");
} else {
    print("Minor");
}
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**

**Expected Result**:
```
Adult
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 7: For Loop**

**Objective**: Verify loop execution

**Code**:
```simplescript
for (var i = 1; i <= 3; i = i + 1) {
    print("Iteration: ", i);
}
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**

**Expected Result**:
```
Iteration: 1
Iteration: 2
Iteration: 3
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 8: While Loop**

**Objective**: Verify while loops work

**Code**:
```simplescript
var count = 0;
while (count < 3) {
    print("Count: ", count);
    count = count + 1;
}
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**

**Expected Result**:
```
Count: 0
Count: 1
Count: 2
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 9: Function Definition & Call**

**Objective**: Verify functions work correctly

**Code**:
```simplescript
function greet(name) {
    print("Hello, ", name);
}

greet("Alice");
greet("Bob");
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**

**Expected Result**:
```
Hello, Alice
Hello, Bob
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 10: Function Return Value**

**Objective**: Verify functions with return statements

**Code**:
```simplescript
function add(a, b) {
    return a + b;
}

var result = add(5, 3);
print("Result: ", result);
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**

**Expected Result**:
```
Result: 8
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 11: Recursion**

**Objective**: Verify recursive functions

**Code**:
```simplescript
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print("5! = ", factorial(5));
print("6! = ", factorial(6));
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**

**Expected Result**:
```
5! = 120
6! = 720
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 12: Token Analysis**

**Objective**: Verify token display

**Code**:
```simplescript
var x = 42;
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**
3. Click **🔤 Tokens** tab

**Expected Result**:
- Should show tokens like:
  - KEYWORD: var
  - IDENTIFIER: x
  - OPERATOR: =
  - NUMBER: 42
  - SEMICOLON: ;

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 13: AST Display**

**Objective**: Verify AST visualization

**Code**:
```simplescript
var x = 10;
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**
3. Click **🌳 AST** tab

**Expected Result**:
- Should show tree structure:
```
Program
  └── VariableDeclaration
      ├── name: x
      └── value: NumberLiteral(10)
```

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 14: Error Detection (Syntax)**

**Objective**: Verify syntax error detection

**Code**:
```simplescript
var x = 10    // Missing semicolon
print(x);
```

**Steps**:
1. Paste code (note: missing semicolon)
2. Click **▶ Run Code**
3. Check **⚠️ Errors** tab

**Expected Result**:
- Error message appears in Errors tab
- Status shows error state
- Output is empty

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 15: Error Detection (Undefined Variable)**

**Objective**: Verify semantic error detection

**Code**:
```simplescript
print(undefined_var);
```

**Steps**:
1. Paste code
2. Click **▶ Run Code**
3. Check **⚠️ Errors** tab

**Expected Result**:
- Error mentions undefined variable
- Errors tab shows semantic error
- Program doesn't execute

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 16: Step-by-Step Compilation**

**Objective**: Verify step-by-step mode

**Code**:
```simplescript
var msg = "Hello";
print(msg);
```

**Steps**:
1. Paste code
2. Click **👣 Step-by-Step**
3. Watch pipeline indicator progress through 4 phases
4. Click next at each stage

**Expected Result**:
- Pipeline shows each phase with delay
- Tokens visible after lexer phase
- AST visible after parser phase
- Output visible after execution
- Output: `Hello`

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 17: Keyboard Shortcuts**

**Objective**: Verify keyboard shortcuts work

**Test Cases**:

| Shortcut | Expected Action |
|----------|-----------------|
| `Ctrl + Enter` | Compiles code |
| `Ctrl + S` | Downloads file |
| `Ctrl + Shift + C` | Clears editor |
| `Esc` | Closes modals |

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 18: Theme Toggle**

**Objective**: Verify dark/light theme switch

**Steps**:
1. Click 🌙 button (top right)
2. Interface should change to light theme
3. Click again for dark theme
4. Refresh page - theme should persist

**Expected Result**:
- Smooth theme transition
- Theme persists after page refresh
- All text readable in both themes

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 19: Load Sample Program**

**Objective**: Verify sample programs load

**Steps**:
1. Click dropdown: "Load Sample Program..."
2. Select "Hello World"
3. Code appears in editor
4. Click **▶ Run Code**

**Expected Result**:
- Code auto-populates
- Program runs successfully
- Output shows: `Hello, World!` and `Welcome to SimpleScript!`

**Status**: ✅ PASS / ❌ FAIL

---

### **TEST 20: Save & Load Code**

**Objective**: Verify file save/load functionality

**Steps**:
1. Type: `var test = 123;`
2. Click **💾 Save**
3. File downloads as `program.simple`
4. Clear editor
5. Click **📂 Load**
6. Select the downloaded file
7. Code should reappear

**Expected Result**:
- File downloads successfully
- Filename is `program.simple`
- Code loads correctly from file
- Content matches original

**Status**: ✅ PASS / ❌ FAIL

---

## 📊 Test Results Summary

After running all tests, count your results:

- **Total Tests**: 20
- **Passed**: ___
- **Failed**: ___
- **Pass Rate**: ____%

### **Scoring**:
- **18-20 PASS**: ✅ **Excellent** - Compiler fully functional
- **15-17 PASS**: 🟡 **Good** - Minor issues to debug
- **<15 PASS**: ❌ **Needs Work** - Major issues to fix

---

## 🐛 Debugging Failed Tests

If a test fails:

1. **Check Browser Console** (F12 → Console tab)
   - Any JavaScript errors?
   - Check network tab for API failures

2. **Check Server Terminal**
   - Any error messages?
   - Is server still running?

3. **Check Errors Tab**
   - What error message appears?
   - Is it a syntax or semantic error?

4. **Try a Simple Program**
   - Test with just `print("test");`
   - Does the basic example work?

5. **Restart Server**
   - Stop server: `Ctrl + C`
   - Start again: `python simple_server.py`
   - Refresh browser

---

## ✨ Advanced Tests (Optional)

### **Complex Program Test**
```simplescript
function fibonacci(n) {
    if (n <= 1) {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

for (var i = 0; i < 10; i = i + 1) {
    print("fib(", i, ") = ", fibonacci(i));
}
```

**Expected**: Outputs Fibonacci sequence 0-9

---

### **String Concatenation Test**
```simplescript
var name = "World";
var greeting = "Hello, ";
print(greeting, name, "!");
```

**Expected**: `Hello, World!`

---

### **Boolean Logic Test**
```simplescript
var x = 10;
var y = 20;

if (x < y and y > 15) {
    print("Both conditions true");
}
```

**Expected**: `Both conditions true`

---

## 🎉 Success Criteria

Your compiler is **ready for production** when:

✅ All 20 core tests pass  
✅ No JavaScript errors in console  
✅ All sample programs run correctly  
✅ Error detection works properly  
✅ Keyboard shortcuts functional  
✅ Save/Load works reliably  

---

**Congratulations on your SimpleScript Compiler! 🎊**