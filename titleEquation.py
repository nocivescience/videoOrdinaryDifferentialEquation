from manim import *
import itertools
class TituloScene(Scene):
    def construct(self):
        titulo=Text("Ecuaciones diferenciales" ,t2c={"diferenciales":RED,"Ecuaciones":BLUE})
        self.play(Write(titulo))
        self.wait(10)