from manim import *
import itertools as it
import sympy as sp


class Heat(Rectangle):
    conf = {
        'n_part': 20,
        'config_rect': {
            'width': 6,
            'height': 4
        },
        'margin': .15,
        'just_vertical': True,
        'just_horizontal': True,
        'bounding': True,
    }

    def __init__(self, **kwargs):
        super().__init__(width=self.conf['config_rect']['width'],
                         height=self.conf['config_rect']['height'], color=WHITE)
        self.to_edge(LEFT)
        signatures = np.random.choice(['a', 'b'], size=self.conf['n_part'])
        ball = VGroup(*[
            self.get_ball(self, sign) for x, sign in zip(range(self.conf['n_part']), signatures)
        ])
        self.add(ball)

    def get_ball(self, box, sign):
        speed_factor = np.random.random()
        ball = Dot(radius=0.2, color=interpolate_color(
            BLUE, RED, speed_factor))
        sign = Tex(sign)
        sign.set_height(ball.radius-.05)
        sign.move_to(ball.get_center())
        # sign.set_width(ball.get_width()-0.03)
        sign.set_color(BLACK)
        ball.add(sign)
        speed = 2+3*speed_factor
        direction = rotate_vector(RIGHT, TAU*np.random.random())
        ball.velocity = speed*direction
        x0, y0, z0 = box.get_corner(DL)
        x1, y1, z1 = box.get_corner(UR)
        ball.move_to(np.array([
            interpolate(x0, x1, np.random.random()),
            interpolate(y0, y1, np.random.random()),
            0
        ]))

        def update(ball, dt):
            ball.shift(ball.velocity*dt)
            if self.conf['just_horizontal']:
                if ball.get_left()[0] < box.get_left()[0]+self.conf['margin']:
                    ball.velocity[0] = np.abs(ball.velocity[0])
                if ball.get_right()[0] > box.get_right()[0]-self.conf['margin']:
                    ball.velocity[0] = -np.abs(ball.velocity[0])
            else:
                ball.velocity[0] = 0
            if self.conf['just_vertical']:
                if ball.get_top()[1] > box.get_top()[1]-self.conf['margin']:
                    ball.velocity[1] = -np.abs(ball.velocity[1])
                if ball.get_bottom()[1] < box.get_bottom()[1]+self.conf['margin']:
                    ball.velocity[1] = np.abs(ball.velocity[1])
            else:
                ball.velocity[1] = 0
            return ball
        ball.add_updater(update)
        return ball


class HeatScene(Scene):
    def construct(self):
        heat = Heat()
        self.add(heat)
        self.wait(4)
