// Professional SimpleScript Compiler JavaScript

const API_BASE = 'http://localhost:5000/api';

// Sample programs
const samples = {
    hello: `// Hello World Program
print("Hello, World!");
print("Welcome to SimpleScript!");`,

    arithmetic: `// Arithmetic Operations
var a = 10;
var b = 3;
print("a = ", a);
print("b = ", b);
print("a + b = ", a + b);
print("a - b = ", a - b);
print("a * b = ", a * b);
print("a / b = ", a / b);
print("a % b = ", a % b);`,

    loop: `// For Loop Example
print("Counting from 1 to 10:");
for (var i = 1; i <= 10; i = i + 1) {
    print("Count: ", i);
}`,

    function: `// Function Demo
function add(x, y) {
    return x + y;
}

function greet(name) {
    print("Hello, ", name);
}

var sum = add(15, 25);
print("15 + 25 = ", sum);
greet("SimpleScript");`,

    conditional: `// Conditional Logic
var age = 25;
if (age >= 18) {
    print("You are an adult");
} else {
    print("You are a minor");
}

var score = 85;
if (score >= 90) {
    print("Grade: A");
} else if (score >= 80) {
    print("Grade: B");
} else if (score >= 70) {
    print("Grade: C");
} else {
    print("Grade: F");
}`,

    factorial: `// Factorial Function
function factorial(n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

print("Factorial of 5 = ", factorial(5));
print("Factorial of 6 = ", factorial(6));
print("Factorial of 10 = ", factorial(10));`,

    nested: `// Nested Loops
print("Multiplication Table:");
for (var i = 1; i <= 5; i = i + 1) {
    for (var j = 1; j <= 5; j = j + 1) {
        print(i, " * ", j, " = ", i * j);
    }
    print("---");
}`
};

let isDarkTheme = localStorage.getItem('themePro') === 'dark';
let compileTimeout;
let currentCompileTime = 0;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEditor();
    setupEventListeners();
    setupTheme();
    loadSampleProgram('hello');
    updateLineCount();
});

// Setup Editor
function setupEditor() {
    const editor = document.getElementById('codeEditorPro');
    const highlight = document.getElementById('highlightCodePro');

    editor.addEventListener('input', function() {
        updateHighlight();
        updateLineCount();
        clearTimeout(compileTimeout);
        compileTimeout = setTimeout(() => {
            realTimeUpdatePreviews();
        }, 800);
        localStorage.setItem('codeProSession', editor.value);
    });

    editor.addEventListener('scroll', function() {
        document.getElementById('highlightPro').scrollLeft = editor.scrollLeft;
        document.getElementById('highlightPro').scrollTop = editor.scrollTop;
    });

    // Load saved code
    const savedCode = localStorage.getItem('codeProSession');
    if (savedCode) {
        editor.value = savedCode;
        updateHighlight();
    }

    // Tab key support
    editor.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            e.preventDefault();
            const start = this.selectionStart;
            const end = this.selectionEnd;
            this.value = this.value.substring(0, start) + '\t' + this.value.substring(end);
            this.selectionStart = this.selectionEnd = start + 1;
        }
    });
}

// Update Syntax Highlighting
function updateHighlight() {
    const editor = document.getElementById('codeEditorPro');
    const highlight = document.getElementById('highlightCodePro');

    let code = editor.value;

    // Keyword highlighting
    code = code.replace(/\b(var|function|if|else|for|while|break|continue|return|print|input|true|false|and|or|not)\b/g, 
        '<span style="color: #569cd6;">$1</span>');
    
    // String highlighting
    code = code.replace(/"[^"]*"/g, match => `<span style="color: #ce9178;">${match}</span>`);
    code = code.replace(/'[^']*'/g, match => `<span style="color: #ce9178;">${match}</span>`);
    
    // Number highlighting
    code = code.replace(/\b\d+\b/g, match => `<span style="color: #b5cea8;">${match}</span>`);
    
    // Comment highlighting
    code = code.replace(/\/\/.*$/gm, match => `<span style="color: #6a9955;">${match}</span>`);

    highlight.innerHTML = code;
}

