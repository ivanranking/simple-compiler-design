# 📑 Project File Guide

This file helps you navigate the SimpleScript Compiler Professional Edition project.

## 📂 Directory Structure

### 🔴 **ROOT FOLDER** - Main Project
```
compiler design/
├── 📄 README.md                    ← Original project README
├── 📄 README_PROFESSIONAL.md       ← ⭐ MAIN OVERVIEW (START HERE!)
├── 📄 START_HERE.md                ← Quick start guide
├── 📄 QUICKSTART.md                ← Alternative quick start
├── 📄 PROFESSIONAL_GUIDE.md        ← 📖 COMPLETE USER GUIDE
├── 📄 QUICK_REFERENCE.md           ← ⌨️ SYNTAX & SHORTCUTS
├── 📄 TESTING_GUIDE.md             ← 🧪 VALIDATION TESTS
├── 📄 ARCHITECTURE.md              ← 🏗️ SYSTEM DESIGN
├── 📄 LANGUAGE_SPEC.md             ← 📝 LANGUAGE REFERENCE
├── 📄 PROJECT_SUMMARY.md           ← Project status
├── 📄 PROJECT_FILES.md             ← File descriptions
├── 📄 EXAMPLES.md                  ← Example programs
├── 📄 FILE_GUIDE.md                ← This file
│
├── 🚀 launch_pro.bat               ← Windows launcher (DOUBLE-CLICK TO START!)
├── 📄 run.bat                      ← Alternative launcher
│
├── 📁 backend/                     ← Python compiler backend
│   ├── 🐍 simple_server.py         ← HTTP server (no Flask needed!)
│   ├── 🐍 lexer.py                 ← Tokenizer
│   ├── 🐍 parser.py                ← Syntax parser
│   ├── 🐍 semantic_analyzer.py     ← Type checker
│   ├── 🐍 interpreter.py           ← Code executor
│   └── 📄 requirements.txt          ← Python dependencies
│
├── 📁 frontend/                    ← Web interface
│   ├── 🌐 home.html                ← Interface selector (landing page)
│   ├── 🌐 pro.html                 ← Professional IDE (3-column)
│   ├── 🌐 index.html               ← Educational IDE (alternative)
│   ├── 🎨 style-pro.css            ← Professional styling
│   ├── 🎨 style.css                ← Educational styling
│   ├── 💻 script-pro.js            ← Professional IDE logic
│   └── 💻 script.js                ← Educational IDE logic
│
└── 📁 samples/                     ← Sample programs
    ├── hello_world.simple          ← Print statements
    ├── arithmetic.simple           ← Math operations
    ├── conditionals.simple         ← If/else logic
    ├── for_loop.simple             ← For loops
    ├── while_loop.simple           ← While loops
    ├── functions.simple            ← Function definitions
    ├── factorial.simple            ← Recursion example
    └── nested_loops.simple         ← Complex loops
```

---

## 🚀 Quick Start

### **Getting Started:**
1. **Windows**: Double-click `launch_pro.bat`
2. **Other OS**: Open terminal: `cd backend && python simple_server.py`
3. **Browser**: Go to `http://localhost:5000`
4. **IDE**: Click "Professional Edition"
5. **Code**: Start writing SimpleScript!

---

## 📖 Documentation Guide

### **For First-Time Users**
| File | Purpose | Read Time |
|------|---------|-----------|
| **README_PROFESSIONAL.md** | Overview & features | 5 min |
| **PROFESSIONAL_GUIDE.md** | Complete user manual | 15 min |
| **QUICK_REFERENCE.md** | Syntax cheat sheet | 3 min |

