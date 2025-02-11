from tkinter import Button, Label, W, SUNKEN
from .helpers import get_high_score, set_high_score

class CellButton(Button):
    def __init__(self, frame, hit_event, ir, ic):
        super().__init__(frame, text="_", width=2, bg="gray", font="Helvetica 9")
        self.flagged = False
        self.revealed = False
        button_event = lambda event="<Button-1>", r=ir, c=ic: hit_event(event, r, c) if not self["state"]=="disabled" else 0
        self.bind("<Button-1>", button_event)
        self.bind("<Button-3>", self.flag)
        self.grid(row=ir, column=ic, sticky=W)

    def flag(self, _event):
        if self.revealed or self["state"] == "disabled": return
        self.flagged = not self.flagged
        self["text"] = "*" if self.flagged else "_"
        self["fg"] = "red" if self.flagged else "black"

    def hit(self, value, override=False):
        if self.revealed or (self.flagged and not override): return False
        self.configure(
            text = self.value_string(value),
            fg = self.value_color(value),
            bg = "light gray" if value != -1 else "black",
            font = "Helvetica 9 bold"
        )
        self.revealed = True
        return True

    def reset(self):
        self.flagged = False
        self.revealed = False
        self["state"] = "normal"
        self.configure(
            text="_",
            fg="black",
            bg="gray",
            font="Helvetica 9"
        )

    def disable(self):
        self["state"] = "disabled"

    @staticmethod
    def value_string(value):
        match value:
            case 0: return ""
            case -1: return "X"
            case _: return str(value)

    @staticmethod
    def value_color(value):
        match value:
            case -1: return "white"
            case 0: return "black"
            case 1: return "blue"
            case 2: return "green"
            case 3: return "red"
            case 4: return "purple"
            case 5: return "orange"
            case 6: return "teal"
            case 7: return "black"
            case 8: return "gray"

class HighScoreLabel(Label):
    def __init__(self, frame, mode):
        super().__init__(frame, relief=SUNKEN, width=10)
        value = get_high_score(mode)
        self["text"] = str(value) if value != -1 else "None"
        self.mode = mode
        self.bind("<Button 3>", lambda event: self.update_value(-1))

    def update_value(self, value):
        self["text"] = str(value) if value != -1 else "None"
        set_high_score(self.mode, value)