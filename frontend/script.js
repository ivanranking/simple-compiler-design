// SimpleScript Compiler Frontend

const API_BASE = 'http://localhost:5000/api';

// Sample Programs
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

    loop: `// Loop Example
print("Counting from 1 to 5:");
for (var i = 1; i <= 5; i = i + 1) {
    print("Count: ", i);
}`,

    function: `// Function Demo
function multiply(x, y) {
    return x * y;
}

var result = multiply(6, 7);
print("6 * 7 = ", result);`,

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

var result = factorial(5);
print("Factorial of 5 = ", result);`
};

// Global state
let isDarkTheme = localStorage.getItem('theme') === 'dark';
let autoCompileEnabled = localStorage.getItem('autoCompile') === 'true';
let compileTimeout;
let currentStep = 0;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    setupEditor();
    setupEventListeners();
    setupTheme();
    setupAutoCompile();
    setupKeyboardShortcutsModal();
    loadSampleProgram('hello');
});

// Setup Code Editor with Syntax Highlighting
function setupEditor() {
    const editor = document.getElementById('codeEditor');
    const highlight = document.getElementById('highlightCode');

    editor.addEventListener('input', function() {
        updateHighlight();
        if (autoCompileEnabled) {
            debouncedRealTimeCompile();
        }
        localStorage.setItem('simplescript_code', editor.value);
    });

    editor.addEventListener('scroll', function() {
        document.getElementById('highlight').scrollLeft = editor.scrollLeft;
        document.getElementById('highlight').scrollTop = editor.scrollTop;
    });

    const savedCode = localStorage.getItem('simplescript_code');
    if (savedCode) {
        editor.value = savedCode;
        updateHighlight();
    }
}

// Update Syntax Highlighting
function updateHighlight() {
    const editor = document.getElementById('codeEditor');
    const highlight = document.getElementById('highlightCode');

    let code = editor.value;

    code = code.replace(/\b(var|function|if|else|for|while|break|continue|return|print|input|true|false|and|or|not)\b/g, '<span class="hljs-keyword">$1</span>');
    code = code.replace(/"[^"]*"/g, match => `<span class="hljs-string">${match}</span>`);
    code = code.replace(/'[^']*'/g, match => `<span class="hljs-string">${match}</span>`);
    code = code.replace(/\b\d+\b/g, match => `<span class="hljs-number">${match}</span>`);
    code = code.replace(/\/\/.*$/gm, match => `<span style="color: #6a9955;">${match}</span>`);

    highlight.innerHTML = code;
}

// Debounced Real-time Compile
function debouncedRealTimeCompile() {
    clearTimeout(compileTimeout);
    compileTimeout = setTimeout(() => {
        realTimeCompile();
    }, 1000);
}

// Real-time Compile for Preview
async function realTimeCompile() {
    const code = document.getElementById('codeEditor').value;

    if (!code.trim()) {
        clearPreviews();
        return;
    }

    try {
        const lexResponse = await fetch(`${API_BASE}/lexify`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const lexResult = await lexResponse.json();
        updateLexicalPreview(lexResult);

        const parseResponse = await fetch(`${API_BASE}/parse`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const parseResult = await parseResponse.json();
        updateParsePreview(parseResult);

    } catch (error) {
        console.log('Real-time compile error:', error);
    }
}

// Update Lexical Preview
function updateLexicalPreview(result) {
    const preview = document.getElementById('lexicalPreview');

    if (result.success && result.tokens.length > 0) {
        const tokenHtml = result.tokens.slice(0, 10).map(token =>
            `<span class="preview-token ${token.type.toLowerCase()}">${token.type}: ${escapeHtml(token.value)}</span>`
        ).join(' ');

        const remaining = result.tokens.length > 10 ? ` ... and ${result.tokens.length - 10} more` : '';
        preview.innerHTML = tokenHtml + remaining;
    } else {
        preview.innerHTML = '<span class="preview-error">Lexical errors detected</span>';
    }
}

// Update Parse Preview
function updateParsePreview(result) {
    const preview = document.getElementById('parsePreview');

    if (result.success && result.ast) {
        const astLines = result.ast.split('\n').slice(0, 5);
        preview.innerHTML = astLines.join('<br>') + (result.ast.split('\n').length > 5 ? '<br>...' : '');
    } else {
        preview.innerHTML = '<span class="preview-error">Parse errors detected</span>';
    }
}

// Clear Previews
function clearPreviews() {
    document.getElementById('lexicalPreview').innerHTML = 'Start typing to see tokens...';
    document.getElementById('parsePreview').innerHTML = 'Start typing to see AST...';
}

// Setup Theme
function setupTheme() {
    const themeToggle = document.getElementById('themeToggle');
    applyTheme();
    themeToggle.addEventListener('click', toggleTheme);
}

// Toggle Theme
function toggleTheme() {
    isDarkTheme = !isDarkTheme;
    localStorage.setItem('theme', isDarkTheme ? 'dark' : 'light');
    applyTheme();
    updateThemeButton();
}

// Apply Theme
function applyTheme() {
    document.body.classList.toggle('dark-theme', isDarkTheme);
    updateThemeButton();
}

// Update Theme Button
function updateThemeButton() {
    const themeToggle = document.getElementById('themeToggle');
    themeToggle.innerHTML = isDarkTheme ? '<i class="fas fa-sun"></i> Light Mode' : '<i class="fas fa-moon"></i> Dark Mode';
}

// Setup Auto Compile
function setupAutoCompile() {
    const autoCompileToggle = document.getElementById('autoCompileToggle');
    updateAutoCompileButton();
    autoCompileToggle.addEventListener('click', toggleAutoCompile);
}

// Toggle Auto Compile
function toggleAutoCompile() {
    autoCompileEnabled = !autoCompileEnabled;
    localStorage.setItem('autoCompile', autoCompileEnabled);
    updateAutoCompileButton();

    if (autoCompileEnabled) {
        showInfo('Auto-compile enabled');
        realTimeCompile();
    } else {
        showInfo('Auto-compile disabled');
        clearTimeout(compileTimeout);
    }
}

// Update Auto Compile Button
function updateAutoCompileButton() {
    const autoCompileToggle = document.getElementById('autoCompileToggle');
    autoCompileToggle.innerHTML = autoCompileEnabled ? '<i class="fas fa-pause"></i> Stop Auto' : '<i class="fas fa-bolt"></i> Auto-Compile';
    autoCompileToggle.classList.toggle('active', autoCompileEnabled);
}

// Setup Keyboard Shortcuts Modal
function setupKeyboardShortcutsModal() {
    const shortcutsBtn = document.getElementById('shortcutsBtn');
    const closeModal = document.getElementById('closeModal');
    const modal = document.getElementById('shortcutsModal');

    shortcutsBtn.addEventListener('click', () => {
        modal.classList.remove('hidden');
    });

    closeModal.addEventListener('click', () => {
        modal.classList.add('hidden');
    });

    modal.addEventListener('click', (e) => {
        if (e.target === modal) {
            modal.classList.add('hidden');
        }
    });
}

// Setup Event Listeners
function setupEventListeners() {
    document.getElementById('compileBtn').addEventListener('click', compileCode);
    document.getElementById('stepCompileBtn').addEventListener('click', stepByStepCompile);
    document.getElementById('clearBtn').addEventListener('click', function() {
        document.getElementById('codeEditor').value = '';
        updateHighlight();
        clearOutput();
        clearPreviews();
        resetPipelineSteps();
    });
    document.getElementById('saveBtn').addEventListener('click', saveCodeFile);
    document.getElementById('loadBtn').addEventListener('click', function() {
        document.getElementById('fileInput').click();
    });
    document.getElementById('fileInput').addEventListener('change', loadCodeFile);
    document.getElementById('copyOutputBtn').addEventListener('click', copyOutput);
    document.getElementById('copyAstBtn').addEventListener('click', copyAst);

    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            switchTab(this.getAttribute('data-tab'));
        });
    });

    document.querySelectorAll('.sample-btn').forEach(button => {
        button.addEventListener('click', function() {
            loadSampleProgram(this.getAttribute('data-sample'));
        });
    });
}

// Copy Output
function copyOutput() {
    const output = document.getElementById('output').textContent;
    navigator.clipboard.writeText(output).then(() => {
        showSuccess('Output copied to clipboard!');
    });
}

// Copy AST
function copyAst() {
    const ast = document.getElementById('ast').textContent;
    navigator.clipboard.writeText(ast).then(() => {
        showSuccess('AST copied to clipboard!');
    });
}

// Load Sample Program
function loadSampleProgram(name) {
    const editor = document.getElementById('codeEditor');
    editor.value = samples[name];
    updateHighlight();
    clearOutput();
    clearPreviews();
    resetPipelineSteps();
}

// Compile Code
async function compileCode() {
    const code = document.getElementById('codeEditor').value;

    if (!code.trim()) {
        showError('Please enter some code to compile');
        return;
    }

    const compileBtn = document.getElementById('compileBtn');
    const originalText = compileBtn.innerHTML;
    compileBtn.innerHTML = '<span class="loading"></span>Compiling...';
    compileBtn.disabled = true;

    resetPipelineSteps();

    try {
        const response = await fetch(`${API_BASE}/compile`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();

        if (result.success) {
            displayOutput(result);
            updatePipelineSteps(true);
            showSuccess('Compilation successful!');
        } else {
            displayError(result.error);
            updatePipelineSteps(false, result.error);
            showError('Compilation failed');
        }
    } catch (error) {
        displayError(`Network Error: ${error.message}`);
        updatePipelineSteps(false, error.message);
        showError('Failed to reach compiler server');
    } finally {
        compileBtn.innerHTML = originalText;
        compileBtn.disabled = false;
    }
}

// Step-by-Step Compile
async function stepByStepCompile() {
    const code = document.getElementById('codeEditor').value;

    if (!code.trim()) {
        showError('Please enter some code to compile');
        return;
    }

    resetPipelineSteps();
    currentStep = 0;

    const btn = document.getElementById('stepCompileBtn');
    const originalText = btn.textContent;
    btn.innerHTML = '<i class="fas fa-shoe-prints"></i> Next Step';
    btn.disabled = false;

    await performStep(code, 'lexer');
}

// Perform Individual Compilation Step
async function performStep(code, step) {
    updatePipelineStep(step, 'processing');

    try {
        let endpoint, stepName;

        switch (step) {
            case 'lexer':
                endpoint = '/lexify';
                stepName = 'Lexical Analysis';
                break;
            case 'parser':
                endpoint = '/parse';
                stepName = 'Syntax Analysis';
                break;
            case 'semantic':
                await performFullSemanticCheck(code);
                return;
            case 'interpreter':
                await performFullExecution(code);
                return;
        }

        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();

        if (result.success) {
            updatePipelineStep(step, 'success');
            showInfo(`${stepName} completed successfully`);

            currentStep++;
            const nextStep = getNextStep(step);
            if (nextStep) {
                setTimeout(() => performStep(code, nextStep), 1000);
            } else {
                document.getElementById('stepCompileBtn').innerHTML = '<i class="fas fa-check"></i> Complete';
                setTimeout(() => {
                    document.getElementById('stepCompileBtn').textContent = originalText;
                }, 2000);
            }
        } else {
            updatePipelineStep(step, 'error', result.error);
            showError(`${stepName} failed: ${result.error}`);
            document.getElementById('stepCompileBtn').textContent = originalText;
        }
    } catch (error) {
        updatePipelineStep(step, 'error', error.message);
        showError(`Step failed: ${error.message}`);
        document.getElementById('stepCompileBtn').textContent = originalText;
    }
}

// Perform Full Semantic Check
async function performFullSemanticCheck(code) {
    try {
        const response = await fetch(`${API_BASE}/compile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();

        if (result.success || result.error.includes('Runtime')) {
            updatePipelineStep('semantic', 'success');
            showInfo('Semantic Analysis completed successfully');
            setTimeout(() => performStep(code, 'interpreter'), 1000);
        } else {
            updatePipelineStep('semantic', 'error', result.error);
            showError(`Semantic Analysis failed: ${result.error}`);
        }
    } catch (error) {
        updatePipelineStep('semantic', 'error', error.message);
        showError(`Semantic Analysis failed: ${error.message}`);
    }
}

