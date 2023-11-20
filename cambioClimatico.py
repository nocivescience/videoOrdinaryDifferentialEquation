from manim import *
import itertools as it
class RebotesScene(Scene):
    conf={
        'width':6,
        'height':3,
        'colors':[GREEN,RED,YELLOW,BLUE,PURE_BLUE],
        'n_electrons':40,
    }
    def construct(self):
        box=self.get_box()
        dots=self.get_dots()
        self.add(
            box,
            dots,
        )
        self.wait(8)
        self.get_animation()
        self.wait(8)
        self.play(
            Write(self.precio())
        )
        self.wait(8)
    def get_box(self):
        box=self.box=Rectangle(width=6,height=4)
        box.to_edge(LEFT)
        titulo= Text('Calor').next_to(box,UP,buff=0.5)
        return VGroup(box,titulo)
    def get_dots(self):
        points=np.array([
            [
                np.random.uniform(-3,3),
                np.random.uniform(-2,2),
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
            if(abs(p1.center[0])+0.08)>self.box.width/2:
                p1.center[0]=np.sign(p1.center[0])*(self.box.width/2)
                p1.velocity[0]*=-1*np.sign(p1.velocity[0])*np.sign(p1.center[0])
            elif (abs(p1.center[1]))>self.box.height/2:
                p1.center[1]=np.sign(p1.center[1])*(self.box.height/2)
                p1.velocity[1]*=-1*np.sign(p1.velocity[1])*np.sign(p1.center[1])
        for p in particles:
            p.move_to(p.center)
        
    def get_animation(self):
        color_electron=it.cycle(self.conf['colors'])
        rectangle=Rectangle(width=self.box.width,height=self.box.height).to_edge(RIGHT)
        titulo=Text('Evaporación').next_to(rectangle,UP,buff=0.5)
        self.play(
            Write(titulo)
        )
        dots=VGroup()
        positions=np.array([[np.random.uniform(-self.conf['width']/2+0.1,self.conf['width']/2),
            np.random.uniform(-self.conf['height']/2+0.1,self.conf['height']/2),0] for _ in range(self.conf['n_electrons'])])
        textos=np.random.choice(['a^+','b^-'],size=len(positions))
        for pos,texto in zip(positions,textos):
            dot=Dot().move_to(pos)
            dot.set_color(next(color_electron))
            text=MathTex(texto).set_width(dot.get_width()-0.01)
            text.move_to(dot.get_center())
            text.set_color(BLACK)
            dot.add(text)
            dot.pos=pos
            dots.add(dot)
        def electron_update(mobs,dt):
            for mob in mobs:
                mob.pos[1]+=dt*3
                if mob.pos[1]>rectangle.height/2:
                    mob.pos[1]=-rectangle.height/2
                mob.move_to(mob.pos+3.4*RIGHT)
        dots.add_updater(electron_update)
        self.add(dots,rectangle)
        self.wait(3)
        self.anodoCatodo(rectangle)
        self.wait(2)
    def anodoCatodo(self,rectangle):
        zinc=MathTex('CO').move_to(np.array([-rectangle.width/2,rectangle.height/2,0]))
        platino=MathTex('CO_2').move_to(np.array([rectangle.width/2,rectangle.height/2,0]))
        path=VGroup()
        path.set_points_smoothly([np.array([-rectangle.width/2,rectangle.height/2,0]),ORIGIN+DOWN,np.array([rectangle.width/2,rectangle.height/2,0])])
        VGroup(zinc,platino,path).move_to(3.8*RIGHT+.8*UP)
        self.play(Write(platino),Write(zinc))
        time=0
        while time<5:
            my_time=0.2
            time+=my_time
            self.play(ShowPassingFlash(path.set_color(TEAL_B)),run_time=my_time,time_width=0.2)
        self.wait()
        self.play(*[
            FadeOut(anim) for anim in [platino,zinc]
        ])
    def precio(self):
        return MathTex('\\Delta^- Precio').to_edge(DOWN)