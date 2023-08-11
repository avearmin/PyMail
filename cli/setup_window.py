import curses
from cli.window import Window


class SetupWindow(Window):
    def __init__(self, stdscr):
        super().__init__(stdscr)
    
    def display(self):
        self.start()
        self.window.addstr(4, 10, "To continue, create a password:")
        self.window.refresh()
    
    def get_password_input(self):
        curses.echo()
        curses.curs_set(1)
        password = self.window.getstr(5, 10)
        curses.noecho()
        curses.curs_set(0)
        return password.decode()

    def main_loop(self):
        while self.is_active:
            key = self.stdscr.getch()
            if key == ord("q") or key == ord("Q"):
                self.close()
                self.is_active = False