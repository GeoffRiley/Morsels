import ast
import operator
import sys
from datetime import datetime, timedelta
from sys import exit, stderr


def dmath(start_date: datetime, days: int):
    forecast = start_date + timedelta(days=days)
    print(forecast.strftime('%Y-%m-%d'))


def tmath(start_date: datetime, end_date: datetime):
    difference = end_date - start_date
    print(difference.days)


def is_date(date_string: str):
    try:
        val = datetime.strptime(date_string, '%Y-%m-%d')
    except ValueError:
        return False
    return val


_operations = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
}

_unuary_operations = {
    ast.UAdd: lambda x: x,
    ast.USub: lambda x: -x,
}


def _safe_eval(node: ast.AST):
    if isinstance(node, (ast.Num, ast.Constant)):
        if not isinstance(node.n, int):
            print('Error: only integers allowed', file=stderr)
            exit(1)
        return node.n
    elif isinstance(node, ast.UnaryOp):
        op = _unuary_operations[node.op.__class__]
        return op(_safe_eval(node.operand))
    elif isinstance(node, ast.BinOp):
        try:
            op = _operations[node.op.__class__]
            left = _safe_eval(node.left)
            right = _safe_eval(node.right)
            return op(left, right)
        except KeyError as exc:
            print(f'Error: {str(exc)}', file=stderr)
    elif isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    print(f'Error: Bad operator {ast.unparse(node)}', file=stderr)
    exit(1)


def safe_eval(maths_string: str):
    try:
        node = ast.parse(maths_string, '', 'eval')
    except SyntaxError as exc:
        print(f'Error: {str(exc)}', file=stderr)
        exit(1)
    return _safe_eval(node)


def main():
    args = sys.argv[1:]
    try:
        dt_list = [is_date(arg) or safe_eval(arg) for arg in args]
    except ValueError as exc:
        print(f'Error: {str(exc)}', file=stderr)
        exit(1)

    if len(dt_list) == 1:
        dmath(datetime.today(), dt_list[0])
    elif isinstance(dt_list[1], int):
        dmath(*dt_list[:2])
    else:
        tmath(*dt_list[:2])


if __name__ == '__main__':
    main()
