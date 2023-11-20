from manim import *
import operator as op


class HowManyHitGet(Scene):
    CONFIG = {
        "mass": 3,
        "MASS": 15,
        "radio": .1,
        "RADIO": 1,
        "velocidad_0": 6,
        "ancho": (config['frame_width']-1)/2
    }

    def construct(self):
        first_scene = self.add_my_dot()

    def get_my_ball(self, masa, radio, velocidad, ancho):
        dot = Dot(radius=radio, fill_opacity=1, stroke_width=0)
        dot.radio = radio
        dot.masa = masa
        dot.center = op.add(
            np.random.uniform(-ancho+radio, ancho-radio)*RIGHT, 0)
        dot.velocidad = rotate_vector(np.random.uniform(0, velocidad)*RIGHT, 0)
        dot.move_to(dot.center)
        return dot

    def get_my_box(self):
        box = Rectangle(
            width=2*self.CONFIG['ancho'], height=2*self.CONFIG['RADIO'])
        box.set_stroke(width=1, color=BLUE)
        box.set_fill(opacity=0)
        return box

    def add_my_dot(self):
        balls = VGroup(*[self.get_my_ball(masa=self.CONFIG['mass'], radio=self.CONFIG['radio'], velocidad=self.CONFIG['velocidad_0'], ancho=self.CONFIG['ancho'])
                         for _ in range(3)
                         ])
        BALL = self.get_my_ball(
            masa=self.CONFIG['MASS'], radio=self.CONFIG['RADIO'], velocidad=0, ancho=self.CONFIG['ancho'])
        all_particles = VGroup(BALL, *balls)
        my_box = self.get_my_box()
        self.play(FadeIn(all_particles), Create(my_box))
        all_particles.add_updater(self.update_particle)
        self.add(all_particles)
        self.wait(10)
        self.get_function(my_box)
        self.wait(10)
    def update_particle(self, particles, dt):
        for p1 in particles:
            p1.center += p1.velocidad*dt
            buff = 0.01
            for p2 in particles:
                if p1 is p2:
                    continue
                dist = np.linalg.norm(p2.center-p1.center)
                diff = dist-(p1.radio+p2.radio)
                if diff < 0:
                    unit_vect = (p2.center-p1.center)/dist
                    p1.center += (diff-buff)*unit_vect/2
                    p2.center -= (diff-buff)*unit_vect/2
                    v1 = p1.velocidad
                    v2 = p2.velocidad
                    m1 = p1.masa
                    m2 = p2.masa
                    u1 = (m2*(v2-v1)+v1*m1+m2*v2)/(m1+m2)
                    u2 = (m1*(v1-v2)+v1*m1+m2*v2)/(m1+m2)
                    p1.velocidad = u1
                    p2.velocidad = u2
            r1 = p1.radio
            c1 = p1.center
            if abs(c1[0])+r1 > self.CONFIG['ancho']:
                c1[0] = np.sign(c1[0])*(self.CONFIG['ancho']-r1)
                p1.velocidad[0] *= -1 * \
                    op.mul(np.sign(p1.velocidad[0]), np.sign(c1[0]))
        for p in particles:
            p.move_to(p.center)
        return particles
    def get_function(self,box):
        grupo=VGroup()
        ecuacion1=MathTex("\\vec{F}= \\displaystyle \\frac{d\\vec{p}}{dt}")
        ecuacion2=MathTex("\\vec{F}= \\displaystyle \\frac{d(m\\vec{v})}{dt}")
        ecuacion3=MathTex("\\vec{F}= \\displaystyle \\frac{dm}{dt}v+m\\frac{d v}{dt}")
        ecuacion4=MathTex("p=m\\vec{v}")
        grupo.add(ecuacion1,ecuacion2,ecuacion3,ecuacion4)
        grupo.next_to(box,UP, buff=.4)
        self.play(Write(ecuacion1))
        self.wait(3)
        self.play(ReplacementTransform(ecuacion1,ecuacion2))
        self.wait(3)
        self.play(ReplacementTransform(ecuacion2,ecuacion3))
        self.wait(3)
        self.play(ReplacementTransform(ecuacion3,ecuacion4))
        self.wait(3)
        self.play(FadeOut(grupo))