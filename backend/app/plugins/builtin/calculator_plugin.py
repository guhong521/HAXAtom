"""
计算器插件

提供数学计算功能
"""

import ast
import operator
import re
from typing import Any, Dict

from app.plugins.base import BasePlugin, PluginMetadata, PluginResult


class CalculatorPlugin(BasePlugin):
    """
    计算器插件
    
    功能：
    - 基础数学运算（加减乘除、幂运算）
    - 支持括号优先级
    - 安全计算（限制危险操作）
    """
    
    @property
    def metadata(self) -> PluginMetadata:
        return PluginMetadata(
            name="calculator",
            description="执行数学计算，支持 + - * / ^ 运算符和括号",
            version="1.0.0",
            author="HAXAtom",
            category="calculation",
            icon="🧮",
            tags=["math", "calculation", "utility"]
        )
    
    async def execute(self, params: Dict[str, Any]) -> PluginResult:
        """
        执行计算
        
        Args:
            params: 参数
                - expression: 数学表达式，如 "1 + 2 * 3"
        
        Returns:
            PluginResult: 计算结果
        """
        try:
            expression = params.get("expression", "")
            
            if not expression:
                return PluginResult.error(
                    error="Empty expression",
                    message="请输入数学表达式"
                )
            
            # 计算结果
            result = self._safe_eval(expression)
            
            return PluginResult.ok(
                data={
                    "expression": expression,
                    "result": result,
                    "type": type(result).__name__
                },
                message=f"{expression} = {result}"
            )
            
        except Exception as e:
            return PluginResult.error(
                error=str(e),
                message=f"计算错误: {str(e)}"
            )
    
    def _safe_eval(self, expression: str) -> float:
        """
        安全计算表达式
        
        只允许数学运算，禁止函数调用等危险操作
        
        Args:
            expression: 数学表达式
            
        Returns:
            float: 计算结果
        """
        # 清理表达式
        expression = expression.strip()
        
        # 只允许数字、运算符和括号
        allowed_pattern = r'^[\d+\-*/().^\s]+$'
        if not re.match(allowed_pattern, expression):
            raise ValueError("表达式包含非法字符，只允许数字和 +-*/^()")
        
        # 替换幂运算符
        expression = expression.replace("^", "**")
        
        # 使用 AST 安全解析
        try:
            tree = ast.parse(expression, mode='eval')
        except SyntaxError:
            raise ValueError("表达式语法错误")
        
        # 安全计算
        allowed_operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.Pow: operator.pow,
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }
        
        def eval_node(node):
            if isinstance(node, ast.Num):
                return node.n
            elif isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("不支持的常量类型")
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](left, right)
                raise ValueError(f"不支持的运算符")
            elif isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                op_type = type(node.op)
                if op_type in allowed_operators:
                    return allowed_operators[op_type](operand)
                raise ValueError(f"不支持的运算符")
            elif isinstance(node, ast.Expression):
                return eval_node(node.body)
            else:
                raise ValueError(f"不支持的表达式类型: {type(node).__name__}")
        
        result = eval_node(tree)
        
        # 如果是整数，返回整数
        if isinstance(result, float) and result.is_integer():
            return int(result)
        return result
    
    def validate_params(self, params: Dict[str, Any]) -> tuple[bool, str]:
        """验证参数"""
        expression = params.get("expression", "")
        
        if not expression:
            return False, "expression参数不能为空"
        
        if len(expression) > 1000:
            return False, "表达式过长（最大1000字符）"
        
        return True, None
