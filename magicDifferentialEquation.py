from manim import *
import itertools as it
import sympy as sp
class EquationScene(Scene):
    CONFIG={
        'colors': [
            RED,
            BLUE,
            YELLOW,
            GREEN,
            ORANGE,
        ]
    }
    def construct(self):
        self.colors=it.cycle(self.CONFIG['colors'])
        titulo=Title("Ecuaciones diferenciales")
        for title in titulo.family_members_with_points():
            title.set(color=next(self.colors))
        self.play(Write(titulo))
        self.wait(3)
        group=self.differential_equation()
        self.play(
            LaggedStart(*[
                Write(mob) for mob in group
            ],lag_ratio=.1)
        )
        self.wait(8)
    def get_random_position(self):
        position = np.array([
            np.random.uniform(-config['frame_width']/2+.5, config['frame_width']/2-.5),
            np.random.uniform(-config['frame_height']/2+1, config['frame_height']/2-1),
            0
        ])
        return position
    def differential_equation(self):
        x=sp.Symbol('x')
        f1= sp.sin(4*x)
        f2= sp.cos(4*x)
        f1_diff=sp.diff(f1,x)
        f2_diff=sp.diff(f2,x)
        f1_diff_2=sp.diff(f1_diff,x)
        f2_diff_2=sp.diff(f2_diff,x)
        differential_equation_1=MathTex("\\frac{d}{dx}f(x)=f'(x)")
        differential_equation_2=MathTex("\\frac{d}{dx}f'(x)+y^{(4)}=f''(x)")
        differential_equation_3=MathTex("\\frac{d}{dx}f''(x)+y^{(4)}=f'''(x)-y^{(6)}")
        differential_equation_4=MathTex("\\frac{d}{dy}\\cos(4r)=f''(x)-y^{(6)}")
        differential_equation_5=MathTex("\\frac{d}{dy}\\sin(4r)=f''(x)+\\frac{d}{dx}\\tan(x)-y^{(6)}")
        group=Group(
            MathTex(f1),
            MathTex(f2),
            MathTex(f1_diff),
            MathTex(f2_diff),
            MathTex(f1_diff_2),
            MathTex(f2_diff_2),
            differential_equation_1,
            differential_equation_2,
            differential_equation_3,
            differential_equation_4,
            differential_equation_5,
        )
        for mob in group:
            position=self.get_random_position()
            mob.set_color(next(self.colors))
            mob.shift(position)
        group.to_edge(DOWN)
        return group