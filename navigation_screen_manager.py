from kivy.uix.screenmanager import ScreenManager


class NavigationScreenManager(ScreenManager):
    screen_stack = []
    print("NavigationScreenManager: Inicializando o gerenciador de telas de navegação.")
    print("Stack de telas: ", screen_stack)

    def push(self, screen_name):
        print("Adicionando ao stack:", self.current)  # Para depuração
        # if screen_name not in self.screen_stack:
        self.screen_stack.append(self.current)
        self.transition.direction = 'left'
        self.current = screen_name

    def pop(self):
        screen_stack_len = len(self.screen_stack)
        print("screen_stack_len: ", screen_stack_len)
        if screen_stack_len > 0:
            screen_name = self.screen_stack[-1]
            del self.screen_stack[-1]
            self.transition.direction = 'right'
            self.current = screen_name

    def logout(self):
        self.screen_stack.clear()
        self.current = 'screen_clientes'