### **For Learning**
| File | Purpose |
|------|---------|
| **EXAMPLES.md** | Example programs & outputs |
| **LANGUAGE_SPEC.md** | Complete language specification |
| **samples/** folder | Pre-loaded sample programs |

### **For Validation**
| File | Purpose |
|------|---------|
| **TESTING_GUIDE.md** | 20-test verification suite |

### **For Understanding Architecture**
| File | Purpose |
|------|---------|
| **ARCHITECTURE.md** | System design & components |
| **PROJECT_SUMMARY.md** | Project overview |

---

## 🎯 File Descriptions

### **Documentation Files**

#### `README_PROFESSIONAL.md` ⭐ START HERE
- **Purpose**: Main entry point with complete overview
- **Contains**: Features, quick start, architecture, documentation index
- **Best For**: First-time users, project overview

#### `PROFESSIONAL_GUIDE.md` 📖 COMPREHENSIVE GUIDE
- **Purpose**: Complete user guide with examples
- **Contains**: Features, language guide, keyboard shortcuts, example programs, troubleshooting
- **Best For**: Learning to use the IDE, understanding SimpleScript syntax

#### `QUICK_REFERENCE.md` ⌨️ CHEAT SHEET
- **Purpose**: Quick syntax reference and keyboard shortcuts
- **Contains**: Syntax examples, operator reference, common patterns
- **Best For**: Quick lookup while coding

#### `TESTING_GUIDE.md` 🧪 VALIDATION
- **Purpose**: Comprehensive test suite with expected results
- **Contains**: 20 tests covering all features
- **Best For**: Verifying everything works correctly

#### `ARCHITECTURE.md` 🏗️ TECHNICAL DESIGN
- **Purpose**: System architecture and implementation details
- **Contains**: Component design, data flow, API specifications
- **Best For**: Understanding how the compiler works

#### `LANGUAGE_SPEC.md` 📝 LANGUAGE REFERENCE
- **Purpose**: Complete SimpleScript language specification
- **Contains**: Syntax rules, operators, control structures
- **Best For**: Language reference during development

#### `EXAMPLES.md`
- **Purpose**: Example programs with expected outputs
- **Contains**: Code samples for various scenarios
- **Best For**: Learning by example

#### `START_HERE.md` & `QUICKSTART.md`
- **Purpose**: Quick introduction and setup
- **Contains**: Basic setup and first program
- **Best For**: Very quick start (5 minutes)

### **Backend Files (Python)**

#### `backend/simple_server.py` 🌐 SERVER
- **Purpose**: HTTP server for serving IDE and API
- **Key Features**:
  - Flask-free (uses Python's built-in http.server)
  - Handles GET requests for HTML/CSS/JS
  - Handles POST requests for compilation
  - Python 3.14+ compatible
- **How to Run**: `python simple_server.py`
- **Port**: localhost:5000

#### `backend/lexer.py` 🔤 TOKENIZER
- **Purpose**: Converts source code into tokens
- **Key Functions**:
  - `tokenize(code)` → Returns list of Token objects
- **Output**: List of tokens (keyword, identifier, operator, number, etc.)

#### `backend/parser.py` 🌳 SYNTAX PARSER
- **Purpose**: Builds Abstract Syntax Tree from tokens
- **Key Functions**:
  - `parse(tokens)` → Returns AST
- **Output**: Tree structure representing code organization

#### `backend/semantic_analyzer.py` 🔍 TYPE CHECKER
- **Purpose**: Validates types and scope
- **Key Functions**:
  - `analyze(ast)` → Returns validated AST + errors
- **Checks**:
  - Variable definitions before use
  - Type compatibility
  - Function signatures

#### `backend/interpreter.py` ⚡ EXECUTOR
- **Purpose**: Executes the code
- **Key Functions**:
  - `interpret(ast)` → Returns program output
- **Output**: Console output, error messages

### **Frontend Files (JavaScript/HTML/CSS)**

#### `frontend/home.html` 🏠 LANDING PAGE
- **Purpose**: Interface selector page
- **Shows**: Professional vs Educational edition options
- **Status Display**: Green checkmark when server running

#### `frontend/pro.html` 💼 PROFESSIONAL IDE (MAIN)
- **Purpose**: Main 3-column IDE interface
- **Sections**:
  - Left: Code editor with syntax highlighting
  - Middle: Pipeline visualization + analysis tabs
  - Right: Program output console
- **Status**: Fully functional

#### `frontend/style-pro.css` 🎨 PROFESSIONAL STYLES
- **Purpose**: CSS for professional interface
- **Features**:
  - Dark/Light theme support
  - Responsive grid layout
  - Syntax highlighting colors
  - Custom animations

#### `frontend/script-pro.js` 💻 PROFESSIONAL LOGIC
- **Purpose**: JavaScript for professional IDE
- **Functions**:
  - Code compilation & execution
  - Real-time syntax highlighting
  - Analysis tab switching
  - File save/load
  - Keyboard shortcuts

#### `frontend/index.html` 📚 EDUCATIONAL IDE (ALT)
- **Purpose**: Alternative educational interface
- **Note**: Professional edition is primary

---

## 🔄 File Dependencies

```
Index:        home.html
              ├── pro.html (Professional Edition)
              │   ├── style-pro.css
              │   └── script-pro.js
              │       └── /api/compile endpoint
              │
              └── index.html (Educational Edition)
                  ├── style.css
                  └── script.js
                      └── /api/compile endpoint

Backend:      simple_server.py (main entry point)
              ├── lexer.py
              ├── parser.py
              ├── semantic_analyzer.py
              └── interpreter.py
```

---

## 📊 File Statistics

| Category | Files | Size |
|----------|-------|------|
| Documentation | 8 files | ~50 KB |
| Python Backend | 5 files | ~20 KB |
| Frontend | 8 files | ~150 KB |
| Samples | 8 files | ~2 KB |
| **Total** | **29 files** | **~222 KB** |

---

## 🎯 Recommended Reading Order

### **For Quick Setup (10 minutes)**
1. This file (FILE_GUIDE.md)
2. README_PROFESSIONAL.md
3. QUICK_REFERENCE.md
4. Run `launch_pro.bat` and try a sample program

### **For Learning (1 hour)**
1. README_PROFESSIONAL.md
2. PROFESSIONAL_GUIDE.md (Sections 1-3)
3. QUICK_REFERENCE.md
4. Try sample programs
5. Write your first program

### **For Complete Understanding (2-3 hours)**
1. All documentation files in order
2. Review ARCHITECTURE.md
3. Read LANGUAGE_SPEC.md
4. Try TESTING_GUIDE.md
5. Explore backend code

### **For Troubleshooting**
1. PROFESSIONAL_GUIDE.md → "Troubleshooting" section
2. TESTING_GUIDE.md → "Debugging Failed Tests" section
3. Check browser console (F12)
4. Review server terminal output

---

## 🔐 Important Files to Keep

⭐ **Essential (Do Not Delete)**
- `backend/simple_server.py` - Server will not run without this
- `frontend/pro.html` - Main IDE
- `frontend/script-pro.js` - IDE functionality
- `launch_pro.bat` - Easy launcher

⚠️ **Important (Project relies on)**
- All backend Python files (lexer, parser, etc.)
- All CSS styling files
- Sample programs (for reference)

📌 **Documentation (For reference)**
- All .md files in root
- Contains guides and specifications

---

## 💾 Backup Recommendations

Keep backups of:
1. **backend/simple_server.py** - If modified
2. **frontend/pro.html** - If customized
3. **frontend/script-pro.js** - If modified
4. Your code files (programs written in IDE)

---

## 🚀 Common File Operations

### **To Start the Compiler**
```bash
# Windows: Double-click launch_pro.bat
# Or: python backend/simple_server.py
```

### **To Load an Example**
```
1. Start IDE at http://localhost:5000/pro.html
2. Click "Load Sample Program..."
3. Select from list
```

### **To Save Your Code**
```
1. Click "Save" button or Ctrl+S
2. File downloads as program.simple
3. Keep in safe location
```

### **To Load Saved Code**
```
1. Click "Load" button or Ctrl+L
2. Select your .simple file
3. Code appears in editor
```

---

## 📞 Quick Help

### **"I don't know where to start"**
→ Read README_PROFESSIONAL.md

### **"I need a syntax reference"**
→ Read QUICK_REFERENCE.md or LANGUAGE_SPEC.md

### **"Something isn't working"**
→ Read TESTING_GUIDE.md "Troubleshooting" section

### **"I want to understand the design"**
→ Read ARCHITECTURE.md

### **"I want to learn with examples"**
→ Read EXAMPLES.md or PROFESSIONAL_GUIDE.md

### **"I want to test everything"**
→ Follow TESTING_GUIDE.md

---

## ✨ File Organization Summary

**📚 Documentation** (8 files)
- Complete guides for users and developers
- Tutorials, references, architecture docs

**🔧 Backend** (5 files)
- Python compiler implementation
- Lexer, parser, semantic analyzer, interpreter

**🌐 Frontend** (8 files)
- Professional and educational IDE interfaces
- HTML, CSS, JavaScript

**📝 Samples** (8 files)
- Pre-loaded example programs
- Ready to use in IDE

---

**Need help? Start with README_PROFESSIONAL.md!** 🚀