import curses
from cli.login_window import LoginWindow


class CLI:
    def __init__(self):
        self.stdscr = curses.initscr()
        self.login_win = LoginWindow(self.stdscr)

    def start(self):
        self.login_win.display()