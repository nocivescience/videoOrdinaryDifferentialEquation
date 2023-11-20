from manim import *
import itertools as it
import sympy as sp
class RectangleRain(Rectangle):
    def __init__(self, texto, **kwargs):
        self.texto=texto
        super().__init__(**kwargs)
        self.add(self.titulo())
    def titulo(self):
        titulo=Text(self.texto).next_to(self,UP,buff=0.5)
        return titulo
class ClimaticChangeScene(Scene):
    configuracion={
        'width':6,
        'height':3,
    }
    def construct(self):
        rectangulo= RectangleRain('Calor',width=4,height=3)
        rectangulo.to_edge(LEFT)
        self.play(
            Write(rectangulo)
        )