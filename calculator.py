import customtkinter as ctk
import math

# Appearance settings
ctk.set_appearance_mode("dark")

class MathProCalculator(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Color Palette - Deep Cyber Theme
        self.COLORS = {
            "bg": "#0f172a", 
            "display": "#1e293b", 
            "num": "#334155",
            "op": "#f59e0b",    
            "sci": "#8b5cf6",   
            "del": "#f43f5e",   
            "equal": "#10b981"  
        }

        # Window Configuration
        self.title("Math Pro Calculator")
        self.geometry("400x600")
        self.configure(fg_color=self.COLORS["bg"])
        self.resizable(False, False)

        self.current_lang = "GR"
        
        # Translation Map for UI labels
        self.ui_map = {
            "sin": {"EN": "sin", "GR": "ημ"},
            "cos": {"EN": "cos", "GR": "συν"},
            "tan": {"EN": "tan", "GR": "εφ"},
            "sqrt": {"EN": "sqrt", "GR": "√"}
        }

        # Logic Map to translate UI symbols to Python math functions
        self.logic_map = {
            "÷": "/", "×": "*", "√": "math.sqrt", 
            "^": "**", "ημ": "math.sin", "συν": "math.cos", "εφ": "math.tan",
            "sin": "math.sin", "cos": "math.cos", "tan": "math.tan"
        }

        self.init_ui()

    def init_ui(self):
        """Initialize all UI components"""
        # Header Section: Display and Language Switch
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        self.display = ctk.CTkEntry(
            self.header_frame, font=("Helvetica", 30, "bold"), height=75, 
            corner_radius=12, justify="right", 
            fg_color=self.COLORS["display"], border_width=0
        )
        self.display.pack(fill="x")

        # Compact Language Switcher
        self.lang_btn = ctk.CTkSegmentedButton(
            self, values=["GR", "EN"], 
            command=self.toggle_language, height=25, width=80,
            selected_color=self.COLORS["sci"]
        )
        self.lang_btn.set("GR")
        self.lang_btn.pack(side="top", anchor="e", padx=25, pady=(0, 10))

        # Button Grid Container
        self.grid_container = ctk.CTkFrame(self, fg_color="transparent")
        self.grid_container.pack(pady=5, padx=15, fill="both", expand=True)

        self.layout = [
            ['sin', 'cos', 'tan', 'sqrt'],
            ['(', ')', '^', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['.', '0', 'C', 'Del'],
            ['=']
        ]

        self.button_widgets = []
        self.create_buttons()

    def create_buttons(self):
        """Render the calculator buttons based on the layout"""
        for r, row in enumerate(self.layout):
            self.grid_container.grid_rowconfigure(r, weight=1)
            for c, label in enumerate(row):
                self.grid_container.grid_columnconfigure(c, weight=1)
                
                # Get translated text or default label
                btn_text = self.ui_map[label][self.current_lang] if label in self.ui_map else label
                
                # Setup button colors and span
                col_span = 4 if label == "=" else 1
                
                if label == "=": color = self.COLORS["equal"]
                elif label in ["C", "Del"]: color = self.COLORS["del"]
                elif label in ["÷", "×", "-", "+"]: color = self.COLORS["op"]
                elif label in ["sin", "cos", "tan", "sqrt", "^"]: color = self.COLORS["sci"]
                else: color = self.COLORS["num"]

                btn = ctk.CTkButton(
                    self.grid_container, text=btn_text, width=0, height=0, 
                    corner_radius=10, fg_color=color,
                    font=("Helvetica", 16, "bold"),
                    command=lambda l=label: self.on_button_click(l)
                )
                btn.grid(row=r, column=c, columnspan=col_span, padx=4, pady=4, sticky="nsew")
                self.button_widgets.append((btn, label))

    def toggle_language(self, language):
        """Update button labels dynamically on language change"""
        self.current_lang = language
        for btn, label in self.button_widgets:
            if label in self.ui_map:
                btn.configure(text=self.ui_map[label][language])

    def on_button_click(self, label):
        """Handle button press events and calculations"""
        current_val = self.display.get()
        visual_repr = self.ui_map[label][self.current_lang] if label in self.ui_map else label

        if label == "C":
            self.display.delete(0, 'end')
        elif label == "Del":
            self.display.delete(len(current_val)-1, 'end')
        elif label == "=":
            try:
                # Replace visual operators with Python-executable math logic
                expression = current_val
                for visual, real in self.logic_map.items():
                    expression = expression.replace(visual, real)
                
                # Evaluate expression
                result = eval(expression)
                if isinstance(result, float):
                    result = round(result, 8)
                
                self.display.delete(0, 'end')
                self.display.insert(0, str(result))
            except Exception:
                self.display.delete(0, 'end')
                self.display.insert(0, "Error")
        elif label in ['sin', 'cos', 'tan', 'sqrt']:
            self.display.insert('end', visual_repr + "(")
        else:
            self.display.insert('end', visual_repr)

if __name__ == "__main__":
    app = MathProCalculator()
    app.mainloop()