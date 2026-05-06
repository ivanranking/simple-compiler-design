"""
Simple HTTP Server for SimpleScript Compiler
A Flask-free server that works with Python 3.14+
"""

import http.server
import socketserver
import json
import urllib.parse
import sys
import os
from io import StringIO

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from lexer import Lexer, Token, TokenType
from parser import Parser
from semantic_analyzer import SemanticAnalyzer, SemanticError
from interpreter import Interpreter, RuntimeError as InterpreterError

class CompilerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to serve files from
        super().__init__(*args, directory=os.path.join(os.path.dirname(__file__), '..', 'frontend'), **kwargs)

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/':
            self.path = '/home.html'
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
            return
        elif self.path == '/api/language-spec':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            spec = {
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
            }
            self.wfile.write(json.dumps(spec).encode())
            return

        return super().do_GET()

    def do_POST(self):
        """Handle POST requests"""
        if self.path.startswith('/api/'):
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode())

            if self.path == '/api/compile':
                result = self.compile_code(data)
            elif self.path == '/api/lexify':
                result = self.lexify_only(data)
            elif self.path == '/api/parse':
                result = self.parse_only(data)
            else:
                result = {'error': 'Unknown endpoint'}

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def serialize_token(self, token: Token) -> dict:
        """Serialize a token to JSON"""
        return {
            'type': token.type.name,
            'value': str(token.value),
            'line': token.line,
            'column': token.column
        }

    def format_ast(self, node, indent=0) -> str:
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
                            result += "\n" + self.format_ast(item, indent + 2)
                    else:
                        # List of primitives
                        result += f"\n{indent_str}  {field_name}: {value}"
                elif hasattr(value, '__dataclass_fields__'):
                    # Single AST node
                    result += f"\n{indent_str}  {field_name}:"
                    result += "\n" + self.format_ast(value, indent + 2)
                else:
                    # Primitive value
                    result += f"\n{indent_str}  {field_name}: {value}"

        return result

    def compile_code(self, data):
        """Compile and run SimpleScript code"""
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
            result['tokens'] = [self.serialize_token(t) for t in tokens if t.type != TokenType.EOF]

            # PHASE 2: Syntax Analysis (Parsing)
            print(f"[DEBUG] Parsing {len(tokens)} tokens...")
            parser = Parser(tokens)
            ast = parser.parse()
            result['ast'] = self.format_ast(ast)

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

        return result

    def lexify_only(self, data):
        """Only perform lexical analysis"""
        code = data.get('code', '')

        result = {
            'success': False,
            'tokens': [],
            'error': None
        }

        try:
            lexer = Lexer(code)
            tokens = lexer.tokenize()
            result['tokens'] = [self.serialize_token(t) for t in tokens if t.type != TokenType.EOF]
            result['success'] = True
        except Exception as e:
            result['error'] = str(e)

        return result

    def parse_only(self, data):
        """Only perform lexical and syntax analysis"""
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
            result['ast'] = self.format_ast(ast)
            result['success'] = True
        except SyntaxError as e:
            result['error'] = f"Syntax Error: {str(e)}"
        except Exception as e:
            result['error'] = str(e)

        return result

def run_server(port=5000):
    """Run the HTTP server"""
    import webbrowser
    import threading
    
    def open_browser():
        import time
        time.sleep(1)
        webbrowser.open(f'http://localhost:{port}')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    with socketserver.TCPServer(("", port), CompilerHandler) as httpd:
        print(f"🚀 SimpleScript Compiler Server running on http://localhost:{port}")
        print(f"📁 Serving frontend from: {os.path.join(os.path.dirname(__file__), '..', 'frontend')}")
        print("📖 Opening interface in your browser...")
        print("Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
            httpd.shutdown()

if __name__ == '__main__':
    run_server()