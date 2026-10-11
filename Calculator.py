```python
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class CalcporApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calcpor Calculator")
        self.root.geometry("420x620")
        self.root.minsize(380, 560)
        
        # Configure theme and colors (Google Calculator dark/light modern style)
        self.is_dark_mode = True
        self.setup_themes()
        
        # State variables
        self.current_expression = "0"
        self.last_result = ""
        self.history_list = []
        self.memory_value = 0.0
        self.is_new_calculation = False

        self.create_widgets()
        self.apply_theme()

    def setup_themes(self):
        self.themes = {
            "dark": {
                "bg": "#202124",
                "display_bg": "#202124",
                "display_fg": "#e8eaed",
                "sub_display_fg": "#9aa0a6",
                "btn_num_bg": "#3c4043",
                "btn_num_fg": "#e8eaed",
                "btn_op_bg": "#8ab4f8",
                "btn_op_fg": "#202124",
                "btn_func_bg": "#292a2d",
                "btn_func_fg": "#8ab4f8",
                "sidebar_bg": "#292a2d",
                "sidebar_fg": "#bdc1c6",
                "hover_num": "#5f6368",
                "hover_op": "#aecbfa",
                "hover_func": "#3c4043"
            },
            "light": {
                "bg": "#f8f9fa",
                "display_bg": "#f8f9fa",
                "display_fg": "#202124",
                "sub_display_fg": "#5f6368",
                "btn_num_bg": "#ffffff",
                "btn_num_fg": "#202124",
                "btn_op_bg": "#1a73e8",
                "btn_op_fg": "#ffffff",
                "btn_func_bg": "#f1f3f4",
                "btn_func_fg": "#1a73e8",
                "sidebar_bg": "#f1f3f4",
                "sidebar_fg": "#3c4043",
                "hover_num": "#f1f3f4",
                "hover_op": "#1557b0",
                "hover_func": "#e8eaed"
            }
        }

    def create_widgets(self):
        self.main_container = tk.Frame(self.root)
        self.main_container.pack(fill=tk.BOTH, expand=True)

        # Calculator Section (Left/Main area)
        self.calc_frame = tk.Frame(self.main_container)
        self.calc_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # History Sidebar (Hidden by default, toggleable)
        self.sidebar_frame = tk.Frame(self.main_container, width=220)
        
        # Top bar for theme toggle & history toggle
        self.top_bar = tk.Frame(self.calc_frame)
        self.top_bar.pack(fill=tk.X, padx=12, pady=8)

        self.theme_btn = tk.Button(self.top_bar, text="🌙", font=("Arial", 12), bd=0, relief=tk.FLAT, command=self.toggle_theme)
        self.theme_btn.pack(side=tk.LEFT)

        self.title_label = tk.Label(self.top_bar, text="Calcpor", font=("Google Sans", 12, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=10)

        self.history_toggle_btn = tk.Button(self.top_bar, text="🕒", font=("Arial", 12), bd=0, relief=tk.FLAT, command=self.toggle_sidebar)
        self.history_toggle_btn.pack(side=tk.RIGHT)

        # Display screen
        self.display_frame = tk.Frame(self.calc_frame)
        self.display_frame.pack(fill=tk.X, padx=16, pady=10)

        self.sub_display = tk.Label(self.display_frame, text="", font=("Google Sans", 14), anchor="e", justify=tk.RIGHT)
        self.sub_display.pack(fill=tk.X)

        self.main_display = tk.Label(self.display_frame, text="0", font=("Google Sans", 36, "bold"), anchor="e", justify=tk.RIGHT)
        self.main_display.pack(fill=tk.X)

        # Keypad Grid Frame
        self.keypad_frame = tk.Frame(self.calc_frame)
        self.keypad_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configure grid weights for responsive scaling
        for i in range(6):
            self.keypad_frame.rowconfigure(i, weight=1)
        for j in range(4):
            self.keypad_frame.columnconfigure(j, weight=1)

        # Button definitions (Text, row, col, type)
        buttons = [
            ("AC", 0, 0, "func"), ("(", 0, 1, "func"), (")", 0, 2, "func"), ("÷", 0, 3, "op"),
            ("7", 1, 0, "num"), ("8", 1, 1, "num"), ("9", 1, 2, "num"), ("×", 1, 3, "op"),
            ("4", 2, 0, "num"), ("5", 2, 1, "num"), ("6", 2, 2, "num"), ("−", 2, 3, "op"),
            ("1", 3, 0, "num"), ("2", 3, 1, "num"), ("3", 3, 2, "num"), ("+", 3, 3, "op"),
            ("0", 4, 0, "num"), (".", 4, 1, "num"), ("⌫", 4, 2, "func"), ("=", 4, 3, "op"),
            ("sin", 5, 0, "func"), ("cos", 5, 1, "func"), ("tan", 5, 2, "func"), ("√", 5, 3, "func")
        ]

        self.buttons_dict = {}
        for (text, row, col, btype) in buttons:
            btn = tk.Button(
                self.keypad_frame, 
                text=text, 
                font=("Google Sans", 16), 
                bd=0, 
                relief=tk.FLAT,
                command=lambda t=text: self.on_button_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)
            self.buttons_dict[text] = (btn, btype)

        # History Sidebar Widgets
        self.sidebar_header = tk.Label(self.sidebar_frame, text="History", font=("Google Sans", 12, "bold"))
        self.sidebar_header.pack(fill=tk.X, padx=10, pady=10)

        self.history_listbox_frame = tk.Frame(self.sidebar_frame)
        self.history_listbox_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.history_scrollbar = tk.Scrollbar(self.history_listbox_frame)
        self.history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_listbox = tk.Listbox(
            self.history_listbox_frame, 
            font=("Google Sans", 11), 
            bd=0, 
            yscrollcommand=self.history_scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.history_scrollbar.config(command=self.history_listbox.yview)
        self.history_listbox.bind("<<ListboxSelect>>", self.on_history_select)

        self.clear_history_btn = tk.Button(
            self.sidebar_frame, 
            text="Clear History", 
            font=("Google Sans", 10), 
            command=self.clear_history,
            bd=0,
            relief=tk.FLAT
        )
        self.clear_history_btn.pack(fill=tk.X, padx=10, pady=10)

        # Track sidebar visibility
        self.sidebar_visible = False

    def apply_theme(self):
        theme = self.themes["dark" if self.is_dark_mode else "light"]
        
        self.root.config(bg=theme["bg"])
        self.main_container.config(bg=theme["bg"])
        self.calc_frame.config(bg=theme["bg"])
        self.top_bar.config(bg=theme["bg"])
        self.theme_btn.config(bg=theme["bg"], fg=theme["display_fg"])
        self.title_label.config(bg=theme["bg"], fg=theme["display_fg"])
        self.history_toggle_btn.config(bg=theme["bg"], fg=theme["display_fg"])
        
        self.display_frame.config(bg=theme["display_bg"])
        self.sub_display.config(bg=theme["display_bg"], fg=theme["sub_display_fg"])
        self.main_display.config(bg=theme["display_bg"], fg=theme["display_fg"])
        
        self.keypad_frame.config(bg=theme["bg"])

        # Sidebar styling
        self.sidebar_frame.config(bg=theme["sidebar_bg"])
        self.sidebar_header.config(bg=theme["sidebar_bg"], fg=theme["sidebar_fg"])
        self.history_listbox_frame.config(bg=theme["sidebar_bg"])
        self.history_listbox.config(
            bg=theme["sidebar_bg"], 
            fg=theme["sidebar_fg"], 
            selectbackground=theme["btn_op_bg"],
            selectforeground=theme["btn_op_fg"]
        )
        self.clear_history_btn.config(bg=theme["btn_func_bg"], fg=theme["btn_func_fg"])

        # Button styling
        for text, (btn, btype) in self.buttons_dict.items():
            if btype == "num":
                btn.config(bg=theme["btn_num_bg"], fg=theme["btn_num_fg"])
            elif btype == "op":
                btn.config(bg=theme["btn_op_bg"], fg=theme["btn_op_fg"])
            elif btype == "func":
                btn.config(bg=theme["btn_func_bg"], fg=theme["btn_func_fg"])

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.theme_btn.config(text="☀️" if self.is_dark_mode else "🌙")
        self.apply_theme()

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y)
            self.sidebar_visible = True

    def on_button_click(self, char):
        if char == "AC":
            self.current_expression = "0"
            self.sub_display.config(text="")
            self.is_new_calculation = False
        elif char == "⌫":
            if self.is_new_calculation:
                self.current_expression = "0"
                self.is_new_calculation = False
            elif len(self.current_expression) > 1:
                self.current_expression = self.current_expression[:-1]
            else:
                self.current_expression = "0"
        elif char == "=":
            self.calculate_result()
            return
        elif char in ["sin", "cos", "tan", "√"]:
            self.apply_advanced_function(char)
            return
        else:
            if self.is_new_calculation:
                if char in "0123456789.":
                    self.current_expression = char
                else:
                    self.current_expression = self.last_result + char
                self.is_new_calculation = False
            else:
                if self.current_expression == "0" and char not in ".+-×÷":
                    self.current_expression = char
                else:
                    # Prevent multiple consecutive operators if needed
                    self.current_expression += char

        self.main_display.config(text=self.current_expression)

    def apply_advanced_function(self, func):
        try:
            import math
            # Clean string for evaluation
            eval_str = self.current_expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            val = eval(eval_str)
            
            if func == "sin":
                res = math.sin(math.radians(val))
                expr = f"sin({val}°)"
            elif func == "cos":
                res = math.cos(math.radians(val))
                expr = f"cos({val}°)"
            elif func == "tan":
                res = math.tan(math.radians(val))
                expr = f"tan({val}°)"
            elif func == "√":
                if val < 0:
                    raise ValueError("Imaginary number")
                res = math.sqrt(val)
                expr = f"√({val})"

            res_str = str(int(res)) if res.is_integer() else f"{res:.6f}".rstrip("0").rstrip(".")
            self.sub_display.config(text=expr)
            self.main_display.config(text=res_str)
            
            # Add to history
            timestamp = datetime.datetime.now().strftime("%H:%M")
            history_item = f"{expr} = {res_str}"
            self.history_list.append(history_item)
            self.history_listbox.insert(tk.END, history_item)
            
            self.current_expression = res_str
            self.last_result = res_str
            self.is_new_calculation = True
        except Exception as e:
            self.main_display.config(text="Error")
            self.current_expression = "0"
            self.is_new_calculation = True

    def calculate_result(self):
        try:
            expr_to_eval = self.current_expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            
            # Evaluate expression
            result = eval(expr_to_eval)
            
            # Format result
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            result_str = str(result)
            
            # Update sub-display and main display
            self.sub_display.config(text=self.current_expression + " =")
            self.main_display.config(text=result_str)
            
            # Add to history list
            history_entry = f"{self.current_expression} = {result_str}"
            self.history_list.append(history_entry)
            self.history_listbox.insert(tk.END, history_entry)
            
            # Save state
            self.last_result = result_str
            self.current_expression = result_str
            self.is_new_calculation = True
            
        except ZeroDivisionError:
            self.sub_display.config(text=self.current_expression)
            self.main_display.config(text="Cannot divide by zero")
            self.current_expression = "0"
            self.is_new_calculation = True
        except Exception:
            self.sub_display.config(text=self.current_expression)
            self.main_display.config(text="Format Error")
            self.current_expression = "0"
            self.is_new_calculation = True

    def on_history_select(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            selected_item = self.history_listbox.get(index)
            # Extract result part after '='
            parts = selected_item.split("=")
            if len(parts) == 2:
                expr_part = parts[0].strip()
                res_part = parts[1].strip()
                self.sub_display.config(text=expr_part)
                self.main_display.config(text=res_part)
                self.current_expression = res_part
                self.is_new_calculation = True

    def clear_history(self):
        self.history_list.clear()
        self.history_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalcporApp(root)
    root.mainloop()
```
