import customtkinter as ctk
from wordle_bot import WordleBot

class WordleGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Wordle Bot")
        self.geometry("565x455")
        ctk.set_appearance_mode('light')

        self.iconbitmap('wordle/wordlebot_icon.ico')

        self.resizable(True, True)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.container = ctk.CTkFrame(self, corner_radius=10, fg_color='white')
        self.container.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.show_frame()

    def show_frame(self):
        frame = Wordle(parent=self.container, controller=self)
        frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        frame.tkraise()

class Wordle(ctk.CTkFrame):

    def __init__(self, parent, controller):
        super().__init__(parent, fg_color='transparent')
        self.controller = controller

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)

        # Construct wordle grid:
        self.word_entries = []
        self.construct_entries()

        self.controller.bind("<Key>", self.key_handler)

        # Construct colour buttons:
        self.colours = {'#787C7E': 'B',
                        '#C9B458': 'Y',
                        '#6AAA64': 'G'}
        colour_buttons_frame = ctk.CTkFrame(self,
                                            fg_color='white',
                                            bg_color='transparent',
                                            border_color='black',
                                            border_width=1,
                                            corner_radius=5)
        colour_buttons_frame.grid(row=6, column=0, padx=5, pady=5, sticky='nsew')

        for i in range(4):
            colour_buttons_frame.columnconfigure(i, weight=1)

        button_style1 = {'height': 40,
                        'width': 40,
                        'text': '',
                        'corner_radius': 5}

        green_button = ctk.CTkButton(colour_buttons_frame,
                                     **button_style1,
                                     fg_color='#6AAA64',
                                     hover_color='#538A50',
                                     command=lambda: self.set_colour('#6AAA64'))
        green_button.grid(row=0, column=0, padx=3, pady=2)

        yellow_button = ctk.CTkButton(colour_buttons_frame,
                                      **button_style1,
                                      fg_color='#C9B458',
                                      hover_color='#A8923F',
                                      command=lambda: self.set_colour('#C9B458'))
        yellow_button.grid(row=0, column=1, padx=3, pady=2)

        grey_button = ctk.CTkButton(colour_buttons_frame,
                                    **button_style1,
                                    fg_color='#787C7E',
                                    hover_color='#5F6365',
                                    command=lambda: self.set_colour('#787C7E'))
        grey_button.grid(row=0, column=2, padx=3, pady=2)

        back_button = ctk.CTkButton(colour_buttons_frame,
                                    font=('Arial', 15, 'bold'),
                                    text="\u232B",
                                    height=30,
                                    width=40,
                                    corner_radius=5,
                                    fg_color='black',
                                    hover_color='#333333',
                                    command=lambda: self.set_colour(None))
        back_button.grid(row=0, column=3, padx=3, pady=2)

        # Undo Button:
        button_style2 = {'font': ('Cascadia Mono', 20, 'bold'),
                         'text_color': 'white',
                         'corner_radius': 5,
                         'fg_color': 'black',
                         'hover_color': '#333333',
                         'height': 30}

        undo_button = ctk.CTkButton(self,
                                    text='UNDO',
                                    **button_style2,
                                    command=self.undo,
                                    state='disabled')
        undo_button.grid(row=6, column=1, padx=5, pady=5)

        # Enter Button:
        enter_button = ctk.CTkButton(self,
                                     text='ENTER',
                                     **button_style2,
                                     command=self.enter)
        enter_button.grid(row=6, column=2, padx=5, pady=5)

        # initialise wordlebot:
        self.game = WordleBot()

        # Word Information List:
        self.word_frame = ctk.CTkFrame(self,
                                       fg_color='white',
                                       bg_color='transparent',
                                       border_color='black',
                                       border_width=1,
                                       corner_radius=5)
        self.word_frame.grid(row=0, rowspan=6, column=2, padx=5, pady=3, sticky='nsew')

        for i in range(11):
            self.word_frame.rowconfigure(i, weight=1)

        self.update_wordlist()

        # Location information:
        self.colour_ind = 0
        self.letter_ind = 0
        self.word = 0

    def construct_entries(self):
        for i in range(6):
            word_frame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
            word_frame.grid(row=i, column=0, columnspan=2, sticky='nsew')

            for j in range(6):
                word_frame.columnconfigure(j, weight=1)
            
            word = []
            for j in range(5):
                entry = ctk.CTkEntry(word_frame,
                                     font=("Cascadia Mono", 40, 'bold'),
                                     text_color='black',
                                     justify="center",
                                     height=60,
                                     width=60,
                                     corner_radius=0,
                                     fg_color='white',
                                     border_color='#D3D6DA',
                                     state='disabled')
                entry._entry.configure(cursor="arrow")
                entry.grid(row=0, column=j, padx=2, pady=2, sticky='nsew')

                word.append(entry)
            self.word_entries.append(word)

    def key_handler(self, event):
        char = event.char.upper() # Character to be entered
        key = event.keysym # Name of key

        # ctrl+key for colour control:
        if (event.state & 0x4):
            key = key.lower()
            if key == 'g':
                self.set_colour('#6AAA64')
            elif key == 'y':
                self.set_colour('#C9B458')
            elif key == 'b':
                self.set_colour('#787C7E')
            elif key == "z":
                self.set_colour(None)

        # standard key entry:
        if key == "BackSpace":
            if self.letter_ind > 0:
                self.letter_ind -= 1
                self.set_text("")
        elif key == "Return":
            self.enter()
        elif key == "Delete":
            self.undo()
        elif char.isalpha() and len(char) == 1:
            if self.letter_ind < 5:
                self.set_text(char)
                self.letter_ind += 1

    def set_text(self, char):
        entry = self.word_entries[self.word][self.letter_ind]
        entry.configure(state="normal")
        if char == "": entry.configure(border_color='#D3D6DA')
        else: entry.configure(border_color='#8C8F91')
        entry.delete(0, "end")
        entry.insert(0, char)
        entry.configure(state="disabled")

    def set_colour(self, col):
        if col is None:
            if self.colour_ind > 0: self.colour_ind -= 1
            entry = self.word_entries[self.word][self.colour_ind]
            entry.configure(fg_color='white')
        else:
            entry = self.word_entries[self.word][self.colour_ind]
            entry.configure(fg_color=col)
            if self.colour_ind < 5: self.colour_ind += 1

    def undo(self):
        pass

    def enter(self):
        # Checking that entry has been filled in correctly:
        for i in range(5):
            entry = self.word_entries[self.word][i]
            char, col = entry.get(), entry.cget('fg_color')
            if char == '' or col == 'white':
                return None
        # Update word aesthetic and collect guess information:
        guess = ''
        result = ''
        for i in range(5):
            entry = self.word_entries[self.word][i]

            col = entry.cget('fg_color')
            guess += entry.get().lower()
            result += self.colours[col]

            entry.configure(border_color=f'{col}')
            entry.configure(text_color='white')
        # Change word:
        self.word += 1
        self.colour_ind = 0
        self.letter_ind = 0
        # Update suggestions:
        self.game.play(guess, result, update_dictionary=True, display=False)
        for widget in self.word_frame.winfo_children():
            widget.destroy()
        self.update_wordlist()

    def update_wordlist(self):
        entropy_dict = self.game.word_entropy()
        sorted_entropy = sorted(entropy_dict.items(), key=lambda item: item[1], reverse=True)

        for i in range(min(len(sorted_entropy), 10)):
            word_display = ctk.CTkLabel(self.word_frame,
                                        font=('Cascadia Mono', 20),
                                        text=f'{sorted_entropy[i][0].upper()} - {sorted_entropy[i][1]:.3f}',
                                        justify='center')
            word_display.grid(row=i, padx=22, pady=3, sticky='nsew')
        length_display = ctk.CTkLabel(self.word_frame,
                                      font=('Cascadia Mono', 20),
                                      text=f'{len(sorted_entropy)} options',
                                      justify='center')
        length_display.grid(row=10, padx=3, pady=3, sticky='nsew')

if __name__ == "__main__":
    game = WordleGUI()
    game.mainloop()
