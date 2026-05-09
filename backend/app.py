"""
FLASK BACKEND for SimpleScript Compiler
Provides REST API for compilation and execution
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import sys
import os
from io import StringIO
from lexer import Lexer, Token, TokenType
from parser import Parser
from semantic_analyzer import SemanticAnalyzer, SemanticError
from interpreter import Interpreter, RuntimeError as InterpreterError

app = Flask(__name__)
CORS(app)


def serialize_token(token: Token) -> dict:
    """Serialize a token to JSON"""
    return {
        'type': token.type.name,
        'value': str(token.value),
        'line': token.line,
        'column': token.column
    }


def format_ast(node, indent=0) -> str:
    """Format AST as string"""
    indent_str = "  " * indent
    
    if node is None:
        return f"{indent_str}None"
    
    class_name = node.__class__.__name__
    result = f"{indent_str}{class_name}"
    
    # Get the fields from dataclass
    if hasattr(node, '__dataclass_fields__'):
        field_values = []
        for field_name, field_obj in node.__dataclass_fields__.items():
            value = getattr(node, field_name)
            
            if isinstance(value, list):
                if value and hasattr(value[0], '__dataclass_fields__'):
                    # List of AST nodes
                    result += f"\n{indent_str}  {field_name}:"
                    for item in value:
                        result += "\n" + format_ast(item, indent + 2)
                else:
                    # List of primitives
                    result += f"\n{indent_str}  {field_name}: {value}"
            elif hasattr(value, '__dataclass_fields__'):
                # Single AST node
                result += f"\n{indent_str}  {field_name}:"
                result += "\n" + format_ast(value, indent + 2)
            else:
                # Primitive value
                result += f"\n{indent_str}  {field_name}: {value}"
    
    return result


@app.route('/api/compile', methods=['POST'])
def compile_code():
    """
    Compile and run SimpleScript code
    Expected JSON: {"code": "..."}
    Returns: {
        "success": bool,
        "tokens": [...],
        "ast": "...",
        "output": "...",
        "error": "..." (if error)
    }
    """
    data = request.json
    code = data.get('code', '')
    
    result = {
        'success': False,
        'tokens': [],
        'ast': None,
        'output': '',
        'error': None
    }
    
    try:
        # PHASE 1: Lexical Analysis
        print(f"[DEBUG] Lexing code: {code[:50]}...")
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        result['tokens'] = [serialize_token(t) for t in tokens if t.type != TokenType.EOF]
        
        # PHASE 2: Syntax Analysis (Parsing)
        print(f"[DEBUG] Parsing {len(tokens)} tokens...")
        parser = Parser(tokens)
        ast = parser.parse()
        result['ast'] = format_ast(ast)
        
        # PHASE 3: Semantic Analysis
        print("[DEBUG] Performing semantic analysis...")
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.analyze(ast)
        
        # PHASE 4 & 5: Interpretation/Execution
        print("[DEBUG] Executing...")
        interpreter = Interpreter()
        output = interpreter.interpret(ast)
        result['output'] = output
        result['success'] = True
        
    except SyntaxError as e:
        result['error'] = f"Syntax Error: {str(e)}"
    except SemanticError as e:
        result['error'] = f"Semantic Error: {str(e)}"
    except InterpreterError as e:
        result['error'] = f"Runtime Error: {str(e)}"
    except Exception as e:
        result['error'] = f"Error: {type(e).__name__}: {str(e)}"
    
    return jsonify(result)


@app.route('/api/lexify', methods=['POST'])
def lexify_only():
    """Only perform lexical analysis"""
    data = request.json
    code = data.get('code', '')
    
    result = {
        'success': False,
        'tokens': [],
        'error': None
    }
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        result['tokens'] = [serialize_token(t) for t in tokens if t.type != TokenType.EOF]
        result['success'] = True
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)


@app.route('/api/parse', methods=['POST'])
def parse_only():
    """Only perform lexical and syntax analysis"""
    data = request.json
    code = data.get('code', '')
    
    result = {
        'success': False,
        'ast': None,
        'error': None
    }
    
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize()
        parser = Parser(tokens)
        ast = parser.parse()
        result['ast'] = format_ast(ast)
        result['success'] = True
    except SyntaxError as e:
        result['error'] = f"Syntax Error: {str(e)}"
    except Exception as e:
        result['error'] = str(e)
    
    return jsonify(result)


@app.route('/api/language-spec', methods=['GET'])
def language_spec():
    """Get language specification"""
    return jsonify({
        'keywords': [
            'var', 'function', 'if', 'else', 'for', 'while',
            'break', 'continue', 'return', 'print', 'input',
            'true', 'false', 'and', 'or', 'not'
        ],
        'operators': [
            '+', '-', '*', '/', '%', '=', '==', '!=',
            '<', '>', '<=', '>=', 'and', 'or', 'not'
        ],
        'types': ['int', 'float', 'string', 'boolean']
    })


@app.route('/api/info', methods=['GET'])
def info():
    """Backend info endpoint"""
    return jsonify({
        'message': 'SimpleScript compiler backend',
        'routes': [
            '/health',
            '/api/compile',
            '/api/lexify',
            '/api/parse',
            '/api/language-spec'
        ]
    })


@app.route('/', methods=['GET'])
def index():
    """Serve the frontend selection page"""
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    return send_from_directory(frontend_dir, 'home.html')


@app.route('/<path:filename>', methods=['GET'])
def serve_frontend(filename):
    """Serve frontend static files and HTML pages"""
    frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))
    safe_path = os.path.normpath(filename)
    if safe_path.startswith('..'):
        return jsonify({'error': 'Invalid file path'}), 400
    return send_from_directory(frontend_dir, safe_path)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
