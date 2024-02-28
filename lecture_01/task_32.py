"""ააგეთ კალკულატორი. (სტრიქონის ანალიზის საშუალებით)."""

class Calculator:
    def calculate(self, expr: str) -> int:
        expr = expr + "\0"
        value, _ = self.eval(expr, 0, [])
        return value

    def eval(self, expr, i, stack):
        operand = 0
        prev_op = "+"
        while i < len(expr):
            char = expr[i]
            if char == " ":
                pass
            elif char.isdigit():
                operand = operand * 10 + int(char)
            elif char in ("+", "-", "*", "/", ")", "\0"):
                if prev_op == "+":
                    stack.append(operand)
                elif prev_op == "-":
                    stack.append(-operand)
                elif prev_op == "*":
                    prev_operand = stack.pop()
                    stack.append(prev_operand * operand)
                elif prev_op == "/":
                    prev_operand = stack.pop()
                    stack.append(int(prev_operand / operand))

                if char in ("+", "-", "*", "/"):
                    operand = 0
                    prev_op = char
                elif char in (")", "\0"):
                    return sum(stack), i
            elif char == "(":
                operand, i = self.eval(expr, i + 1, [])
            else:
                raise ValueError("Invalid expression")

            i += 1


if __name__ == "__main__":
    expression = input("Enter expression: ")
    calculator = Calculator()
    print(calculator.calculate(expression))
