import urwid


class EmailMenu:
    def display_email(self, email):
        subject = urwid.Text(email[0])
        sender = urwid.Text(email[1])
        content = urwid.Text(email[2])
        div = urwid.Divider()
        pile = urwid.Pile([sender, div, subject, div, content])
        top = urwid.Filler(pile, valign="top")
        urwid.MainLoop(top).run()