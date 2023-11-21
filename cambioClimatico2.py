from manim import *
import itertools as it
import sympy as sp
class RectangleRain(Rectangle):
    def __init__(self, texto, **kwargs):
        super().__init__(**kwargs)
        self.texto=texto
        self.width=4
        self.height=3
        self.add(self.titulo(),self.get_dots())
    def titulo(self):
        titulo=Text(self.texto).next_to(self,UP,buff=0.5)
        return titulo
    def get_dots(self):
        points=np.array([
            [
                np.random.uniform(-self.width/2, self.width/2),
                np.random.uniform(-self.height/2, self.height/2),
                0
            ] for _ in range(40)
        ])
        dots=VGroup(*[
            Dot(radius=0.08).move_to(point) for point in points
        ])
        for dot in dots:
            dot.set_color(RED)
            dot.color=dot.get_color()
            dot.center=dot.get_center()
            dot.velocity=rotate_vector(
                np.random.uniform(0,5)*RIGHT,
                np.random.uniform(0,TAU)
            )
        # dots.move_to(self.get_center())
        dots.add_updater(self.update_particles)
        return dots
    def update_particles(self,particles,dt):
        particles[0].set_color(BLUE)
        for p in particles:
            dist=np.linalg.norm(p.center-particles[0].center)
            if dist<1:
                p.set_color(BLUE)
            else:
                p.set_color(RED)
        for p1 in particles:
            p1.center+=p1.velocity*dt
            if(abs(p1.center[0])+0.08)>self.width/4:
                p1.center[0]=np.sign(p1.center[0])*(self.width/4)
                p1.velocity[0]*=-1*np.sign(p1.velocity[0])*np.sign(p1.center[0])
            elif (abs(p1.center[1]))>self.height/4:
                p1.center[1]=np.sign(p1.center[1])*(self.height/4)
                p1.velocity[1]*=-1*np.sign(p1.velocity[1])*np.sign(p1.center[1])
        for p in particles:
            p.move_to(p.center+4*RIGHT)
class ClimaticChangeScene(Scene):
    configuracion={
        'width':6,
        'height':3,
    }
    def construct(self):
        rectangulo= RectangleRain('Calor',width=4,height=3)
        rectangulo.to_edge(LEFT)
        self.add(rectangulo)
        self.wait(3)