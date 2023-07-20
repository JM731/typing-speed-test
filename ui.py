import tkinter as tk
import tkinter.ttk as ttk
from words import Words
import string

FONT = ("Arial", 20)
SAMPLE_FONT = ("Arial", 16)
FIRST_WORD_FONT = ("Arial", 25, 'bold')
RESULTS_LABEL_FONT = ("Arial", 30)
RESULTS_FONT = ("Arial", 25)
TEXT_ENTRY_FONT = ("Arial", 16)

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 380


class ProgramInterface:
    def __init__(self, words: Words):
        # Main Window
        self.root = tk.Tk()
        self.root.title("Typing Speed Test")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.config(pady=25, padx=50)
        self.root.resizable(False, False)
        self.root.grid_propagate(False)

        # Widgets
        self.timer_label = tk.Label(text="60s", font=FONT)
        self.type_here_label = tk.Label(text="Type here", font=FONT)
        style = ttk.Style()
        style.configure("TEntry", padding=5)
        self.typing_input = ttk.Entry(width=20, justify='center', font=("Arial", 16))
        self.restart_button = ttk.Button(text="Restart", command=self.restart)
        self.final_results_label = tk.Label(text="Results", font=RESULTS_LABEL_FONT)
        self.raw_cpm_label = tk.Label(text="", font=RESULTS_FONT)
        self.cpm_label = tk.Label(text="", font=RESULTS_FONT)
        self.wpm_label = tk.Label(text="", font=RESULTS_FONT)
        self.displayed_words_labels = [tk.Label(text="", font=SAMPLE_FONT) for _ in range(15)]
        # The current word the user should type will be displayed below the text input field (typing_input)
        # and each character will be colored separately, therefore a label for each letter will be needed. Since the
        # word is random, the labels will be generated and destroyed as needed.
        self.current_word_frame = tk.Frame()
        self.current_word_labels = []

        self.timer = None

        self.words = words

        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1)

        self.initial_screen()

        self.root.mainloop()

    def start_timer(self, event):
        key = event.char
        # This filters which keys are recognized, just symbols and space are needed as inputs
        if key in string.printable and key != "\r" and len(key) == 1:
            self.user_input(event)
            # Once the timer starts, we change the key press binding to the method user_input (see description on
            # its functionality below)
            self.root.bind("<Key>", self.user_input)
            self.root.bind("<KeyRelease>", self.spacebar_release)
            self.countdown(60)

    def countdown(self, count):
        self.timer_label.config(text=f"{count}s")
        if count > 0:
            self.timer = self.root.after(1000, self.countdown, count - 1)
        else:
            # Once the timer runs out, the finish_screen method is called, displaying the user result
            self.finish_screen()

    # This method will be called when a key is pressed, but the if statement will filter for symbols only
    # (except backspace, "\x08"),  ignoring when the spacebar is pressed (it will be dealt by a different method)
    def user_input(self, event):
        key = event.char
        if key in string.printable and key != "\r" and len(key) == 1 and event.keysym != "space" or key == "\x08":
            self.delete_current_word_labels()
            self.display_current_word()

    # This method will be triggered when the spacebar key is released, releasing over just pressing it is preferred
    # because otherwise the user can press and hold and submit many empty strings very quickly. It doesn't change the
    # program's functionality in any way, just avoids spamming empty strings too fast.
    def spacebar_release(self, event):
        if event.keysym == "space":
            # Adds the user input to the word dictionary for storage and future comparison
            self.words.add_word_dict(self.typing_input.get())
            self.typing_input.delete(0, tk.END)
            self.delete_current_word_labels()
            self.display_current_word()
            self.display_current_word_list()

    # This method will be called whenever the current word displayed below the input field needs to be updated
    # or removed.
    def delete_current_word_labels(self):
        self.current_word_labels.clear()
        for label in self.current_word_frame.winfo_children():
            label.destroy()

    # This method returns a list containing the colors ("green", "red" or "black") that each character in the current
    # word should be displayed as. Green if the user input character matches the current word's, red if it doesn't,
    # black if there is none. So, if the current word is 'glass', for example, and the user typed 'glss', 'g', 'l'
    # and the first 's' will be displayed as green, 'a' as red and the final 's' as black.
    def current_word_char_color(self):
        user_input_word = self.typing_input.get()
        current_word = self.words.get_current_word()
        # All characters will be displayed as red in case the user types more characters than the current word
        # actually has
        if len(user_input_word) > len(current_word):
            return ["red" for _ in range(len(current_word))]
        return ["black" if i > len(user_input_word) - 1 else "green" if user_input_word[i] == current_word[i]
                else "red" for i in range(len(current_word))]

    # This method will return the color a word will be displayed as in the word sample list; blue if the user typed
    # the word correctly, red otherwise, black if the word still needs to be typed.
    def word_list_color(self, word):
        if word not in self.words.word_dict:
            return "black"
        elif word == self.words.word_dict[word]:
            return "blue"
        return "red"

    # This method will be called whenever the current word needs to be displayed or updated.
    def display_current_word(self):
        current_word = self.words.get_current_word()
        current_word_char_colors = self.current_word_char_color()
        for i, char in enumerate(current_word):
            self.current_word_labels.append(tk.Label(self.current_word_frame,
                                                     text=char,
                                                     font=FIRST_WORD_FONT,
                                                     fg=current_word_char_colors[i]))
        for i, label in enumerate(self.current_word_labels):
            label.grid(row=0, column=i, sticky='nsew')

    # This method will be called whenever the current sample word list needs to be displayed or updated.
    def display_current_word_list(self):
        # A total of 15 sample words will be displayed simultaneously
        word_list = self.words.get_current_word_list()
        for i in range(15):
            self.displayed_words_labels[i].config(text=word_list[i], fg=self.word_list_color(word_list[i]))

    def initial_screen(self):
        # Populating with widgets
        self.restart_button.grid(row=0, column=0, columnspan=5, pady=(0, 5))
        self.timer_label.grid(row=1, column=0, columnspan=5, sticky="NSEW")
        self.type_here_label.grid(row=2, column=0, columnspan=5, sticky="NSEW")
        self.typing_input.grid(row=3, column=0, columnspan=5, pady=5)
        self.current_word_frame.grid(row=4, column=0, columnspan=5, pady=(5, 10))
        col = 0
        row = 5
        for label in self.displayed_words_labels:
            label.grid(row=row, column=col, sticky="nsew", padx=8)
            self.root.update()
            if col == 4:
                col = 0
                row += 1
            else:
                col += 1

        # Key Bindings
        self.root.bind("<Key>", self.start_timer)

        self.typing_input.focus_set()

        self.display_current_word()
        self.display_current_word_list()

        self.restart_button.config(state=tk.NORMAL)

    def finish_screen(self):
        # Key bindings are removed since they are not necessary in this screen
        self.root.unbind("<Key>")
        self.root.unbind("<KeyRelease>")

        # Removing the initial_screen widgets
        self.timer_label.grid_forget()
        self.typing_input.grid_forget()
        self.current_word_frame.grid_forget()
        for label in self.displayed_words_labels:
            label.config(text='')
            label.grid_forget()

        # Populating with relevant widgets
        self.final_results_label.grid(row=1, column=0, columnspan=5, pady=(10, 10))
        self.raw_cpm_label.config(text=f"Raw CPM: {self.words.get_raw_char_num()}")
        self.raw_cpm_label.grid(row=2, column=0, columnspan=5)
        corrected_cpm = self.words.get_correct_char_num()
        self.cpm_label.config(text=f"Corrected CPM: {corrected_cpm}")
        self.cpm_label.grid(row=3, column=0, columnspan=5)
        self.wpm_label.config(text=f"WPM: {round(corrected_cpm/5)}")
        self.wpm_label.grid(row=4, column=0, columnspan=5)

    def restart(self):
        self.restart_button.config(state=tk.DISABLED)
        self.root.unbind("<KeyRelease>")
        self.root.unbind("<Key>")
        self.delete_current_word_labels()
        self.remove_finish_labels()
        if self.timer is not None:
            self.root.after_cancel(self.timer)
            self.timer = None
        self.timer_label.config(text="60s")
        self.typing_input.delete(0, tk.END)
        self.words.start()
        self.initial_screen()

    def remove_finish_labels(self):
        self.final_results_label.grid_forget()
        self.raw_cpm_label.grid_forget()
        self.cpm_label.grid_forget()
        self.wpm_label.grid_forget()
