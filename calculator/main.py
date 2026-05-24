# calculator/main.py

import sys
import tkinter as tk
from pkg.calculator import Calculator
from pkg.render import format_json_output
from gui import CalculatorGUI  # Import the CalculatorGUI class

def main():
    calculator = Calculator()
    
    if "--gui" in sys.argv:
        root = tk.Tk()
        gui = CalculatorGUI(root)
        root.mainloop()
        return

    if len(sys.argv) <= 1:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "3 + 5"')
        print('To run the GUI: python main.py --gui') # Add GUI usage instruction
        return

    expression = " ".join(sys.argv[1:])
    try:
        result = calculator.evaluate(expression)
        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
