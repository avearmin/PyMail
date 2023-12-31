import urwid


class EmailMenu:
    def __init__(self, key_handler_callback):
        self.view_name = None
        self.current_reply_addr = None
        self.loop = None
        self.key_handler = key_handler_callback
        self.start_main_loop()
    
    def start_main_loop(self):
        top = self.get_menu([])
        self.loop = urwid.MainLoop(top, unhandled_input=self.key_handler)

    def set_menu_view(self, emails: list):
        self.current_choices = emails
        main = urwid.Padding(self.get_menu(emails), left=2, right=2)
        top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
            align='center', width=('relative', 60),
            valign='middle', height=('relative', 60),
            min_width=20, min_height=9)
        self.view_name = 'MENU'
        self.loop.widget = top

    def get_menu(self, emails: list) -> urwid.ListBox:
        key_text = ('UP prev email DOWN next email\n'
            'LEFT prev page RIGHT next page\n'
            '^x exit ^r send email'
        )
        body = [urwid.Text(key_text), urwid.Divider()]
        for email in emails:
            button = urwid.Button(str(email[1]) + ": " + str(email[0]))
            urwid.connect_signal(button, 'click', self.set_email_view, email)
            body.append(urwid.AttrMap(button, None, focus_map='reversed'))
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))
    
    def set_email_view(self, button, email: tuple):
        self.current_reply_addr = email[1]
        top = self.stack_email_sections(email)
        self.view_name = 'READ'
        self.loop.widget = top
    
    def stack_email_sections(self, email) -> urwid.ListBox:
        key_text = '^x back to mail list ^r reply'
        body = [urwid.Text(key_text), urwid.Divider()]
        for section in email:
            body.append(urwid.Text(section))
            body.append(urwid.Divider())
        return urwid.ListBox(urwid.SimpleFocusListWalker(body))

