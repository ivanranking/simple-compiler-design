"""
PARSER for SimpleScript
Builds Abstract Syntax Tree (AST) from tokens
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union, Any
from lexer import Token, TokenType


# AST Node definitions
@dataclass
class ASTNode:
    """Base class for all AST nodes"""
    pass


@dataclass
class Program(ASTNode):
    statements: List['Statement'] = field(default_factory=list)


# Statements
@dataclass
class Statement(ASTNode):
    pass


@dataclass
class VarDecl(Statement):
    name: str
    initializer: Optional['Expression'] = None


@dataclass
class FuncDecl(Statement):
    name: str
    params: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)


@dataclass
class ExprStmt(Statement):
    expression: 'Expression' = None


@dataclass
class IfStmt(Statement):
    condition: 'Expression'
    then_branch: Statement
    else_branch: Optional[Statement] = None


@dataclass
class WhileStmt(Statement):
    condition: 'Expression'
    body: Statement = None


@dataclass
class ForStmt(Statement):
    initializer: Optional[Statement]
    condition: Optional['Expression']
    increment: Optional['Expression']
    body: Statement = None


@dataclass
class Block(Statement):
    statements: List[Statement] = field(default_factory=list)


@dataclass
class ReturnStmt(Statement):
    value: Optional['Expression'] = None


@dataclass
class PrintStmt(Statement):
    arguments: List['Expression'] = field(default_factory=list)


@dataclass
class InputStmt(Statement):
    variable: str = None


@dataclass
class BreakStmt(Statement):
    pass


@dataclass
class ContinueStmt(Statement):
    pass


# Expressions
@dataclass
class Expression(ASTNode):
    pass


@dataclass
class Binary(Expression):
    left: Expression
    operator: str
    right: Expression


@dataclass
class Unary(Expression):
    operator: str
    operand: Expression


@dataclass
class Assignment(Expression):
    target: str
    value: Expression


@dataclass
class Call(Expression):
    function: Expression
    arguments: List[Expression] = field(default_factory=list)


@dataclass
class Identifier(Expression):
    name: str


@dataclass
class Literal(Expression):
    value: Any
    type: str  # 'integer', 'float', 'string', 'boolean'


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.position = 0
    
    def current_token(self) -> Token:
        """Get current token"""
        if self.position >= len(self.tokens):
            return self.tokens[-1]  # Return EOF
        return self.tokens[self.position]
    
    def peek_token(self, offset=1) -> Token:
        """Peek ahead at token"""
        pos = self.position + offset
        if pos >= len(self.tokens):
            return self.tokens[-1]
        return self.tokens[pos]
    
    def advance(self) -> Token:
        """Move to next token"""
        token = self.current_token()
        if self.position < len(self.tokens) - 1:
            self.position += 1
        return token
    
    def match(self, *token_types: TokenType) -> bool:
        """Check if current token matches any type"""
        return self.current_token().type in token_types
    
    def consume(self, token_type: TokenType, message: str) -> Token:
        """Consume a token of expected type or raise error"""
        if not self.match(token_type):
            raise SyntaxError(
                f"{message} at {self.current_token().line}:"
                f"{self.current_token().column}. "
                f"Got {self.current_token().type.name}"
            )
        return self.advance()
    
    def parse(self) -> Program:
        """Parse entire program"""
        statements = []
        while not self.match(TokenType.EOF):
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        return Program(statements)
    
    def declaration(self) -> Optional[Statement]:
        """Parse a declaration (var, function) or statement"""
        if self.match(TokenType.VAR):
            return self.var_declaration()
        elif self.match(TokenType.FUNCTION):
            return self.function_declaration()
        else:
            return self.statement()
    
    def var_declaration(self) -> VarDecl:
        """Parse: var IDENTIFIER ('=' expression)? ';'"""
        self.consume(TokenType.VAR, "Expected 'var'")
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expected ';' after variable declaration")
        return VarDecl(name, initializer)
    
    def function_declaration(self) -> FuncDecl:
        """Parse: function IDENTIFIER '(' params? ')' '{' statements* '}'"""
        self.consume(TokenType.FUNCTION, "Expected 'function'")
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        
        self.consume(TokenType.LPAREN, "Expected '(' after function name")
        
        params = []
        if not self.match(TokenType.RPAREN):
            params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.consume(TokenType.IDENTIFIER, "Expected parameter name").value)
        
        self.consume(TokenType.RPAREN, "Expected ')' after parameters")
        self.consume(TokenType.LBRACE, "Expected '{' before function body")
        
        body = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            stmt = self.declaration()
            if stmt:
                body.append(stmt)
        
        self.consume(TokenType.RBRACE, "Expected '}' after function body")
        return FuncDecl(name, params, body)
    
    def statement(self) -> Statement:
        """Parse a statement"""
        if self.match(TokenType.IF):
            return self.if_statement()
        elif self.match(TokenType.WHILE):
            return self.while_statement()
        elif self.match(TokenType.FOR):
            return self.for_statement()
        elif self.match(TokenType.LBRACE):
            return self.block_statement()
        elif self.match(TokenType.RETURN):
            return self.return_statement()
        elif self.match(TokenType.PRINT):
            return self.print_statement()
        elif self.match(TokenType.INPUT):
            return self.input_statement()
        elif self.match(TokenType.BREAK):
            return self.break_statement()
        elif self.match(TokenType.CONTINUE):
            return self.continue_statement()
        else:
            return self.expression_statement()
    
    def if_statement(self) -> IfStmt:
        """Parse: if '(' expression ')' statement ('else' statement)?"""
        self.consume(TokenType.IF, "Expected 'if'")
        self.consume(TokenType.LPAREN, "Expected '(' after 'if'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        
        then_branch = self.statement()
        else_branch = None
        
        if self.match(TokenType.ELSE):
            self.advance()
            else_branch = self.statement()
        
        return IfStmt(condition, then_branch, else_branch)
    
    def while_statement(self) -> WhileStmt:
        """Parse: while '(' expression ')' statement"""
        self.consume(TokenType.WHILE, "Expected 'while'")
        self.consume(TokenType.LPAREN, "Expected '(' after 'while'")
        condition = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after condition")
        body = self.statement()
        
        return WhileStmt(condition, body)
    
    def for_statement(self) -> ForStmt:
        """Parse: for '(' expr_stmt expression ';' expression ')' statement"""
        self.consume(TokenType.FOR, "Expected 'for'")
        self.consume(TokenType.LPAREN, "Expected '(' after 'for'")
        
        # Initializer
        initializer = None
        if self.match(TokenType.VAR):
            initializer = self.var_declaration()
        elif not self.match(TokenType.SEMICOLON):
            initializer = self.expression_statement()
        else:
            self.advance()  # Skip semicolon
        
        # Condition
        condition = None
        if not self.match(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after condition")
        
        # Increment
        increment = None
        if not self.match(TokenType.RPAREN):
            increment = self.expression()
        self.consume(TokenType.RPAREN, "Expected ')' after for clauses")
        
        body = self.statement()
        return ForStmt(initializer, condition, increment, body)
    
    def block_statement(self) -> Block:
        """Parse: '{' statement* '}'"""
        self.consume(TokenType.LBRACE, "Expected '{'")
        statements = []
        
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            stmt = self.declaration()
            if stmt:
                statements.append(stmt)
        
        self.consume(TokenType.RBRACE, "Expected '}' after block")
        return Block(statements)
    
    def return_statement(self) -> ReturnStmt:
        """Parse: return expression? ';'"""
        self.consume(TokenType.RETURN, "Expected 'return'")
        
        value = None
        if not self.match(TokenType.SEMICOLON):
            value = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expected ';' after return")
        return ReturnStmt(value)
    
    def print_statement(self) -> PrintStmt:
        """Parse: print '(' expression (',' expression)* ')' ';'"""
        self.consume(TokenType.PRINT, "Expected 'print'")
        self.consume(TokenType.LPAREN, "Expected '(' after 'print'")
        
        arguments = []
        if not self.match(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                self.advance()
                arguments.append(self.expression())
        
        self.consume(TokenType.RPAREN, "Expected ')' after print arguments")
        self.consume(TokenType.SEMICOLON, "Expected ';' after print statement")
        
        return PrintStmt(arguments)
    
    def input_statement(self) -> InputStmt:
        """Parse: input '(' IDENTIFIER ')' ';'"""
        self.consume(TokenType.INPUT, "Expected 'input'")
        self.consume(TokenType.LPAREN, "Expected '(' after 'input'")
        variable = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        self.consume(TokenType.RPAREN, "Expected ')' after variable")
        self.consume(TokenType.SEMICOLON, "Expected ';' after input statement")
        
        return InputStmt(variable)
    
    def break_statement(self) -> BreakStmt:
        """Parse: break ';'"""
        self.consume(TokenType.BREAK, "Expected 'break'")
        self.consume(TokenType.SEMICOLON, "Expected ';' after 'break'")
        return BreakStmt()
    
    def continue_statement(self) -> ContinueStmt:
        """Parse: continue ';'"""
        self.consume(TokenType.CONTINUE, "Expected 'continue'")
        self.consume(TokenType.SEMICOLON, "Expected ';' after 'continue'")
        return ContinueStmt()
    
    def expression_statement(self) -> ExprStmt:
        """Parse: expression ';'"""
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expected ';' after expression")
        return ExprStmt(expr)
    
    def expression(self) -> Expression:
        """Parse expression (lowest precedence)"""
        return self.assignment()
    
    def assignment(self) -> Expression:
        """Parse: identifier '=' assignment | logical_or"""
        expr = self.logical_or()
        
        if self.match(TokenType.ASSIGN):
            if isinstance(expr, Identifier):
                self.advance()
                value = self.assignment()
                return Assignment(expr.name, value)
            else:
                raise SyntaxError("Invalid assignment target")
        
        return expr
    
    def logical_or(self) -> Expression:
        """Parse: logical_and ('or' logical_and)*"""
        left = self.logical_and()
        
        while self.match(TokenType.OR):
            op = self.advance().value
            right = self.logical_and()
            left = Binary(left, op, right)
        
        return left
    
    def logical_and(self) -> Expression:
        """Parse: equality ('and' equality)*"""
        left = self.equality()
        
        while self.match(TokenType.AND):
            op = self.advance().value
            right = self.equality()
            left = Binary(left, op, right)
        
        return left
    
    def equality(self) -> Expression:
        """Parse: comparison (('==' | '!=') comparison)*"""
        left = self.comparison()
        
        while self.match(TokenType.EQUAL, TokenType.NOT_EQUAL):
            op = self.advance().value
            right = self.comparison()
            left = Binary(left, op, right)
        
        return left
    
    def comparison(self) -> Expression:
        """Parse: additive (('<' | '>' | '<=' | '>=') additive)*"""
        left = self.additive()
        
        while self.match(TokenType.LESS, TokenType.GREATER, 
                         TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL):
            op = self.advance().value
            right = self.additive()
            left = Binary(left, op, right)
        
        return left
    
    def additive(self) -> Expression:
        """Parse: multiplicative (('+' | '-') multiplicative)*"""
        left = self.multiplicative()
        
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            right = self.multiplicative()
            left = Binary(left, op, right)
        
        return left
    
    def multiplicative(self) -> Expression:
        """Parse: unary (('*' | '/' | '%') unary)*"""
        left = self.unary()
        
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            right = self.unary()
            left = Binary(left, op, right)
        
        return left
    
    def unary(self) -> Expression:
        """Parse: ('not' | '-') unary | postfix"""
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.advance().value
            operand = self.unary()
            return Unary(op, operand)
        
        return self.postfix()
    
    def postfix(self) -> Expression:
        """Parse: primary ('(' arguments? ')')*"""
        expr = self.primary()
        
        while self.match(TokenType.LPAREN):
            self.advance()
            arguments = []
            
            if not self.match(TokenType.RPAREN):
                arguments.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.expression())
            
            self.consume(TokenType.RPAREN, "Expected ')' after arguments")
            expr = Call(expr, arguments)
        
        return expr
    
    def primary(self) -> Expression:
        """Parse: NUMBER | STRING | IDENTIFIER | TRUE | FALSE | '(' expression ')'"""
        
        if self.match(TokenType.INTEGER):
            value = self.advance().value
            return Literal(value, 'integer')
        
        elif self.match(TokenType.FLOAT):
            value = self.advance().value
            return Literal(value, 'float')
        
        elif self.match(TokenType.STRING):
            value = self.advance().value
            return Literal(value, 'string')
        
        elif self.match(TokenType.TRUE):
            self.advance()
            return Literal(True, 'boolean')
        
        elif self.match(TokenType.FALSE):
            self.advance()
            return Literal(False, 'boolean')
        
        elif self.match(TokenType.IDENTIFIER):
            name = self.advance().value
            return Identifier(name)
        
        elif self.match(TokenType.LPAREN):
            self.advance()
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')' after expression")
            return expr
        
        else:
            raise SyntaxError(
                f"Unexpected token {self.current_token().type.name} "
                f"at {self.current_token().line}:{self.current_token().column}"
            )
