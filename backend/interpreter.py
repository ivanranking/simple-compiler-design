"""
CODE GENERATOR AND INTERPRETER for SimpleScript
Executes the AST directly (tree-walking interpreter)
Also generates intermediate three-address code representation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from parser import *
import sys


class RuntimeError(Exception):
    """Runtime execution error"""
    pass


class BreakException(Exception):
    """Signal to break from a loop"""
    pass


class ContinueException(Exception):
    """Signal to continue to next iteration"""
    pass


class ReturnException(Exception):
    """Signal to return from function"""
    def __init__(self, value=None):
        self.value = value


@dataclass
class TAC:
    """Three-Address Code instruction"""
    op: str  # 'assign', 'add', 'sub', 'mul', 'div', 'mod', 'label', 'goto', 'if_goto', etc.
    arg1: Optional[str] = None
    arg2: Optional[str] = None
    result: Optional[str] = None
    
    def __repr__(self):
        if self.result:
            return f"{self.result} = {self.op} {self.arg1} {self.arg2 or ''}"
        elif self.arg2:
            return f"{self.op} {self.arg1}, {self.arg2}"
        elif self.arg1:
            return f"{self.op} {self.arg1}"
        else:
            return f"{self.op}"


class CodeGenerator:
    """Generates intermediate three-address code"""
    def __init__(self):
        self.instructions: List[TAC] = []
        self.temp_counter = 0
        self.label_counter = 0
    
    def generate_temp(self) -> str:
        """Generate a temporary variable"""
        self.temp_counter += 1
        return f"_temp{self.temp_counter}"
    
    def generate_label(self, prefix: str = "L") -> str:
        """Generate a label"""
        self.label_counter += 1
        return f"{prefix}{self.label_counter}"
    
    def emit(self, op: str, arg1: str = None, arg2: str = None, result: str = None):
        """Emit a TAC instruction"""
        self.instructions.append(TAC(op, arg1, arg2, result))
    
    def get_code(self) -> List[TAC]:
        """Get all generated code"""
        return self.instructions


class Interpreter:
    """Tree-walking interpreter for SimpleScript"""
    def __init__(self, output_callback: Callable[[str], None] = None):
        self.global_scope = {}
        self.current_scope = self.global_scope
        self.scope_stack = [self.global_scope]
        self.functions = {}
        self.output_lines = []
        self.output_callback = output_callback or self._default_output
        self.code_gen = CodeGenerator()
    
    def _default_output(self, text: str):
        """Default output handler"""
        self.output_lines.append(str(text))
    
    def get_output(self) -> str:
        """Get all output"""
        return '\n'.join(self.output_lines)
    
    def push_scope(self):
        """Create a new scope"""
        new_scope = {}
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
    
    def pop_scope(self):
        """Pop current scope"""
        self.scope_stack.pop()
        self.current_scope = self.scope_stack[-1]
    
    def get_variable(self, name: str) -> Any:
        """Get variable value, searching up scope stack"""
        for scope in reversed(self.scope_stack):
            if name in scope:
                return scope[name]
        raise RuntimeError(f"Undefined variable '{name}'")
    
    def set_variable(self, name: str, value: Any):
        """Set variable value in current or parent scope"""
        # If variable exists in any parent scope, update it there
        for scope in reversed(self.scope_stack):
            if name in scope:
                scope[name] = value
                return
        # Otherwise set in current scope
        self.current_scope[name] = value
    
    def interpret(self, program: Program) -> str:
        """Interpret the entire program"""
        try:
            for statement in program.statements:
                self.visit_statement(statement)
        except Exception as e:
            if not isinstance(e, (BreakException, ContinueException, ReturnException)):
                raise RuntimeError(str(e))
        
        return self.get_output()
    
    # Statement visitors
    def visit_statement(self, stmt: Statement):
        """Visit a statement"""
        if isinstance(stmt, VarDecl):
            self.visit_var_decl(stmt)
        elif isinstance(stmt, FuncDecl):
            self.visit_func_decl(stmt)
        elif isinstance(stmt, ExprStmt):
            self.visit_expr_stmt(stmt)
        elif isinstance(stmt, IfStmt):
            self.visit_if_stmt(stmt)
        elif isinstance(stmt, WhileStmt):
            self.visit_while_stmt(stmt)
        elif isinstance(stmt, ForStmt):
            self.visit_for_stmt(stmt)
        elif isinstance(stmt, Block):
            self.visit_block(stmt)
        elif isinstance(stmt, ReturnStmt):
            self.visit_return_stmt(stmt)
        elif isinstance(stmt, PrintStmt):
            self.visit_print_stmt(stmt)
        elif isinstance(stmt, InputStmt):
            self.visit_input_stmt(stmt)
        elif isinstance(stmt, BreakStmt):
            raise BreakException()
        elif isinstance(stmt, ContinueStmt):
            raise ContinueException()
        else:
            raise RuntimeError(f"Unknown statement type: {type(stmt)}")
    
    def visit_var_decl(self, decl: VarDecl):
        """Visit variable declaration"""
        value = None
        if decl.initializer:
            value = self.visit_expression(decl.initializer)
        self.current_scope[decl.name] = value
    
    def visit_func_decl(self, decl: FuncDecl):
        """Visit function declaration"""
        self.functions[decl.name] = decl
    
    def visit_expr_stmt(self, stmt: ExprStmt):
        """Visit expression statement"""
        self.visit_expression(stmt.expression)
    
    def visit_if_stmt(self, stmt: IfStmt):
        """Visit if statement"""
        condition = self.visit_expression(stmt.condition)
        if self.is_truthy(condition):
            self.visit_statement(stmt.then_branch)
        elif stmt.else_branch:
            self.visit_statement(stmt.else_branch)
    
    def visit_while_stmt(self, stmt: WhileStmt):
        """Visit while statement"""
        while self.is_truthy(self.visit_expression(stmt.condition)):
            try:
                self.visit_statement(stmt.body)
            except ContinueException:
                continue
            except BreakException:
                break
    
    def visit_for_stmt(self, stmt: ForStmt):
        """Visit for statement"""
        self.push_scope()
        
        if stmt.initializer:
            self.visit_statement(stmt.initializer)
        
        while stmt.condition is None or self.is_truthy(self.visit_expression(stmt.condition)):
            try:
                self.visit_statement(stmt.body)
            except ContinueException:
                pass
            except BreakException:
                break
            
            if stmt.increment:
                self.visit_expression(stmt.increment)
        
        self.pop_scope()
    
    def visit_block(self, stmt: Block):
        """Visit block statement"""
        self.push_scope()
        for s in stmt.statements:
            self.visit_statement(s)
        self.pop_scope()
    
    def visit_return_stmt(self, stmt: ReturnStmt):
        """Visit return statement"""
        value = None
        if stmt.value:
            value = self.visit_expression(stmt.value)
        raise ReturnException(value)
    
    def visit_print_stmt(self, stmt: PrintStmt):
        """Visit print statement"""
        output = ""
        for arg in stmt.arguments:
            value = self.visit_expression(arg)
            output += str(value)
        self.output_callback(output)
    
    def visit_input_stmt(self, stmt: InputStmt):
        """Visit input statement"""
        self.output_callback(f"Input requested for '{stmt.variable}' - not supported in web mode")
        self.set_variable(stmt.variable, "")
    
    # Expression visitors
    def visit_expression(self, expr: Expression) -> Any:
        """Visit expression and return value"""
        if isinstance(expr, Literal):
            return expr.value
        
        elif isinstance(expr, Identifier):
            return self.get_variable(expr.name)
        
        elif isinstance(expr, Binary):
            left = self.visit_expression(expr.left)
            right = self.visit_expression(expr.right)
            
            if expr.operator == '+':
                return left + right
            elif expr.operator == '-':
                return left - right
            elif expr.operator == '*':
                return left * right
            elif expr.operator == '/':
                if isinstance(left, int) and isinstance(right, int):
                    return left // right  # Integer division
                return left / right
            elif expr.operator == '%':
                return left % right
            elif expr.operator == '<':
                return left < right
            elif expr.operator == '>':
                return left > right
            elif expr.operator == '<=':
                return left <= right
            elif expr.operator == '>=':
                return left >= right
            elif expr.operator == '==':
                return left == right
            elif expr.operator == '!=':
                return left != right
            elif expr.operator == 'and':
                return self.is_truthy(left) and self.is_truthy(right)
            elif expr.operator == 'or':
                return self.is_truthy(left) or self.is_truthy(right)
            else:
                raise RuntimeError(f"Unknown operator: {expr.operator}")
        
        elif isinstance(expr, Unary):
            operand = self.visit_expression(expr.operand)
            
            if expr.operator == '-':
                return -operand
            elif expr.operator == 'not':
                return not self.is_truthy(operand)
            else:
                raise RuntimeError(f"Unknown unary operator: {expr.operator}")
        
        elif isinstance(expr, Assignment):
            value = self.visit_expression(expr.value)
            self.set_variable(expr.target, value)
            return value
        
        elif isinstance(expr, Call):
            if isinstance(expr.function, Identifier):
                func_name = expr.function.name
                
                if func_name not in self.functions:
                    raise RuntimeError(f"Undefined function '{func_name}'")
                
                func_decl = self.functions[func_name]
                
                # Evaluate arguments
                args = [self.visit_expression(arg) for arg in expr.arguments]
                
                # Create new scope for function
                self.push_scope()
                
                # Bind parameters
                for i, param in enumerate(func_decl.params):
                    self.current_scope[param] = args[i] if i < len(args) else None
                
                # Execute function body
                return_value = None
                try:
                    for stmt in func_decl.body:
                        self.visit_statement(stmt)
                except ReturnException as e:
                    return_value = e.value
                
                self.pop_scope()
                return return_value
            else:
                raise RuntimeError("Cannot call non-identifier expressions")
        
        else:
            raise RuntimeError(f"Unknown expression type: {type(expr)}")
    
    def is_truthy(self, value: Any) -> bool:
        """Convert value to boolean"""
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)):
            return value != 0
        if isinstance(value, str):
            return value != ""
        return value is not None
