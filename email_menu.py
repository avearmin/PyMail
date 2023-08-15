import urwid


class EmailMenu:
    def display_menu(self, choices):
        main = urwid.Padding(self.get_menu(choices), left=2, right=2)
        top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
        urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()

    def get_menu(self, choices):
        body = [urwid.Text("test"), urwid.Divider()]
        for c in choices:
            button = urwid.Button(str(c[1]) + ": " + str(c[0]))
            urwid.connect_signal(button, 'click', self.display_email, c)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
    def display_email(self, button, email):
        subject = urwid.Text(email[0])
        sender = urwid.Text(email[1])
        content = urwid.Text(email[2])
        div = urwid.Divider()
        pile = urwid.Pile([sender, div, subject, div, content])
        top = urwid.Filler(pile, valign="top")
        urwid.MainLoop(top).run()