from mobject import Mobject
from mobject.image_mobject import MobjectFromRegion
from mobject.tex_mobject import TextMobject
from region import region_from_polygon_vertices
from topics.geometry import Arrow, Dot, Circle
from topics.number_line import NumberPlane
from scene import Scene
from animation.simple_animations import \
    ShowCreation, Rotating, PhaseFlow, ApplyToCenters
from animation.transform import Transform, ApplyMethod, FadeOut

from helpers import *


class FluidFlow(Scene):
    DEFAULT_CONFIG = {
        "arrow_spacing" : 1,
        "dot_spacing" : 0.5,
        "dot_color" : BLUE_B,
        "text_color" : WHITE,
        "arrow_color" : GREEN_A,
        "points_height" : SPACE_HEIGHT,
        "points_width" : SPACE_WIDTH,
    }
    def use_function(self, function):
        # def normalized_func(point):
            # result = function(point)
            # length = np.linalg.norm(result)
            # if length > 0:
            #     result /= length
            #     # result *= self.arrow_spacing/2.
            # return result
        self.function = function

    def get_points(self, spacing):
        x_radius, y_radius = [
            val-val%spacing
            for val in self.points_width, self.points_height
        ]
        return map(np.array, it.product(
            np.arange(-x_radius, x_radius+spacing, spacing),
            np.arange(-y_radius, y_radius+spacing, spacing),
            [0]
        ))


    def add_plane(self):
        self.add(NumberPlane().fade())

    def add_dots(self):
        points = self.get_points(self.dot_spacing)
        self.dots = Mobject(*map(Dot, points))
        self.dots.highlight(self.dot_color)
        self.play(ShowCreation(self.dots))
        self.dither()

    def add_arrows(self, true_length = False):
        if not hasattr(self, "function"):
            raise Exception("Must run use_function first")
        points = self.get_points(self.arrow_spacing)
        points = filter(
            lambda p : np.linalg.norm(self.function(p)) > 0.01,
            points
        )
        angles = map(angle_of_vector, map(self.function, points))
        prototype = Arrow(
            ORIGIN, RIGHT*self.arrow_spacing/2.,
            color = self.arrow_color, 
            tip_length = 0.1,
            buff = 0
        )
        arrows = []
        for point in points:
            arrow = prototype.copy()
            output = self.function(point)
            if true_length:
                arrow.scale(np.linalg.norm(output))
            arrow.rotate(angle_of_vector(output))
            arrow.shift(point)
            arrows.append(arrow)
        self.arrows = Mobject(*arrows)

        self.play(ShowCreation(self.arrows))
        self.dither()

    def add_paddle(self):
        pass

    def flow(self, **kwargs):
        if not hasattr(self, "function"):
            raise Exception("Must run use_function first")
        self.play(ApplyToCenters(
            PhaseFlow,
            self.dots.split(),
            function = self.function,
            **kwargs
        ))

    def label(self, text, time = 5):
        mob = TextMobject(text)
        mob.scale(1.5)
        mob.to_edge(UP)
        rectangle = region_from_polygon_vertices(*[
            mob.get_corner(vect) + 0.3*vect
            for vect in [
                UP+RIGHT,
                UP+LEFT,
                DOWN+LEFT,
                DOWN+RIGHT
            ]
        ])
        mob.highlight(self.text_color)
        rectangle = MobjectFromRegion(rectangle, "#111111")
        rectangle.point_thickness = 3
        self.add(rectangle, mob)
        self.dither(time)
        self.remove(mob, rectangle)



class InwardFlow(FluidFlow):
    def construct(self):
        circle = Circle(color = YELLOW_C)
        self.use_function(
            lambda p : -p/(2*np.linalg.norm(0.5*p)**0.5+0.01)
        )
        self.add_plane()
        self.add_arrows()  
        self.play(ShowCreation(circle))
        self.label("""
            Notice that arrows point inward around the origin
        """)
        self.label("""
            Watch what that means as we let particles in \\\\
            space flow along the arrows
        """)
        self.remove(circle)
        circle.scale(0.5)
        self.add_dots()        
        self.flow()
        self.remove(self.arrows)
        self.play(ShowCreation(circle))
        self.label("""
            The density of points around \\\\
            the origin has become greater
        """)

        self.label("""
            This means the divergence of the vector field \\\\
            is negative at the origin:
            $\\nabla \\cdot \\vec{\\textbf{v}}(0, 0) < 0$
        """)
        self.dither(3)


