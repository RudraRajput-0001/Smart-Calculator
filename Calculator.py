
import tkinter as tk
import math
import ast
import operator

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Smart Calculator")
root.geometry("400x600")
root.resizable(False, False)
root.configure(bg="#171923")

# ---------------- DISPLAY ----------------

display = tk.Entry(
    root,
    font=("Arial", 26),
    bg="#252a3a",
    fg="white",
    insertbackground="white",
    justify="right",
    bd=0
)

display.pack(fill="x", padx=15, pady=20, ipady=20)


# ---------------- SAFE CALCULATION ----------------

operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos
}


def safe_eval(expression):
    tree = ast.parse(expression, mode="eval")

    def evaluate(node):

        if isinstance(node, ast.Expression):
            return evaluate(node.body)

        if isinstance(node, ast.Constant):
            if type(node.value) not in (int, float):
                raise ValueError("Invalid input")
            return node.value

        if isinstance(node, ast.BinOp):
            op = operators.get(type(node.op))

            if op is None:
                raise ValueError("Invalid operator")

            left = evaluate(node.left)
            right = evaluate(node.right)

            return op(left, right)

        if isinstance(node, ast.UnaryOp):
            op = operators.get(type(node.op))

            if op is None:
                raise ValueError("Invalid operator")

            return op(evaluate(node.operand))

        raise ValueError("Invalid expression")

    result = evaluate(tree)

    if isinstance(result, complex) or not math.isfinite(result):
        raise ValueError("Invalid result")

    return result


# ---------------- FUNCTIONS ----------------

def press(value):
    display.insert(tk.END, value)


def clear():
    display.delete(0, tk.END)


def delete():
    current = display.get()
    display.delete(0, tk.END)
    display.insert(0, current[:-1])


def calculate():
    try:
        expression = display.get()

        if not expression:
            return

        result = safe_eval(expression)

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


def square():
    try:
        value = float(display.get())
        result = value ** 2

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


def square_root():
    try:
        value = float(display.get())
        result = math.sqrt(value)

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


def percentage():
    try:
        value = float(display.get())
        result = value / 100

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


def scientific(function):
    try:
        value = float(display.get())

        if function == "sin":
            result = math.sin(math.radians(value))
        elif function == "cos":
            result = math.cos(math.radians(value))
        elif function == "tan":
            result = math.tan(math.radians(value))

        display.delete(0, tk.END)
        display.insert(0, str(result))

    except Exception:
        display.delete(0, tk.END)
        display.insert(0, "Error")


# ---------------- BUTTON LAYOUT ----------------

buttons = [
    ["C", "DEL", "%", "/"],
    ["7", "8", "9", "*"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["√", "0", ".", "="],
    ["x²", "sin", "cos", "tan"]
]

frame = tk.Frame(root, bg="#171923")
frame.pack(expand=True, fill="both", padx=10, pady=10)

for i, row in enumerate(buttons):

    for j, char in enumerate(row):

        if char == "C":
            command = clear

        elif char == "DEL":
            command = delete

        elif char == "=":
            command = calculate

        elif char == "√":
            command = square_root

        elif char == "x²":
            command = square

        elif char == "%":
            command = percentage

        elif char in ["sin", "cos", "tan"]:
            command = lambda x=char: scientific(x)

        else:
            command = lambda x=char: press(x)

        color = "#ff9800" if char in [
            "/", "*", "-", "+", "="
        ] else "#30364a"

        if char in ["C", "DEL"]:
            color = "#d84343"

        button = tk.Button(
            frame,
            text=char,
            font=("Arial", 16, "bold"),
            bg=color,
            fg="white",
            activebackground="#555b70",
            activeforeground="white",
            bd=0,
            command=command
        )

        button.grid(
            row=i,
            column=j,
            padx=5,
            pady=5,
            sticky="nsew"
        )

# Equal button sizes

for i in range(6):
    frame.grid_rowconfigure(i, weight=1)

for j in range(4):
    frame.grid_columnconfigure(j, weight=1)


# ---------------- KEYBOARD SUPPORT ----------------

def keyboard_enter(event):
    calculate()

def keyboard_clear(event):
    clear()

root.bind("<Return>", keyboard_enter)
root.bind("<Escape>", keyboard_clear)

# ---------------- RUN APPLICATION ----------------

root.mainloop()
