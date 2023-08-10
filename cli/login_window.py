from cli.window import Window


class LoginWindow(Window):
    def __init__(self, stdscr):
        super().__init__(stdscr)

    def display(self):
        self.start()
        self.window.addstr(1, 1, "Login Window")
        self.window.refresh()
        self.main_loop()
    
    def main_loop(self):
        while self.is_active:
            key = self.stdscr.getch().lower()
            self.stdscr.clear()
            if key == ord("q"):
                self.close()
                self.is_active = False