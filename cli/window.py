import curses


class Window:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.window = stdscr.subwin(10, 40, 1, 1)
        self.is_active = False

    def start(self):
        self.is_active = True
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)

    def close(self):
        self.is_active = False
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
    
    def display(self):
        pass

    def main_loop(self):
        pass