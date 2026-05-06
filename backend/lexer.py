"""
LEXICAL ANALYZER (Lexer) for SimpleScript
Tokenizes source code into a stream of tokens
"""

import re
from enum import Enum, auto
from dataclasses import dataclass
from typing import List, Optional


class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    IDENTIFIER = auto()
    
    # Keywords
    VAR = auto()
    FUNCTION = auto()
    IF = auto()
    ELSE = auto()
    FOR = auto()
    WHILE = auto()
    BREAK = auto()
    CONTINUE = auto()
    RETURN = auto()
    PRINT = auto()
    INPUT = auto()
    TRUE = auto()
    FALSE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    
    # Operators
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    ASSIGN = auto()
    EQUAL = auto()
    NOT_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    
    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    SEMICOLON = auto()
    COMMA = auto()
    
    # Special
    EOF = auto()
    NEWLINE = auto()


@dataclass
class Token:
    type: TokenType
    value: any
    line: int
    column: int
    
    def __repr__(self):
        return f"Token({self.type.name}, {repr(self.value)}, {self.line}:{self.column})"


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []
        
        # Keywords mapping
        self.keywords = {
            'var': TokenType.VAR,
            'function': TokenType.FUNCTION,
            'if': TokenType.IF,
            'else': TokenType.ELSE,
            'for': TokenType.FOR,
            'while': TokenType.WHILE,
            'break': TokenType.BREAK,
            'continue': TokenType.CONTINUE,
            'return': TokenType.RETURN,
            'print': TokenType.PRINT,
            'input': TokenType.INPUT,
            'true': TokenType.TRUE,
            'false': TokenType.FALSE,
            'and': TokenType.AND,
            'or': TokenType.OR,
            'not': TokenType.NOT,
        }
    
    def current_char(self) -> Optional[str]:
        """Get current character without advancing"""
        if self.position >= len(self.source):
            return None
        return self.source[self.position]
    
    def peek_char(self, offset=1) -> Optional[str]:
        """Peek ahead"""
        pos = self.position + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self) -> Optional[str]:
        """Move to next character"""
        if self.position >= len(self.source):
            return None
        char = self.source[self.position]
        self.position += 1
        
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        
        return char
    
    def skip_whitespace(self):
        """Skip whitespace except newlines"""
        while self.current_char() and self.current_char() in ' \t\r':
            self.advance()
    
    def skip_comment(self):
        """Skip comments (// style)"""
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_string(self, quote_char: str) -> str:
        """Read string literal"""
        value = ""
        self.advance()  # Skip opening quote
        
        while self.current_char() and self.current_char() != quote_char:
            if self.current_char() == '\\':
                self.advance()
                next_char = self.current_char()
                if next_char == 'n':
                    value += '\n'
                elif next_char == 't':
                    value += '\t'
                elif next_char == '\\':
                    value += '\\'
                elif next_char == quote_char:
                    value += quote_char
                else:
                    value += next_char
                self.advance()
            else:
                value += self.current_char()
                self.advance()
        
        if self.current_char() == quote_char:
            self.advance()  # Skip closing quote
        else:
            raise SyntaxError(f"Unterminated string at line {self.line}")
        
        return value
    
    def read_number(self) -> Token:
        """Read numeric literal"""
        start_line = self.line
        start_col = self.column
        value = ""
        is_float = False
        
        while self.current_char() and (self.current_char().isdigit() or self.current_char() == '.'):
            if self.current_char() == '.':
                if is_float:
                    break  # Second dot, stop
                is_float = True
            value += self.current_char()
            self.advance()
        
        if is_float:
            return Token(TokenType.FLOAT, float(value), start_line, start_col)
        else:
            return Token(TokenType.INTEGER, int(value), start_line, start_col)
    
    def read_identifier(self) -> Token:
        """Read identifier or keyword"""
        start_line = self.line
        start_col = self.column
        value = ""
        
        while self.current_char() and (self.current_char().isalnum() or self.current_char() == '_'):
            value += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.keywords.get(value, TokenType.IDENTIFIER)
        
        # For boolean keywords, set the value appropriately
        if token_type == TokenType.TRUE:
            return Token(token_type, True, start_line, start_col)
        elif token_type == TokenType.FALSE:
            return Token(token_type, False, start_line, start_col)
        else:
            return Token(token_type, value, start_line, start_col)
    
    def tokenize(self) -> List[Token]:
        """Main tokenization function"""
        self.tokens = []
        
        while self.position < len(self.source):
            self.skip_whitespace()
            
            if self.position >= len(self.source):
                break
            
            # Skip comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            char = self.current_char()
            start_line = self.line
            start_col = self.column
            
            # Newline - for now we skip them (statements end with ;)
            if char == '\n':
                self.advance()
                continue
            
            # Strings
            elif char in '"\'':
                value = self.read_string(char)
                self.tokens.append(Token(TokenType.STRING, value, start_line, start_col))
            
            # Numbers
            elif char.isdigit():
                self.tokens.append(self.read_number())
            
            # Identifiers and keywords
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', start_line, start_col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', start_line, start_col))
                self.advance()
            elif char == '%':
                self.tokens.append(Token(TokenType.MODULO, '%', start_line, start_col))
                self.advance()
            elif char == '=' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.EQUAL, '==', start_line, start_col))
                self.advance()
                self.advance()
            elif char == '=' :
                self.tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col))
                self.advance()
            elif char == '!' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.NOT_EQUAL, '!=', start_line, start_col))
                self.advance()
                self.advance()
            elif char == '<' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.LESS_EQUAL, '<=', start_line, start_col))
                self.advance()
                self.advance()
            elif char == '<':
                self.tokens.append(Token(TokenType.LESS, '<', start_line, start_col))
                self.advance()
            elif char == '>' and self.peek_char() == '=':
                self.tokens.append(Token(TokenType.GREATER_EQUAL, '>=', start_line, start_col))
                self.advance()
                self.advance()
            elif char == '>':
                self.tokens.append(Token(TokenType.GREATER, '>', start_line, start_col))
                self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', start_line, start_col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', start_line, start_col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', start_line, start_col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', start_line, start_col))
                self.advance()
            elif char == ';':
                self.tokens.append(Token(TokenType.SEMICOLON, ';', start_line, start_col))
                self.advance()
            elif char == ',':
                self.tokens.append(Token(TokenType.COMMA, ',', start_line, start_col))
                self.advance()
            else:
                raise SyntaxError(f"Unexpected character '{char}' at {start_line}:{start_col}")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
