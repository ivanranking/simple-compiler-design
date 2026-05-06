"""
SEMANTIC ANALYZER for SimpleScript
Performs type checking, variable validation, and scope analysis
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Set
from parser import *


class SemanticError(Exception):
    """Semantic analysis error"""
    pass


@dataclass
class Symbol:
    """Symbol table entry"""
    name: str
    type: str  # 'int', 'float', 'string', 'boolean', 'function'
    value: Optional[Any] = None
    params: List[str] = field(default_factory=list)
    is_initialized: bool = False


class Scope:
    """Represents a scope (global or local)"""
    def __init__(self, parent: Optional['Scope'] = None):
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
    
    def define(self, name: str, symbol: Symbol):
        """Define a symbol in this scope"""
        if name in self.symbols:
            raise SemanticError(f"Symbol '{name}' is already defined in this scope")
        self.symbols[name] = symbol
    
    def lookup(self, name: str) -> Optional[Symbol]:
        """Look up a symbol, searching parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None
    
    def set(self, name: str, value: Any):
        """Set a symbol value"""
        if name in self.symbols:
            self.symbols[name].value = value
            self.symbols[name].is_initialized = True
        elif self.parent:
            self.parent.set(name, value)
        else:
            raise SemanticError(f"Undefined variable '{name}'")


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = Scope()
        self.current_scope = self.global_scope
        self.in_loop = False
        self.in_function = False
        self.current_function_return_type = None
    
    def analyze(self, program: Program) -> Program:
        """Analyze the entire program"""
        for statement in program.statements:
            self.visit_statement(statement)
        return program
    
    def push_scope(self) -> Scope:
        """Create and push a new scope"""
        scope = Scope(self.current_scope)
        self.current_scope = scope
        return scope
    
    def pop_scope(self) -> Scope:
        """Pop the current scope"""
        scope = self.current_scope
        if scope.parent:
            self.current_scope = scope.parent
        return scope
    
    # Statement visitors
    def visit_statement(self, stmt: Statement) -> Any:
        """Visit a statement"""
        if isinstance(stmt, VarDecl):
            return self.visit_var_decl(stmt)
        elif isinstance(stmt, FuncDecl):
            return self.visit_func_decl(stmt)
        elif isinstance(stmt, ExprStmt):
            return self.visit_expr_stmt(stmt)
        elif isinstance(stmt, IfStmt):
            return self.visit_if_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            return self.visit_while_stmt(stmt)
        elif isinstance(stmt, ForStmt):
            return self.visit_for_stmt(stmt)
        elif isinstance(stmt, Block):
            return self.visit_block(stmt)
        elif isinstance(stmt, ReturnStmt):
            return self.visit_return_stmt(stmt)
        elif isinstance(stmt, PrintStmt):
            return self.visit_print_stmt(stmt)
        elif isinstance(stmt, InputStmt):
            return self.visit_input_stmt(stmt)
        elif isinstance(stmt, BreakStmt):
            return self.visit_break_stmt(stmt)
        elif isinstance(stmt, ContinueStmt):
            return self.visit_continue_stmt(stmt)
        else:
            raise SemanticError(f"Unknown statement type: {type(stmt)}")
    
    def visit_var_decl(self, decl: VarDecl) -> Symbol:
        """Visit variable declaration"""
        # Check if already defined in current scope
        if decl.name in self.current_scope.symbols:
            raise SemanticError(f"Variable '{decl.name}' already defined")
        
        # Infer type from initializer
        var_type = 'int'  # default
        if decl.initializer:
            init_type = self.get_expression_type(decl.initializer)
            var_type = init_type
        
        symbol = Symbol(decl.name, var_type)
        self.current_scope.define(decl.name, symbol)
        return symbol
    
    def visit_func_decl(self, decl: FuncDecl) -> Symbol:
        """Visit function declaration"""
        if decl.name in self.current_scope.symbols:
            raise SemanticError(f"Function '{decl.name}' already defined")
        
        # Add function to scope
        symbol = Symbol(decl.name, 'function', params=decl.params)
        self.current_scope.define(decl.name, symbol)
        
        # Create new scope for function body
        self.push_scope()
        prev_in_func = self.in_function
        self.in_function = True
        
        # Add parameters to function scope
        for param in decl.params:
            param_symbol = Symbol(param, 'int')  # Parameters default to int
            self.current_scope.define(param, param_symbol)
        
        # Analyze function body
        for stmt in decl.body:
            self.visit_statement(stmt)
        
        self.in_function = prev_in_func
        self.pop_scope()
        
        return symbol
    
    def visit_expr_stmt(self, stmt: ExprStmt) -> Any:
        """Visit expression statement"""
        return self.visit_expression(stmt.expression)
    
    def visit_if_stmt(self, stmt: IfStmt) -> Any:
        """Visit if statement"""
        # Check condition is boolean
        cond_type = self.get_expression_type(stmt.condition)
        if cond_type != 'boolean':
            # Allow comparison results which are boolean
            pass
        
        self.visit_statement(stmt.then_branch)
        if stmt.else_branch:
            self.visit_statement(stmt.else_branch)
    
    def visit_while_stmt(self, stmt: WhileStmt) -> Any:
        """Visit while statement"""
        cond_type = self.get_expression_type(stmt.condition)
        
        prev_in_loop = self.in_loop
        self.in_loop = True
        self.visit_statement(stmt.body)
        self.in_loop = prev_in_loop
    
    def visit_for_stmt(self, stmt: ForStmt) -> Any:
        """Visit for statement"""
        # Create new scope for loop
        self.push_scope()
        
        if stmt.initializer:
            self.visit_statement(stmt.initializer)
        
        if stmt.condition:
            cond_type = self.get_expression_type(stmt.condition)
        
        prev_in_loop = self.in_loop
        self.in_loop = True
        
        if stmt.increment:
            self.visit_expression(stmt.increment)
        
        self.visit_statement(stmt.body)
        
        self.in_loop = prev_in_loop
        self.pop_scope()
    
    def visit_block(self, stmt: Block) -> Any:
        """Visit block statement"""
        self.push_scope()
        for s in stmt.statements:
            self.visit_statement(s)
        self.pop_scope()
    
    def visit_return_stmt(self, stmt: ReturnStmt) -> Any:
        """Visit return statement"""
        if not self.in_function:
            raise SemanticError("Return statement outside function")
        
        if stmt.value:
            return_type = self.get_expression_type(stmt.value)
    
    def visit_print_stmt(self, stmt: PrintStmt) -> Any:
        """Visit print statement"""
        for arg in stmt.arguments:
            self.visit_expression(arg)
    
    def visit_input_stmt(self, stmt: InputStmt) -> Any:
        """Visit input statement"""
        symbol = self.current_scope.lookup(stmt.variable)
        if not symbol:
            raise SemanticError(f"Undefined variable '{stmt.variable}'")
    
    def visit_break_stmt(self, stmt: BreakStmt) -> Any:
        """Visit break statement"""
        if not self.in_loop:
            raise SemanticError("Break statement outside loop")
    
    def visit_continue_stmt(self, stmt: ContinueStmt) -> Any:
        """Visit continue statement"""
        if not self.in_loop:
            raise SemanticError("Continue statement outside loop")
    
    # Expression visitors
    def visit_expression(self, expr: Expression) -> str:
        """Visit expression and return type"""
        return self.get_expression_type(expr)
    
    def get_expression_type(self, expr: Expression) -> str:
        """Get the type of an expression"""
        if isinstance(expr, Literal):
            return expr.type
        
        elif isinstance(expr, Identifier):
            symbol = self.current_scope.lookup(expr.name)
            if not symbol:
                raise SemanticError(f"Undefined variable '{expr.name}'")
            return symbol.type
        
        elif isinstance(expr, Binary):
            left_type = self.get_expression_type(expr.left)
            right_type = self.get_expression_type(expr.right)
            
            # Type compatibility checking
            if expr.operator in ['+', '-', '*', '/', '%']:
                if left_type not in ['int', 'float'] or right_type not in ['int', 'float']:
                    raise SemanticError(
                        f"Cannot apply {expr.operator} to {left_type} and {right_type}"
                    )
                # Promote to float if either operand is float
                if left_type == 'float' or right_type == 'float':
                    return 'float'
                return 'int'
            
            elif expr.operator in ['<', '>', '<=', '>=', '==', '!=']:
                return 'boolean'
            
            elif expr.operator in ['and', 'or']:
                if left_type != 'boolean' or right_type != 'boolean':
                    raise SemanticError(
                        f"Cannot apply '{expr.operator}' to {left_type} and {right_type}"
                    )
                return 'boolean'
            
            else:
                raise SemanticError(f"Unknown operator: {expr.operator}")
        
        elif isinstance(expr, Unary):
            operand_type = self.get_expression_type(expr.operand)
            
            if expr.operator == '-':
                if operand_type not in ['int', 'float']:
                    raise SemanticError(f"Cannot negate {operand_type}")
                return operand_type
            elif expr.operator == 'not':
                if operand_type != 'boolean':
                    raise SemanticError(f"Cannot apply 'not' to {operand_type}")
                return 'boolean'
            else:
                raise SemanticError(f"Unknown unary operator: {expr.operator}")
        
        elif isinstance(expr, Assignment):
            symbol = self.current_scope.lookup(expr.target)
            if not symbol:
                raise SemanticError(f"Undefined variable '{expr.target}'")
            
            value_type = self.get_expression_type(expr.value)
            # Allow some implicit conversions
            symbol.is_initialized = True
            return value_type
        
        elif isinstance(expr, Call):
            if isinstance(expr.function, Identifier):
                symbol = self.current_scope.lookup(expr.function.name)
                if not symbol:
                    raise SemanticError(f"Undefined function '{expr.function.name}'")
                if symbol.type != 'function':
                    raise SemanticError(f"'{expr.function.name}' is not a function")
                
                if len(expr.arguments) != len(symbol.params):
                    raise SemanticError(
                        f"Function '{expr.function.name}' expects "
                        f"{len(symbol.params)} arguments, got {len(expr.arguments)}"
                    )
                
                # For simplicity, function return type is int
                return 'int'
            else:
                raise SemanticError("Cannot call non-identifier expressions")
        
        else:
            raise SemanticError(f"Unknown expression type: {type(expr)}")
