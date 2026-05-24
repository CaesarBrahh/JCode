
import tkinter as tk
from tkinter import messagebox
from pkg.calculator import Calculator

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        self.calculator = Calculator()

        self.expression_label = tk.Label(master, text="Expression:")
        self.expression_label.pack()

        self.expression_entry = tk.Entry(master, width=50)
        self.expression_entry.pack()

        self.calculate_button = tk.Button(master, text="Calculate", command=self.calculate)
        self.calculate_button.pack()

        self.result_label = tk.Label(master, text="Result:")
        self.result_label.pack()

        self.result_display = tk.Text(master, height=5, width=50, state=tk.DISABLED)
        self.result_display.pack()

    def calculate(self):
        expression = self.expression_entry.get()
        if not expression:
            messagebox.showwarning("Input Error", "Please enter an expression.")
            return

        try:
            result = self.calculator.evaluate(expression)
            self.update_result_display(f"{expression} = {result}")
        except Exception as e:
            messagebox.showerror("Calculation Error", str(e))
            self.update_result_display(f"Error: {e}")

    def update_result_display(self, text):
        self.result_display.config(state=tk.NORMAL)
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, text)
        self.result_display.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    gui = CalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
