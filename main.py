import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


MAX_ATTEMPTS = 6
WORD_LENGHT = 5
APP_NAME = 'wopyit'


class OnScreenKeyboard:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} - Python WORDLE Clone in Italiano")        
        
        self.attempts = 0
        self.is_finished = False
        self.current_word = ''
        self.words_list = []
        with open('dict/custom_dictionary.txt', 'r') as file:
            for line in file:
                self.words_list.append(line[:-1]) #remove newline char (\n)
        self.solution = random.choice(self.words_list)
        print(self.solution)        

        # Create 6x5 grid of text entries
        self.text_entries = []
        self.create_text_grid()

        # Create keyboard
        self.key_buttons = {}
        self.create_keyboard()
        
    def create_text_grid(self):
        # Frame to hold the text entries
        grid_frame = tk.Frame(self.root)
        grid_frame.grid(row=0, column=0, columnspan=15, padx=10, pady=10)
        
        # Create 6 rows x 5 columns of text entries
        for row in range(MAX_ATTEMPTS):
            row_entries = []
            for col in range(WORD_LENGHT):
                entry = tk.Entry(grid_frame, width=3, font=('Arial', 16), justify='center')
                entry.grid(row=row, column=col, padx=2, pady=2, ipady=5)
                entry.config(state='readonly')  # Make them read-only
                row_entries.append(entry)
            self.text_entries.append(row_entries)
    
    def create_keyboard(self):
        # Keyboard layout (QWERTY)
        keyboard_layout = [
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l'],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', 'Backspace', 'Enter']
        ]
        
        # Special key widths
        special_keys = {
            'Backspace': 2, 'Enter': 2
        }
        
        # Create buttons for each key
        for row_idx, row in enumerate(keyboard_layout, start=1):
            col_idx = 0
            for key in row:
                span = special_keys.get(key, 1)
                
                btn = ttk.Button(
                    self.root, 
                    text=key, 
                    width=6 if span == 1 else 6*span,
                    command=lambda k=key: self.key_press(k)
                )
                
                btn.grid(
                    row=row_idx+1,  # +1 because text grid is row 0
                    column=col_idx, 
                    columnspan=span,
                    padx=2, 
                    pady=2,
                    sticky='ew'
                )

                # Store the button in our dictionary
                # self.key_buttons[key] = btn
                col_idx += span
    
    def key_press(self, key):
        if self.is_finished:
            return
        if key == 'Enter':
            if len(self.current_word) == WORD_LENGHT:
                self.check_solution()
            return
        elif key == 'Backspace':
            self.handle_backspace()
            return
        else:
            if len(self.current_word) != WORD_LENGHT:
                char = key.lower()
            else:
                return
        
        if self.attempts < MAX_ATTEMPTS:
            row = self.attempts
            col = len(self.current_word) % WORD_LENGHT
            self.text_entries[row][col].config(state='normal')
            self.text_entries[row][col].delete(0, tk.END)
            self.text_entries[row][col].insert(0, char)
            self.current_word += char
        else:
            self.is_finished = True
            messagebox.showerror(f"{APP_NAME}", "Hai perso!")
    
    def handle_backspace(self):
        if len(self.current_word) > 0:
            self.current_word = self.current_word[:-1]
            row = self.attempts
            col = len(self.current_word) % WORD_LENGHT
            self.text_entries[row][col].config(state='normal')
            self.text_entries[row][col].delete(0, tk.END)

    def check_solution(self):
        # Preliminary step: the current word needs to be a real word
        if self.current_word not in self.words_list:
            messagebox.showwarning(f"{APP_NAME}", "La parola inserita non esiste nel dizionario!") 
            return

        result = []
        solution_list = list(self.solution)  # Convert to list for easier manipulation
        
        # First pass: Check for exact matches (green)
        for i in range(WORD_LENGHT):
            if self.solution[i] == self.current_word[i]:
                result.append('#00FF00')
                solution_list[i] = None  # Mark this position as used
            else:
                result.append(None)
        
        # Second pass: Check for yellow
        for i in range(WORD_LENGHT):
            if result[i] is None:  # Only process non green positions
                char = self.current_word[i]
                if char in solution_list:
                    result[i] = '#F4D03F'
                    # Find and mark the first occurrence in the list (to avoid double-counting)
                    first_occurrence = solution_list.index(char)
                    solution_list[first_occurrence] = None
                else:
                    result[i] = '#C0C0C0'

        # Third pass: Update the colors in GUI
        for i, bg_color in enumerate(result):
            self.text_entries[self.attempts][i].config(
                disabledbackground=bg_color,
                background=bg_color
            )
        #TODO FIX Keyboard colors
        # for i, letter in enumerate(self.current_word):
        #     self.key_buttons[letter].config(background=result[i])
        
        if self.solution == self.current_word:
            self.is_finished = True
            messagebox.showinfo(f"{APP_NAME}", "Hai vinto!")
        else:
            self.attempts += 1
            self.current_word = ''


if __name__ == "__main__":
    root = tk.Tk()
    app = OnScreenKeyboard(root)
    root.mainloop()
