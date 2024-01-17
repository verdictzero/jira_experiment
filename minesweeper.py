import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master):
        self.master = master
        master.title("💣 Minesweeper")

        self.reset_button = tk.Button(master, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=0, columnspan=4)

        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.grid(row=0, column=6, columnspan=4)

        self.score_label = tk.Label(master, text="Score: 0")
        self.score_label.grid(row=0, column=4, columnspan=2)

        self.buttons = {}
        self.mines = set()
        self.correct_flags = 0
        self.create_buttons()
        self.place_mines()

    def create_buttons(self):
        for x in range(1, 11):
            for y in range(10):
                btn = tk.Button(self.master, width=2, height=1)
                btn.bind('<Button-1>', self.left_click_wrapper(x, y))
                btn.bind('<Button-3>', self.right_click_wrapper(x, y))
                btn.grid(row=x, column=y)
                self.buttons[x, y] = btn

    def place_mines(self):
        self.mines = set(random.sample(self.buttons.keys(), 15))
        self.correct_flags = 0
        self.update_score()

    def reset(self):
        for x in range(1, 11):
            for y in range(10):
                btn = self.buttons[x, y]
                btn.config(text='', state='normal', background='SystemButtonFace')
        self.place_mines()

    def left_click_wrapper(self, x, y):
        return lambda Button: self.left_click(x, y)

    def right_click_wrapper(self, x, y):
        return lambda Button: self.right_click(x, y)

    def left_click(self, x, y):
        if (x, y) in self.mines:
            self.buttons[x, y].config(text='💥', background='red')
            self.game_over()
        else:
            count = self.count_mines(x, y)
            self.buttons[x, y].config(text=str(count), state='disabled')

    def right_click(self, x, y):
        btn = self.buttons[x, y]
        if btn['state'] == 'normal':
            btn.config(text='❔', background='orange')
            if (x, y) in self.mines:
                self.correct_flags += 1
        elif btn['text'] == '❔':
            btn.config(text='', background='SystemButtonFace')
            if (x, y) in self.mines:
                self.correct_flags -= 1
        self.update_score()

    def count_mines(self, x, y):
        count = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if (x+i, y+j) in self.mines:
                    count += 1
        return count

    def game_over(self):
        for x, y in self.mines:
            self.buttons[x, y].config(text='💥', background='red')
        for x, y in self.buttons:
            self.buttons[x, y].config(state='disabled')

    def update_score(self):
        self.score_label.config(text=f"Score: {self.correct_flags}")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
