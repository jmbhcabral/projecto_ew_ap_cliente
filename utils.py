from kivy.uix.image import AsyncImage
from kivy.animation import Animation


class AnimatedAsyncImage(AsyncImage):
    def on_load(self, *args):
        # Certifique-se de chamar o super para manter o comportamento padrão
        super(AnimatedAsyncImage, self).on_load(*args)

        # Resetar para o estado inicial
        self.opacity = 0
        self.scale = 1

        # Criar a animação
        anim = Animation(opacity=1, duration=1) + \
            Animation(scale=2, duration=1)

        # Iniciar a animação
        anim.start(self)
