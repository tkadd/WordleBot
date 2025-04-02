import customtkinter as ctk
from wordle_bot import WordleBot

class WordleGUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Wordle Bot")
        self.geometry("565x455")
        ctk.set_appearance_mode('light')

        self.iconbitmap('wordle/wordlebot_icon.ico')

        self.resizable(False, False)

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

        # Construct colour buttons:
        self.colours = {'grey': '#787C7E',
                        'yellow': '#C9B458',
                        'green': '#6AAA64'}
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
                                     fg_color=self.colours['green'],
                                     hover_color='#538A50',
                                     command=lambda: self.set_colour(self.colours['green']))
        green_button.grid(row=0, column=0, padx=3, pady=2)

        yellow_button = ctk.CTkButton(colour_buttons_frame,
                                      **button_style1,
                                      fg_color=self.colours['yellow'],
                                      hover_color='#A8923F',
                                      command=lambda: self.set_colour(self.colours['yellow']))
        yellow_button.grid(row=0, column=1, padx=3, pady=2)

        grey_button = ctk.CTkButton(colour_buttons_frame,
                                    **button_style1,
                                    fg_color=self.colours['grey'],
                                    hover_color='#5F6365',
                                    command=lambda: self.set_colour(self.colours['grey']))
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
        button_style2 = {'font': ('Clear Sans', 20, 'bold'),
                         'text_color': 'white',
                         'corner_radius': 5,
                         'fg_color': 'black',
                         'hover_color': '#333333',
                         'height': 30}

        undo_button = ctk.CTkButton(self,
                                    text='UNDO',
                                    **button_style2,
                                    command=self.undo)
        undo_button.grid(row=6, column=1, padx=5, pady=5)

        # Enter Button:
        enter_button = ctk.CTkButton(self,
                                     text='ENTER',
                                     **button_style2,
                                     command=self.enter)
        enter_button.grid(row=6, column=2, padx=5, pady=5)

        # Word Information List:
        self.word_frame = ctk.CTkFrame(self,
                                       fg_color='white',
                                       bg_color='transparent',
                                       border_color='black',
                                       border_width=1,
                                       corner_radius=5)
        self.word_frame.grid(row=0, rowspan=6, column=2, padx=5, pady=3, sticky='nsew')

        for i in range(10):
            self.word_frame.rowconfigure(i, weight=1)

    def construct_entries(self):
        for i in range(6):
            word_frame = ctk.CTkFrame(self, bg_color='white', fg_color='white')
            word_frame.grid(row=i, column=0, columnspan=2, sticky='nsew')

            for j in range(6):
                word_frame.columnconfigure(j, weight=1)
            
            word = []
            for j in range(5):
                entry = ctk.CTkEntry(word_frame,
                                     font=("Clear Sans", 35, 'bold'),
                                     text_color='black',
                                     justify="center",
                                     height=60,
                                     width=60,
                                     corner_radius=0,
                                     fg_color='white',
                                     border_color='#D3D6DA')
                entry.grid(row=0, column=j, padx=2, pady=2, sticky='nsew')

                word.append(entry)
            self.word_entries.append(word)

    def set_colour(self, col):
        pass

    def undo(self):
        pass

    def enter(self):
        pass



if __name__ == "__main__":
    game = WordleGUI()
    game.mainloop()