// Update Line Count
function updateLineCount() {
    const editor = document.getElementById('codeEditorPro');
    const lines = editor.value.split('\n').length;
    const chars = editor.value.length;

    document.getElementById('lineCount').textContent = `Lines: ${lines}`;
    document.getElementById('charCount').textContent = `Chars: ${chars}`;
}

// Real-time Preview Updates
async function realTimeUpdatePreviews() {
    const code = document.getElementById('codeEditorPro').value;

    if (!code.trim()) return;

    try {
        const response = await fetch(`${API_BASE}/lexify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();
        if (result.success) {
            document.getElementById('tokenCount').textContent = result.tokens.length;
        }
    } catch (error) {
        console.log('Preview error:', error);
    }
}

// Setup Event Listeners
function setupEventListeners() {
    document.getElementById('compileProBtn').addEventListener('click', compileCode);
    document.getElementById('stepProBtn').addEventListener('click', stepByStepCompile);
    document.getElementById('clearProBtn').addEventListener('click', clearAll);
    document.getElementById('saveProBtn').addEventListener('click', saveCode);
    document.getElementById('loadProBtn').addEventListener('click', () => document.getElementById('fileInputPro').click());
    document.getElementById('fileInputPro').addEventListener('change', loadCodeFile);

    document.getElementById('copyOutput').addEventListener('click', () => copyToClipboard('outputPro'));
    document.getElementById('clearOutput').addEventListener('click', () => {
        document.getElementById('outputPro').textContent = 'Ready to compile...';
    });

    document.getElementById('sampleSelect').addEventListener('change', function() {
        if (this.value) {
            loadSampleProgram(this.value);
            this.value = '';
        }
    });

    document.getElementById('themeTogglePro').addEventListener('click', toggleTheme);
    document.getElementById('settingsBtn').addEventListener('click', () => showModal('languageGuideModal'));
    document.getElementById('helpBtn').addEventListener('click', () => showModal('keyboardShortcutsModal'));

    // Analysis tabs
    document.querySelectorAll('.tab-nav-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const analysis = this.getAttribute('data-analysis');
            switchAnalysisTab(analysis);
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            e.preventDefault();
            compileCode();
        }
        if (e.ctrlKey && e.shiftKey && e.key === 'Enter') {
            e.preventDefault();
            stepByStepCompile();
        }
        if (e.ctrlKey && e.key === 's') {
            e.preventDefault();
            saveCode();
        }
        if (e.ctrlKey && e.key === 'l') {
            e.preventDefault();
            document.getElementById('fileInputPro').click();
        }
        if (e.ctrlKey && e.shiftKey && e.key === 'c') {
            e.preventDefault();
            clearAll();
        }
    });
}

// Compile Code
async function compileCode() {
    const code = document.getElementById('codeEditorPro').value;

    if (!code.trim()) {
        showStatus('Please enter some code', 'error');
        return;
    }

    const btn = document.getElementById('compileProBtn');
    const originalText = btn.textContent;
    btn.textContent = '⏳ Compiling...';
    btn.disabled = true;

    setCompilationStatus('processing', 'Compiling...');
    const startTime = performance.now();

    try {
        const response = await fetch(`${API_BASE}/compile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();
        const endTime = performance.now();
        currentCompileTime = Math.round(endTime - startTime);

        if (result.success) {
            displayCompilationResults(result);
            setCompilationStatus('ready', 'Success');
            updatePipelineSteps(true);
            showStatus('Compilation successful! ✓', 'success');
        } else {
            displayCompilationError(result.error);
            setCompilationStatus('error', 'Failed');
            updatePipelineSteps(false);
            showStatus('Compilation failed', 'error');
        }
    } catch (error) {
        displayCompilationError(`Error: ${error.message}`);
        setCompilationStatus('error', 'Error');
        showStatus('Server connection error', 'error');
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
        document.getElementById('compilationTime').textContent = `${currentCompileTime}ms`;
    }
}

// Display Compilation Results
function displayCompilationResults(result) {
    // Output
    document.getElementById('outputPro').textContent = result.output || '(No output)';

    // Tokens
    const tokenContainer = document.getElementById('tokensPro');
    if (result.tokens && result.tokens.length > 0) {
        tokenContainer.innerHTML = result.tokens.map(token => `
            <div class="token-item">
                <span class="token-type">${token.type}</span>
                <span class="token-value">${escapeHtml(token.value)}</span>
                <span class="token-location">${token.line}:${token.column}</span>
            </div>
        `).join('');
        document.getElementById('tokenCount').textContent = result.tokens.length;
    } else {
        tokenContainer.innerHTML = '<p class="empty-msg">No tokens found</p>';
    }

    // AST
    if (result.ast) {
        document.getElementById('astPro').textContent = result.ast;
    } else {
        document.getElementById('astPro').innerHTML = '<p class="empty-msg">No AST generated</p>';
    }

    // Errors
    if (result.error) {
        document.getElementById('errorsPro').textContent = result.error;
    } else {
        document.getElementById('errorsPro').innerHTML = '<p class="empty-msg">No errors</p>';
    }
}

// Display Compilation Error
function displayCompilationError(error) {
    document.getElementById('outputPro').textContent = '';
    document.getElementById('tokensPro').innerHTML = '<p class="empty-msg">Compilation failed</p>';
    document.getElementById('astPro').innerHTML = '<p class="empty-msg">Compilation failed</p>';
    document.getElementById('errorsPro').textContent = error || 'Unknown error';
}

// Step-by-Step Compilation
async function stepByStepCompile() {
    const code = document.getElementById('codeEditorPro').value;

    if (!code.trim()) {
        showStatus('Please enter some code', 'error');
        return;
    }

    resetPipelineSteps();
    await performCompilationStep(code, 'lexer');
}

// Perform Compilation Step
async function performCompilationStep(code, step) {
    updatePipelineStep(step, 'processing');

    try {
        let response;
        if (step === 'lexer') {
            response = await fetch(`${API_BASE}/lexify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });
        } else if (step === 'parser') {
            response = await fetch(`${API_BASE}/parse`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });
        } else {
            response = await fetch(`${API_BASE}/compile`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code: code })
            });
        }

        const result = await response.json();

        if (result.success || (step === 'semantic' && result.output !== undefined)) {
            updatePipelineStep(step, 'success');
            showStatus(`${step.charAt(0).toUpperCase() + step.slice(1)} complete ✓`, 'success');

            const nextStep = getNextStep(step);
            if (nextStep) {
                setTimeout(() => performCompilationStep(code, nextStep), 800);
            } else {
                displayCompilationResults(result);
                showStatus('All compilation phases completed! ✓', 'success');
            }
        } else {
            updatePipelineStep(step, 'error');
            displayCompilationError(result.error);
            showStatus(`${step} failed`, 'error');
        }
    } catch (error) {
        updatePipelineStep(step, 'error');
        displayCompilationError(error.message);
        showStatus('Error during compilation', 'error');
    }
}

// Get Next Step
function getNextStep(current) {
    const steps = ['lexer', 'parser', 'semantic', 'interpreter'];
    const index = steps.indexOf(current);
    return index < steps.length - 1 ? steps[index + 1] : null;
}

// Update Pipeline Step
function updatePipelineStep(step, status) {
    const stepElement = document.querySelector(`[data-step="${step}"]`);
    if (!stepElement) return;

    stepElement.classList.remove('ready', 'processing', 'success', 'error');
    stepElement.classList.add(status);

    const statusIndicator = stepElement.querySelector('.pipeline-status');
    if (status === 'success') {
        statusIndicator.textContent = '✓';
        statusIndicator.style.color = '#27ae60';
    } else if (status === 'error') {
        statusIndicator.textContent = '✗';
        statusIndicator.style.color = '#e74c3c';
    } else if (status === 'processing') {
        statusIndicator.textContent = '●';
        statusIndicator.style.color = '#f39c12';
    } else {
        statusIndicator.textContent = '●';
        statusIndicator.style.color = '#95a5a6';
    }
}

// Reset Pipeline Steps
function resetPipelineSteps() {
    document.querySelectorAll('[data-step]').forEach(step => {
        updatePipelineStep(step.getAttribute('data-step'), 'ready');
    });
}

// Update Pipeline Steps
function updatePipelineSteps(success) {
    const steps = ['lexer', 'parser', 'semantic', 'interpreter'];
    steps.forEach(step => {
        updatePipelineStep(step, success ? 'success' : 'error');
    });
}

// Switch Analysis Tab
function switchAnalysisTab(analysis) {
    document.querySelectorAll('.tab-nav-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelectorAll('.analysis-pane').forEach(pane => {
        pane.classList.remove('active');
    });

    document.querySelector(`[data-analysis="${analysis}"]`).classList.add('active');
    document.querySelector(`.analysis-pane[data-analysis="${analysis}"]`).classList.add('active');
}

// Set Compilation Status
function setCompilationStatus(status, text) {
    const statusElement = document.getElementById('compilationStatus');
    statusElement.textContent = text;
    statusElement.classList.remove('ready', 'processing', 'error');
    statusElement.classList.add(status);
}

// Load Sample Program
function loadSampleProgram(name) {
    if (!samples[name]) return;

    document.getElementById('codeEditorPro').value = samples[name];
    updateHighlight();
    updateLineCount();

    // Clear outputs
    document.getElementById('outputPro').textContent = 'Ready to compile...';
    document.getElementById('tokensPro').innerHTML = '<p class="empty-msg">Tokens will appear here...</p>';
    document.getElementById('astPro').innerHTML = '<p class="empty-msg">AST will appear here...</p>';
    document.getElementById('errorsPro').innerHTML = '<p class="empty-msg">No errors</p>';

    resetPipelineSteps();
    localStorage.setItem('codeProSession', samples[name]);
}

// Clear All
function clearAll() {
    if (confirm('Are you sure you want to clear everything?')) {
        document.getElementById('codeEditorPro').value = '';
        updateHighlight();
        updateLineCount();
        document.getElementById('outputPro').textContent = 'Ready to compile...';
        document.getElementById('tokensPro').innerHTML = '<p class="empty-msg">Tokens will appear here...</p>';
        document.getElementById('astPro').innerHTML = '<p class="empty-msg">AST will appear here...</p>';
        document.getElementById('errorsPro').innerHTML = '<p class="empty-msg">No errors</p>';
        resetPipelineSteps();
        localStorage.removeItem('codeProSession');
        showStatus('Cleared', 'info');
    }
}

// Save Code
function saveCode() {
    const code = document.getElementById('codeEditorPro').value;
    if (!code.trim()) {
        showStatus('No code to save', 'error');
        return;
    }

    const blob = new Blob([code], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'program.simple';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    showStatus('File saved!', 'success');
}

// Load Code File
function loadCodeFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('codeEditorPro').value = e.target.result;
        updateHighlight();
        updateLineCount();
        document.getElementById('outputPro').textContent = 'Ready to compile...';
        resetPipelineSteps();
        showStatus('File loaded!', 'success');
    };
    reader.readAsText(file);
}

// Copy to Clipboard
function copyToClipboard(elementId) {
    const element = document.getElementById(elementId);
    const text = element.textContent;

    navigator.clipboard.writeText(text).then(() => {
        showStatus('Copied to clipboard!', 'success');
    }).catch(err => {
        showStatus('Failed to copy', 'error');
    });
}

// Setup Theme
function setupTheme() {
    applyTheme();
}

// Toggle Theme
function toggleTheme() {
    isDarkTheme = !isDarkTheme;
    localStorage.setItem('themePro', isDarkTheme ? 'dark' : 'light');
    applyTheme();
}

// Apply Theme
function applyTheme() {
    const btn = document.getElementById('themeTogglePro');
    if (isDarkTheme) {
        document.body.classList.add('dark-theme');
        btn.textContent = '☀️';
    } else {
        document.body.classList.remove('dark-theme');
        btn.textContent = '🌙';
    }
}

// Show Status Message
function showStatus(message, type) {
    const status = document.createElement('div');
    status.className = `status-message status-${type}`;
    status.textContent = message;
    document.body.appendChild(status);

    setTimeout(() => {
        status.remove();
    }, 3000);
}

// Modal Functions
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.add('active');
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    modal.classList.remove('active');
}

function showLanguageGuide() {
    showModal('languageGuideModal');
}

function showKeyboardShortcuts() {
    showModal('keyboardShortcutsModal');
}

function showAbout() {
    showModal('aboutModal');
}

// Close modal on background click
document.addEventListener('click', function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.classList.remove('active');
    }
});

// Escape to close modal
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        document.querySelectorAll('.modal.active').forEach(modal => {
            modal.classList.remove('active');
        });
    }
});

// Utility: Escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}