// Perform Full Execution
async function performFullExecution(code) {
    try {
        const response = await fetch(`${API_BASE}/compile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: code })
        });

        const result = await response.json();

        if (result.success) {
            displayOutput(result);
            updatePipelineStep('interpreter', 'success');
            showSuccess('Execution completed successfully!');
        } else {
            displayError(result.error);
            updatePipelineStep('interpreter', 'error', result.error);
            showError(`Execution failed: ${result.error}`);
        }
    } catch (error) {
        displayError(`Network Error: ${error.message}`);
        updatePipelineStep('interpreter', 'error', error.message);
        showError(`Execution failed: ${error.message}`);
    }
}

// Get Next Step
function getNextStep(currentStep) {
    const steps = ['lexer', 'parser', 'semantic', 'interpreter'];
    const currentIndex = steps.indexOf(currentStep);
    return currentIndex < steps.length - 1 ? steps[currentIndex + 1] : null;
}

// Update Pipeline Step
function updatePipelineStep(step, status, error = null) {
    const stepElement = document.querySelector(`[data-step="${step}"]`);
    const statusElement = stepElement.querySelector('.step-status');

    stepElement.classList.remove('processing', 'success', 'error', 'ready');
    stepElement.classList.add(status);

    switch (status) {
        case 'processing':
            statusElement.textContent = 'Processing...';
            break;
        case 'success':
            statusElement.textContent = '✓ Complete';
            break;
        case 'error':
            statusElement.textContent = '✗ Failed';
            if (error) {
                statusElement.title = error;
            }
            break;
        default:
            statusElement.textContent = 'Ready';
    }
}

// Update Pipeline Steps
function updatePipelineSteps(success, error = null) {
    const steps = ['lexer', 'parser', 'semantic', 'interpreter'];

    steps.forEach(step => {
        updatePipelineStep(step, success ? 'success' : 'error', error);
    });
}

// Reset Pipeline Steps
function resetPipelineSteps() {
    const steps = ['lexer', 'parser', 'semantic', 'interpreter'];

    steps.forEach(step => {
        updatePipelineStep(step, 'ready');
    });
}

// Display Output
function displayOutput(result) {
    if (result.output) {
        document.getElementById('output').textContent = result.output || 'No output';
    } else {
        document.getElementById('output').textContent = '(No output produced)';
    }

    const tokenList = document.getElementById('tokenList');
    if (result.tokens && result.tokens.length > 0) {
        tokenList.innerHTML = result.tokens.map(token => `
            <div class="token-item">
                <span class="token-type">${token.type}</span>:
                <span class="token-value">${escapeHtml(token.value)}</span>
                <span class="token-location">(${token.line}:${token.column})</span>
            </div>
        `).join('');
    } else {
        tokenList.innerHTML = '<p>No tokens found</p>';
    }

    if (result.ast) {
        document.getElementById('ast').textContent = result.ast;
    } else {
        document.getElementById('ast').textContent = 'No AST generated';
    }

    if (result.error) {
        document.getElementById('errors').textContent = result.error;
    } else {
        document.getElementById('errors').textContent = 'No errors';
    }
}

// Display Error
function displayError(error) {
    document.getElementById('output').textContent = '';
    document.getElementById('tokenList').innerHTML = '<p>Compilation failed</p>';
    document.getElementById('ast').textContent = '';
    document.getElementById('errors').textContent = error || 'Unknown error occurred';
}

// Switch Tab
function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });

    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    const tabId = tabName + '-tab';
    const tabElement = document.getElementById(tabId);
    if (tabElement) {
        tabElement.classList.add('active');
    }

    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
}

// Clear Output
function clearOutput() {
    document.getElementById('output').textContent = 'Ready to compile...';
    document.getElementById('tokenList').innerHTML = '<p>Tokens will appear here after compilation</p>';
    document.getElementById('ast').textContent = 'AST will appear here after parsing';
    document.getElementById('errors').textContent = 'No errors';
}

// Save Code to File
function saveCodeFile() {
    const code = document.getElementById('codeEditor').value;
    if (!code.trim()) {
        showError('No code to save');
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
    showSuccess('File saved!');
}

// Load Code from File
function loadCodeFile(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('codeEditor').value = e.target.result;
        updateHighlight();
        clearOutput();
        clearPreviews();
        resetPipelineSteps();
        showSuccess('File loaded!');
    };
    reader.readAsText(file);
}

// Show Status Messages
function showSuccess(message) {
    showStatus(message, 'success');
}

function showError(message) {
    showStatus(message, 'error');
}

function showInfo(message) {
    showStatus(message, 'info');
}

function showStatus(message, type) {
    const status = document.createElement('div');
    status.className = `status-message status-${type}`;
    status.textContent = message;

    const header = document.querySelector('.header');
    header.parentNode.insertBefore(status, header.nextSibling);

    setTimeout(() => {
        status.remove();
    }, 5000);
}

// Utility function to escape HTML
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

// Keyboard Shortcuts
document.addEventListener('keydown', function(event) {
    if (event.ctrlKey && event.key === 'Enter') {
        event.preventDefault();
        compileCode();
    }

    if (event.ctrlKey && event.shiftKey && event.key === 'Enter') {
        event.preventDefault();
        stepByStepCompile();
    }

    if (event.key === 'Tab' && document.activeElement.id === 'codeEditor') {
        event.preventDefault();
        const editor = document.getElementById('codeEditor');
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        editor.value = editor.value.substring(0, start) + '\t' + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + 1;
        updateHighlight();
    }
});

// Alert user about unsaved changes
window.addEventListener('beforeunload', function(event) {
    const currentCode = document.getElementById('codeEditor').value;
    const savedCode = localStorage.getItem('simplescript_code') || '';
    if (currentCode !== savedCode && currentCode.trim()) {
        event.returnValue = '';
    }
});