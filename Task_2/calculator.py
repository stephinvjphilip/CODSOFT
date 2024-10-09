import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Simple Calculator")
        master.configure(bg='black')

        self.entry = tk.Text(master, font=("Arial", 24), bd=12, width=20, height=1,
                             bg='black', fg='white', insertbackground='white')
        self.entry.grid(row=0, column=0, columnspan=4)
        self.entry.tag_configure("orange", foreground="orange")

        button_texts = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]

        row_val = 1
        col_val = 0

        for text in button_texts:
            button_color = 'orange' if text in '+-*/=' else 'white'

            button = tk.Button(master, text=text, padx=20, pady=20, font=("Arial", 16),
                               command=lambda t=text: self.on_button_click(t),
                               bg='gray20', fg=button_color)
            button.grid(row=row_val, column=col_val)

            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        master.bind('<Key>', self.on_key_press)

    def on_button_click(self, char):
        if char == '=':
            self.calculate()
        elif char == 'C':
            self.entry.delete('1.0', tk.END)
            self.entry.config(fg='white')
        else:
            current_text = self.entry.get('1.0', tk.END).strip()
            
            if char in '+-*/=':
                self.entry.insert(tk.END, char)
                self.entry.tag_add("orange", f"1.{len(current_text)}", f"1.{len(current_text) + 1}")
            else:
                self.entry.insert(tk.END, char)

    def on_key_press(self, event):
        key = event.char
        if key in '0123456789+-*/':
            self.on_button_click(key)
        elif key == '\r':
            self.calculate()
        elif key.lower() == 'c':
            self.on_button_click('C')

    def calculate(self):
        try:
            expression = self.entry.get('1.0', tk.END).strip()
            result = eval(expression)
            self.entry.delete('1.0', tk.END)
            self.entry.insert(tk.END, str(result))
            self.entry.config(fg='white') 
        except Exception as e:
            self.entry.delete('1.0', tk.END)
            self.entry.insert(tk.END, "Invalid Input")
            self.entry.config(fg='red') 

root = tk.Tk()
calculator_app = Calculator(root)
root.mainloop()