class OutwardFlow(FluidFlow):
    def construct(self):
        circle = Circle(color = YELLOW_C, radius = 2)
        self.use_function(
            lambda p : p/(2*np.linalg.norm(0.5*p)**0.5+0.01)
        )
        self.add_plane()
        self.add_arrows()  
        self.play(ShowCreation(circle))
        self.label("""
            On the other hand, when arrows \\\\
            indicate an outward flow\\dots 
        """)
        self.remove(circle)
        circle.scale(0.5)
        self.add_dots()        
        self.flow()
        self.remove(self.arrows)
        self.play(ShowCreation(circle))
        self.label("""
            The density of points near \\\\
            the origin becomes smaller
        """)
        self.label("""
            This means the divergence of the vector field \\\\
            is positive at the origin:
            $\\nabla \\cdot \\vec{\\textbf{v}}(0, 0) > 0$
        """)
        self.dither(3)

class DivergenceArticleExample(FluidFlow):
    def construct(self):
        def raw_function((x, y, z)):
            return (2*x-y, y*y, 0)
        def normalized_function(p):
            result = raw_function(p)
            return result/(np.linalg.norm(result)+0.01)
        self.use_function(normalized_function)

        self.add_plane()
        self.add_arrows()
        self.add_dots()
        self.flow()
        self.remove(self.arrows)
        self.dither(3)



class IncompressibleFluid(FluidFlow):
    DEFAULT_CONFIG = {
        "points_width" : 2*SPACE_WIDTH,
        "points_height" : 1.4*SPACE_HEIGHT
    }
    def construct(self):
        self.use_function(
            lambda (x, y, z) : RIGHT+np.sin(x)*UP
        )
        self.add_plane()
        self.add_arrows()
        self.add_dots()
        for x in range(8):
            self.flow(
                run_time = 1,
                rate_func = None,
            )



class ConstantInwardFlow(FluidFlow):
    DEFAULT_CONFIG = {
        "points_height" : 3*SPACE_HEIGHT,
        "points_width" : 3*SPACE_WIDTH,
    }
    def construct(self):
        self.use_function(
            lambda p : -3*p/(np.linalg.norm(p)+0.1)
        )
        self.add_plane()
        self.add_arrows()
        self.add_dots()
        for x in range(4):
            self.flow(
                run_time = 5,
                rate_func = None,
            )




class ConstantOutwardFlow(FluidFlow):
    def construct(self):
        self.use_function(
            lambda p : p/(2*np.linalg.norm(0.5*p)**0.5+0.01)
        )
        self.add_plane()
        self.add_arrows()
        self.add_dots()
        for x in range(4):
            self.flow(rate_func = None)
            dot = self.dots.split()[0].copy()
            dot.center()
            new_dots = [
                dot.copy().shift(0.5*vect)
                for vect in [
                    UP, DOWN, LEFT, RIGHT, 
                    UP+RIGHT, UP+LEFT, DOWN+RIGHT, DOWN+LEFT
                ]
            ]
            self.dots.add(*new_dots)


class ConstantPositiveCurl(FluidFlow):
    DEFAULT_CONFIG = {
        "points_height" : SPACE_WIDTH,
    }
    def construct(self):
        self.use_function(
            lambda p : 0.5*(-p[1]*RIGHT+p[0]*UP)
        )
        self.add_plane()
        self.add_arrows(true_length = True)
        self.add_dots()
        for x in range(10):
            self.flow(
                rate_func = None
            )



class ComplexCurlExample(FluidFlow):
    def construct(self):
        self.use_function(
            lambda (x, y, z) : np.cos(x+y)*RIGHT+np.sin(x*y)*UP
        )
        self.add_plane()
        self.add_arrows(true_length = True)
        self.add_dots()
        for x in range(4):
            self.flow(
                run_time = 5,
                rate_func = None,
            )


class FourSwirls(FluidFlow):
    DEFAULT_CONFIG = {
        "points_height" :SPACE_WIDTH,
        "points_width" : SPACE_WIDTH,
    }
    def construct(self):
        circles = [
            Circle().shift(3*vect)
            for vect in compass_directions()
        ]
        self.use_function(
            lambda (x, y, z) : 0.5*(y**3-9*y)*RIGHT+(x**3-9*x)*UP
        )
        self.add_plane()
        self.add_arrows()

        Mobject(*circles).show()

        for circle in circles:
            self.play(ShowCreation(circle))
        self.add_dots()
        for x in range(4):
            self.flow(
                run_time = 5,
                rate_func = None,
            )












