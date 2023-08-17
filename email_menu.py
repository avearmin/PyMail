import urwid


class EmailMenu:
    def __init__(self, key_handler_callback):
        self.view_name = None
        self.loop = None
        self.key_handler = key_handler_callback
        self.start_main_loop()
    
    def start_main_loop(self):
        top = self.get_menu([])
        self.loop = urwid.MainLoop(top, unhandled_input=self.key_handler)

    def set_menu_view(self, choices):
        self.current_choices = choices
        main = urwid.Padding(self.get_menu(choices), left=2, right=2)
        top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
        self.view_name = "MENU"
        self.loop.widget = top
        self.loop.run()

    def get_menu(self, choices):
        body = [urwid.Text("test"), urwid.Divider()]
        for c in choices:
            button = urwid.Button(str(c[1]) + ": " + str(c[0]))
            urwid.connect_signal(button, 'click', self.set_email_view, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
    def set_email_view(self, button, email):
        subject = urwid.Text(email[0])
        sender = urwid.Text(email[1])
        content = urwid.Text(email[2])
        div = urwid.Divider()
        pile = urwid.Pile([sender, div, subject, div, content])
        top = urwid.Filler(pile, valign="top")
        self.view_name = "READ"
        self.loop.widget = top
        self.loop.run()
