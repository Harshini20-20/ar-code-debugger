import ast

def check_syntax(code_lines):
    code = "\n".join(code_lines)

    try:
        ast.parse(code)
        return "No syntax errors detected"
    except SyntaxError as e:
        return f"Syntax error on line {e.lineno}: {e.msg}"