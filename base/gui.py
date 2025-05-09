# pip install tkinter
import tkinter as tk
import tkinter.messagebox
from tkinter.constants import SUNKEN
from tkinter import ttk
import math

# Color scheme
BG_COLOR = "#1E1E1E"
BUTTON_BG = "#2D2D2D"
BUTTON_FG = "#FFFFFF"
DISPLAY_BG = "#252526"
DISPLAY_FG = "#FFFFFF"
SPECIAL_BG = "#007ACC"
MEMORY_BG = "#4B4B4B"
HOVER_COLOR = "#3E3E3E"
HISTORY_BG = "#252526"
HISTORY_FG = "#CCCCCC"

class ModernCalculator:
	def __init__(self):
		self.window = tk.Tk()
		self.window.title('Modern Calculator By Jabir-Srj')
		self.window.configure(bg=BG_COLOR)
		self.window.resizable(False, False)
		
		# Memory storage
		self.memory = 0
		
		# History storage
		self.history = []
		
		self.setup_ui()
		
	def setup_ui(self):
		# Main container
		self.main_frame = tk.Frame(self.window, bg=BG_COLOR, padx=15, pady=15)
		self.main_frame.pack(expand=True, fill='both')
		
		# Title
		title_label = tk.Label(
			self.main_frame,
			text="Modern Calculator",
			font=("Segoe UI", 20, "bold"),
			bg=BG_COLOR,
			fg=BUTTON_FG
		)
		title_label.pack(pady=(0, 15))
		
		# History display
		self.history_frame = tk.Frame(self.main_frame, bg=HISTORY_BG, height=60)
		self.history_frame.pack(fill='x', pady=(0, 10))
		self.history_label = tk.Label(
			self.history_frame,
			text="",
			font=("Segoe UI", 10),
			bg=HISTORY_BG,
			fg=HISTORY_FG,
			anchor='e',
			justify='right'
		)
		self.history_label.pack(fill='x', padx=10, pady=5)
		
		# Main display
		self.entry = tk.Entry(
			self.main_frame,
			relief=SUNKEN,
			borderwidth=0,
			width=30,
			font=("Segoe UI", 24),
			bg=DISPLAY_BG,
			fg=DISPLAY_FG,
			justify="right"
		)
		self.entry.pack(fill='x', ipady=10, pady=(0, 15))
		
		# Buttons frame
		self.buttons_frame = tk.Frame(self.main_frame, bg=BG_COLOR)
		self.buttons_frame.pack(expand=True, fill='both')
		
		# Create buttons
		self.create_buttons()
		
		# Bind keyboard events
		self.window.bind("<Key>", self.handle_keypress)
		
	def create_button(self, text, row, col, command, width=3, columnspan=1, bg=BUTTON_BG):
		button = tk.Button(
			self.buttons_frame,
			text=text,
			font=("Segoe UI", 12, "bold"),
			width=width,
			command=command,
			bg=bg,
			fg=BUTTON_FG,
			relief=tk.FLAT,
			borderwidth=0,
			padx=15,
			pady=10
		)
		button.grid(row=row, column=col, columnspan=columnspan, padx=2, pady=2, sticky="nsew")
		
		# Add hover effect
		button.bind("<Enter>", lambda e: button.configure(bg=HOVER_COLOR))
		button.bind("<Leave>", lambda e: button.configure(bg=bg))
		
		return button
		
	def create_buttons(self):
		# Memory buttons
		self.create_button("MC", 0, 0, self.memory_clear, bg=MEMORY_BG)
		self.create_button("MR", 0, 1, self.memory_recall, bg=MEMORY_BG)
		self.create_button("M+", 0, 2, self.memory_add, bg=MEMORY_BG)
		self.create_button("M-", 0, 3, self.memory_subtract, bg=MEMORY_BG)
		
		# Parentheses and clear
		self.create_button("(", 1, 0, lambda: self.myclick("("))
		self.create_button(")", 1, 1, lambda: self.myclick(")"))
		self.create_button("⌫", 1, 2, self.backspace)
		self.create_button("C", 1, 3, self.clear)
		
		# Numbers and operations
		for i in range(1, 10):
			row = (i-1)//3 + 2
			col = (i-1)%3
			self.create_button(str(i), row, col, lambda x=i: self.myclick(x))
			
		# Zero, decimal, and operations
		self.create_button("0", 5, 0, lambda: self.myclick(0), columnspan=2)
		self.create_button(".", 5, 2, lambda: self.myclick("."))
		
		# Operations
		self.create_button("+", 6, 0, lambda: self.myclick("+"))
		self.create_button("-", 6, 1, lambda: self.myclick("-"))
		self.create_button("×", 6, 2, lambda: self.myclick("*"))
		self.create_button("÷", 6, 3, lambda: self.myclick("/"))
		
		# Additional operations
		self.create_button("±", 7, 0, self.negate)
		self.create_button("%", 7, 1, self.percentage)
		self.create_button("√", 7, 2, self.square_root)
		self.create_button("=", 7, 3, self.equal, bg=SPECIAL_BG)
		
		# Configure grid weights
		for i in range(8):
			self.buttons_frame.grid_rowconfigure(i, weight=1)
		for i in range(4):
			self.buttons_frame.grid_columnconfigure(i, weight=1)
			
	def myclick(self, number):
		self.entry.insert(tk.END, number)
		
	def clear(self):
		self.entry.delete(0, tk.END)
		
	def backspace(self):
		current = self.entry.get()
		self.entry.delete(0, tk.END)
		self.entry.insert(0, current[:-1])
		
	def equal(self):
		try:
			expression = self.entry.get()
			if '/0' in expression and not '/0.' in expression:
				raise ZeroDivisionError
			result = str(eval(expression))
			self.history.append(f"{expression} = {result}")
			self.update_history()
			self.entry.delete(0, tk.END)
			self.entry.insert(0, result)
		except ZeroDivisionError:
			tkinter.messagebox.showerror("Error", "Cannot divide by zero!")
			self.clear()
		except:
			tkinter.messagebox.showerror("Error", "Invalid Expression!")
			self.clear()
			
	def negate(self):
		try:
			current = float(self.entry.get())
			self.entry.delete(0, tk.END)
			self.entry.insert(0, str(-current))
		except:
			pass
			
	def percentage(self):
		try:
			current = float(self.entry.get())
			self.entry.delete(0, tk.END)
			self.entry.insert(0, str(current/100))
		except:
			pass
			
	def square_root(self):
		try:
			current = float(self.entry.get())
			if current < 0:
				raise ValueError
			self.entry.delete(0, tk.END)
			self.entry.insert(0, str(math.sqrt(current)))
		except:
			tkinter.messagebox.showerror("Error", "Invalid input for square root!")
			self.clear()
			
	def memory_clear(self):
		self.memory = 0
		
	def memory_recall(self):
		self.entry.delete(0, tk.END)
		self.entry.insert(0, str(self.memory))
		
	def memory_add(self):
		try:
			self.memory += float(self.entry.get())
		except:
			pass
			
	def memory_subtract(self):
		try:
			self.memory -= float(self.entry.get())
		except:
			pass
			
	def update_history(self):
		if len(self.history) > 3:
			self.history.pop(0)
		self.history_label.config(text="\n".join(self.history))
		
	def handle_keypress(self, event):
		key = event.char
		if key.isdigit() or key in "+-*/.()":
			self.myclick(key)
		elif event.keysym == "Return":
			self.equal()
		elif event.keysym == "BackSpace":
			self.backspace()
		elif event.keysym == "Escape":
			self.clear()
		
	def run(self):
		self.window.mainloop()

if __name__ == "__main__":
	calc = ModernCalculator()
	calc.run()
