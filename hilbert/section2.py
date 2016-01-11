from mobject import Mobject, Point, Mobject1D
from mobject.tex_mobject import \
    TexMobject, TextMobject, Brace
from mobject.image_mobject import \
    ImageMobject, MobjectFromRegion

from scene import Scene

from animation import Animation
from animation.transform import \
    Transform, CounterclockwiseTransform, ApplyMethod,\
    GrowFromCenter, ClockwiseTransform, ApplyPointwiseFunction, \
    ShrinkToCenter, ShimmerIn, FadeOut, FadeIn
from animation.simple_animations import \
    ShowCreation, Homotopy
from animation.meta_animations import \
    DelayByOrder, TransformAnimations
from animation.playground import Vibrate

from topics.geometry import \
    Line, Dot, Arrow, Grid, Square, Point, Circle
from topics.characters import \
    ThoughtBubble, SpeechBubble, Mathematician
from topics.number_line import UnitInterval, NumberLine
from topics.three_dimensions import Stars
from topics.functions import ParametricFunction

from region import region_from_polygon_vertices, Region

import displayer as disp

from hilbert.curves import \
    TransformOverIncreasingOrders, FlowSnake, HilbertCurve, \
    SnakeCurve, PeanoCurve
from hilbert.section1 import get_mathy_and_bubble

from scipy.spatial.distance import cdist

from helpers import *


def get_time_line():
    length = 5.2*SPACE_WIDTH
    year_range = 400
    time_line = NumberLine(
        numerical_radius = year_range/2,
        unit_length_to_spatial_width = length/year_range,
        tick_frequency = 10,
        leftmost_tick = 1720,
        number_at_center = 1870,
        numbers_with_elongated_ticks = range(1700, 2100, 100)
    )
    time_line.sort_points(lambda p : p[0])        
    time_line.gradient_highlight(
        PeanoCurve.DEFAULT_CONFIG["start_color"], 
        PeanoCurve.DEFAULT_CONFIG["end_color"]
    )
    time_line.add_numbers(
        2020, *range(1800, 2050, 50)
    )
    return time_line


class SectionTwo(Scene):
    def construct(self):
        self.add(TextMobject("Section 2: Filling space"))
        self.dither()

class HilbertCurveIsPerfect(Scene):
    def construct(self):
        curve = HilbertCurve(order = 6)
        curve.highlight(WHITE)
        colored_curve = curve.copy()
        colored_curve.thin_out(3)
        lion = ImageMobject("lion", invert = False)
        lion.replace(curve, stretch = True)
        sparce_lion = lion.copy()
        sparce_lion.thin_out(100)
        distance_matrix = cdist(colored_curve.points, sparce_lion.points)
        closest_point_indices = np.apply_along_axis(
            np.argmin, 1, distance_matrix
        )
        colored_curve.rgbs = sparce_lion.rgbs[closest_point_indices]
        line = Line(5*LEFT, 5*RIGHT)
        Mobject.align_data(line, colored_curve)
        line.rgbs = colored_curve.rgbs

        self.add(lion)
        self.play(ShowCreation(curve, run_time = 3))
        self.play(
            FadeOut(lion),
            Transform(curve, colored_curve),
            run_time = 3
        )
        self.dither()
        self.play(Transform(curve, line, run_time = 5))
        self.dither()


class AskMathematicianFriend(Scene):
    def construct(self):
        mathy, bubble = get_mathy_and_bubble()
        bubble.sort_points(lambda p : np.dot(p, UP+RIGHT))

        self.add(mathy)
        self.dither()
        self.play(ApplyMethod(
            mathy.blink, 
            rate_func = squish_rate_func(there_and_back)
        ))
        self.dither()
        self.play(ShowCreation(bubble))
        self.dither()
        self.play(
            ApplyMethod(mathy.shift, 3*(DOWN+LEFT)),
            ApplyPointwiseFunction(
                lambda p : 15*p/np.linalg.norm(p),
                bubble
            ),
            run_time = 3
        )

class TimeLineAboutSpaceFilling(Scene):
    def construct(self):
        curve = PeanoCurve(order = 5)
        curve.stretch_to_fit_width(2*SPACE_WIDTH)
        curve.stretch_to_fit_height(2*SPACE_HEIGHT)
        curve_start = curve.copy()
        curve_start.apply_over_attr_arrays(
            lambda arr : arr[:200]
        )
        time_line = get_time_line()
        time_line.shift(-time_line.number_to_point(2000))

        self.add(time_line)
        self.play(ApplyMethod(
            time_line.shift,
            -time_line.number_to_point(1900),
            run_time = 3
        ))
        brace = Brace(
            Mobject(
                Point(time_line.number_to_point(1865)),
                Point(time_line.number_to_point(1888)),
            ),
            UP
        )
        words = TextMobject("""
            Cantor drives himself (and the \\\\
            mathematical community at large) \\\\
            crazy with research on infinity.
        """)
        words.next_to(brace, UP)
        self.play(
            GrowFromCenter(brace),
            ShimmerIn(words)
        )
        self.dither()
        self.play(
            Transform(time_line, curve_start),
            FadeOut(brace),
            FadeOut(words)
        )
        self.play(ShowCreation(
            curve, 
            run_time = 5,
            rate_func = None
        ))
        self.dither()



class NotPixelatedSpace(Scene):
    def construct(self):
        grid = Grid(64, 64)
        space_region = Region()
        space_mobject = MobjectFromRegion(space_region, DARK_GREY)
        curve = PeanoCurve(order = 5).replace(space_mobject)
        line = Line(5*LEFT, 5*RIGHT)
        line.gradient_highlight(curve.start_color, curve.end_color)
        for mob in grid, space_mobject:
            mob.sort_points(np.linalg.norm)
        infinitely = TextMobject("Infinitely")
        detailed = TextMobject("detailed")
        extending = TextMobject("extending")
        detailed.next_to(infinitely, RIGHT)
        extending.next_to(infinitely, RIGHT)
        Mobject(extending, infinitely, detailed).center()
        arrows = Mobject(*[
            Arrow(2*p, 4*p)
            for theta in np.arange(np.pi/6, 2*np.pi, np.pi/3)
            for p in [rotate_vector(RIGHT, theta)]
        ])

        self.add(grid)
        self.dither()
        self.play(Transform(grid, space_mobject, run_time = 5))
        self.remove(grid)
        self.highlight_region(space_region, DARK_GREY)
        self.dither()
        self.add(infinitely, detailed)
        self.dither()
        self.play(DelayByOrder(Transform(detailed, extending)))
        self.play(ShowCreation(arrows))
        self.dither()
        self.clear()
        self.highlight_region(space_region, DARK_GREY)
        self.play(ShowCreation(line))
        self.play(Transform(line, curve, run_time = 5))



class HistoryOfDiscover(Scene):
    def construct(self):
        time_line = get_time_line()
        time_line.shift(-time_line.number_to_point(1900))
        hilbert_curve = HilbertCurve(order = 3)
        peano_curve = PeanoCurve(order = 2)
        for curve in hilbert_curve, peano_curve:
            curve.scale(0.5)
        hilbert_curve.to_corner(DOWN+RIGHT)
        peano_curve.to_corner(UP+LEFT)
        squares = Mobject(*[
            Square(side_length=3, color=WHITE).replace(curve)
            for curve in hilbert_curve, peano_curve
        ])


        self.add(time_line)
        self.dither()
        for year, curve, vect, text in [
            (1890, peano_curve, UP, "Peano Curve"), 
            (1891, hilbert_curve, DOWN, "Hilbert Curve"),
            ]:
            point = time_line.number_to_point(year)
            point[1] = 0.2
            arrow = Arrow(point+2*vect, point, buff = 0.1)
            arrow.gradient_highlight(curve.start_color, curve.end_color)
            year_mob = TexMobject(str(year))
            year_mob.next_to(arrow, vect)
            words = TextMobject(text)
            words.next_to(year_mob, vect)

            self.play(
                ShowCreation(arrow), 
                ShimmerIn(year_mob),
                ShimmerIn(words)
            )
            self.play(ShowCreation(curve))
            self.dither()
        self.play(ShowCreation(squares))
        self.dither()
        self.play(ApplyMethod(
            Mobject(*self.mobjects).shift, 20*(DOWN+RIGHT)
        ))



class DefinitionOfCurve(Scene):
    def construct(self):
        start_words = TextMobject([
            "``", "Space Filling", "Curve ''",
        ]).to_edge(TOP, buff = 0.25)
        quote, space_filling, curve_quote = start_words.copy().split()
        curve_quote.shift(
            space_filling.get_left()-\
            curve_quote.get_left()
        )
        space_filling = Point(space_filling.get_center())                
        end_words = Mobject(*[
            quote, space_filling, curve_quote
        ]).center().to_edge(TOP, buff = 0.25)
        space_filling_fractal = TextMobject("""
            ``Space Filling Fractal''
        """).to_edge(UP)
        curve = HilbertCurve(order = 2).shift(DOWN)
        fine_curve = HilbertCurve(order = 8)
        fine_curve.replace(curve)
        dots = Mobject(*[
            Dot(
                curve.points[n*curve.get_num_points()/15],
                color = YELLOW_C
            )
            for n in range(1, 15)
            if n not in [4, 11]
        ])

        start_words.shift(2*(UP+LEFT))
        self.play(
            ApplyMethod(start_words.shift, 2*(DOWN+RIGHT))
        )
        self.dither()
        self.play(Transform(start_words, end_words))
        self.dither()
        self.play(ShowCreation(curve))
        self.dither()
        self.play(ShowCreation(
            dots, 
            run_time = 3,
        ))
        self.dither()
        self.clear()
        self.play(ShowCreation(fine_curve, run_time = 5))
        self.dither()
        self.play(ShimmerIn(space_filling_fractal))
        self.dither()


class PseudoHilbertCurvesDontFillSpace(Scene):
    def construct(self):
        curve = HilbertCurve(order = 1)
        grid = Grid(2, 2, point_thickness=1)
        self.add(grid, curve)
        for order in range(2, 6):
            self.dither()
            new_grid = Grid(2**order, 2**order, point_thickness=1)
            self.play(
                ShowCreation(new_grid),
                Animation(curve)          
            )
            self.remove(grid)
            grid = new_grid
            self.play(Transform(
                curve, HilbertCurve(order = order)
            ))


        square = Square(side_length = 6, color = WHITE)
        square.corner = Mobject1D()
        square.corner.add_line(3*DOWN, ORIGIN)
        square.corner.add_line(ORIGIN, 3*RIGHT)
        square.digest_mobject_attrs()
        square.scale(2**(-5))
        square.corner.highlight(
            Color(rgb = curve.rgbs[curve.get_num_points()/3])
        )
        square.shift(
            grid.get_corner(UP+LEFT)-\
            square.get_corner(UP+LEFT)
        )


        self.dither()
        self.play(
            FadeOut(grid), 
            FadeOut(curve),
            FadeIn(square)
        )
        self.play(
            ApplyMethod(square.replace, grid)
        )
        self.dither()


class HilbertCurveIsLimit(Scene):
    def construct(self):
        mathy, bubble = get_mathy_and_bubble()
        bubble.write(
            "A Hilbert curve is the \\\\ limit of all these \\dots"
        )

        self.add(mathy, bubble)
        self.play(ShimmerIn(bubble.content))
        self.dither()


class DefiningCurves(Scene):
    def construct(self):
        words = TextMobject(
            ["One does not simply define the limit \\\\ \
            of a sequence of","curves","\\dots"]
        )
        top_words = TextMobject([
            "curves", "are functions"
        ]).to_edge(UP)
        curves1 = words.split()[1]
        curves2 = top_words.split()[0]
        words.ingest_sub_mobjects()
        number = TexMobject("0.27")
        pair = TexMobject("(0.53, 0.02)")
        pair.next_to(number, buff = 2)
        arrow = Arrow(number, pair)
        Mobject(number, arrow, pair).center().shift(UP)
        number_line = UnitInterval()
        number_line.stretch_to_fit_width(5)
        number_line.to_edge(LEFT).shift(DOWN)
        grid = Grid(4, 4).scale(0.4)
        grid.next_to(number_line, buff = 2)
        low_arrow = Arrow(number_line, grid)

        self.play(ShimmerIn(words))
        self.dither()
        self.play(
            FadeOut(words),
            ApplyMethod(curves1.replace, curves2),
            ShimmerIn(top_words.split()[1])
        )
        self.dither()
        self.play(FadeIn(number))
        self.play(ShowCreation(arrow))
        self.play(FadeIn(pair))
        self.dither()
        self.play(ShowCreation(number_line))
        self.play(ShowCreation(low_arrow))
        self.play(ShowCreation(grid))
        self.dither()


class PseudoHilbertCurveAsFunctionExample(Scene):
    args_list = [(2,), (3,)]

    # For subclasses to turn args in the above  
    # list into stings which can be appended to the name
    @staticmethod
    def args_to_string(order):
        return "Order%d"%order
        
    @staticmethod
    def string_to_args(order_str):
        return int(order_str)


    def construct(self, order):
        if order == 2:
            result_tex = "(0.125, 0.75)"
        elif order == 3:
            result_tex = "(0.0758,  0.6875)"

        phc, arg, result = TexMobject([
            "\\text{PHC}_%d"%order, 
            "(0.3)", 
            "= %s"%result_tex
        ]).to_edge(UP).split()
        function = TextMobject("Function", size = "\\normal")
        function.shift(phc.get_center()+DOWN+2*LEFT)
        function_arrow = Arrow(function, phc)

        line = Line(5*LEFT, 5*RIGHT)
        curve = HilbertCurve(order = order)
        line.match_colors(curve)
        grid = Grid(2**order, 2**order)
        grid.fade()
        for mob in curve, grid:
            mob.scale(0.7)
        index = int(0.3*line.get_num_points())
        dot1 = Dot(line.points[index])
        arrow1 = Arrow(arg, dot1, buff = 0.1)
        dot2 = Dot(curve.points[index])
        arrow2 = Arrow(result.get_bottom(), dot2, buff = 0.1)

        self.add(phc)
        self.play(
            ShimmerIn(function),
            ShowCreation(function_arrow)
        )
        self.dither()
        self.remove(function_arrow, function)
        self.play(ShowCreation(line))
        self.dither()
        self.play(
            ShimmerIn(arg),
            ShowCreation(arrow1),
            ShowCreation(dot1)
        )
        self.dither()
        self.remove(arrow1)
        self.play(
            FadeIn(grid),            
            Transform(line, curve),
            Transform(dot1, dot2),
            run_time = 2
        )
        self.dither()
        self.play(
            ShimmerIn(result),
            ShowCreation(arrow2)
        )
        self.dither()



class ContinuityRequired(Scene):
    def construct(self):
        words = TextMobject([
            "A function must be",
            "\\emph{continuous}", 
            "if it is to represent a curve."
        ])
        words.split()[1].highlight(YELLOW_C)
        self.add(words)
        self.dither()




class FormalDefinitionOfContinuity(Scene):
    def construct(self):
        self.setup()
        self.label_spaces()
        self.move_dot()
        self.label_jump()
        self.draw_circles()
        self.vary_circle_sizes()
        self.discontinuous_point()


    def setup(self):
        self.input_color = YELLOW_C
        self.output_color = RED
        def spiril(t):
            theta = 2*np.pi*t
            return t*np.cos(theta)*RIGHT+t*np.sin(theta)*UP

        self.spiril1 = ParametricFunction(
            lambda t : 1.5*RIGHT + DOWN + 2*spiril(t),
            density = 5*DEFAULT_POINT_DENSITY_1D,
        )
        self.spiril2 = ParametricFunction(
            lambda t : 5.5*RIGHT + UP - 2*spiril(1-t),
            density = 5*DEFAULT_POINT_DENSITY_1D,
        )
        Mobject.align_data(self.spiril1, self.spiril2)
        self.output = Mobject(self.spiril1, self.spiril2)
        self.output.ingest_sub_mobjects()
        self.output.highlight(GREEN_A)

        self.interval = UnitInterval()
        self.interval.scale_to_fit_width(SPACE_WIDTH-1)
        self.interval.to_edge(LEFT)

        self.input_dot = Dot(color = self.input_color)
        self.output_dot = self.input_dot.copy().highlight(self.output_color)
        left, right = self.interval.get_left(), self.interval.get_right()
        self.input_homotopy = lambda (x, y, z, t) : (x, y, t) + interpolate(left, right, t)
        output_size = self.output.get_num_points()-1
        output_points = self.output.points        
        self.output_homotopy = lambda (x, y, z, t) : (x, y, z) + output_points[int(t*output_size)]

    def get_circles_and_points(self, min_input, max_input):
        input_left, input_right = [
            self.interval.number_to_point(num)
            for num in min_input, max_input
        ]
        input_circle = Circle(
            radius = np.linalg.norm(input_left-input_right)/2,
            color = WHITE
        )
        input_circle.shift((input_left+input_right)/2)

        input_points = Line(
            input_left, input_right, 
            color = self.input_color
        )
        output_points = Mobject(color = self.output_color)
        n = self.output.get_num_points()
        output_points.add_points(
            self.output.points[int(min_input*n):int(max_input*n)]
        )
        output_center = output_points.points[int(0.5*output_points.get_num_points())]
        max_distance = np.linalg.norm(output_center-output_points.points[-1])
        output_circle = Circle(
            radius = max_distance, 
            color = WHITE
        )
        output_circle.shift(output_center)
        return (
            input_circle, 
            input_points, 
            output_circle, 
            output_points
        )


    def label_spaces(self):
        input_space = TextMobject("Input Space")
        input_space.to_edge(UP)        
        input_space.shift(LEFT*SPACE_WIDTH/2)
        output_space = TextMobject("Output Space")
        output_space.to_edge(UP)
        output_space.shift(RIGHT*SPACE_WIDTH/2)
        line = Line(
            UP*SPACE_HEIGHT, DOWN*SPACE_HEIGHT, 
            color = WHITE
        )
        self.play(
            ShimmerIn(input_space),
            ShimmerIn(output_space),
            ShowCreation(line),
            ShowCreation(self.interval),
        )
        self.dither()

    def move_dot(self):
        kwargs = {
            "rate_func" : None,
            "run_time"  : 3
        }
        self.play(
            Homotopy(self.input_homotopy, self.input_dot, **kwargs),
            Homotopy(self.output_homotopy, self.output_dot, **kwargs),
            ShowCreation(self.output, **kwargs)
        )
        self.dither()

    def label_jump(self):
        jump_points = Mobject(
            Point(self.spiril1.points[-1]),
            Point(self.spiril2.points[0])
        )
        self.brace = Brace(jump_points, RIGHT)
        self.jump = TextMobject("Jump")
        self.jump.next_to(self.brace, RIGHT)
        self.play(
            GrowFromCenter(self.brace),
            ShimmerIn(self.jump)
        )
        self.dither()
        self.remove(self.brace, self.jump)


    def draw_circles(self):
        input_value = 0.45
        input_radius = 0.04
        for dot in self.input_dot, self.output_dot:
            dot.center()
        kwargs = {
            "rate_func" : lambda t : interpolate(1, input_value, smooth(t))
        }
        self.play(
            Homotopy(self.input_homotopy, self.input_dot, **kwargs),
            Homotopy(self.output_homotopy, self.output_dot, **kwargs)
        )

        A, B = map(Mobject.get_center, [self.input_dot, self.output_dot])
        A_text = TextMobject("A")
        A_text.shift(A+2*(LEFT+UP))
        A_arrow = Arrow(
            A_text, self.input_dot,
            color = self.input_color
        )
        B_text = TextMobject("B")
        B_text.shift(B+2*RIGHT+DOWN)
        B_arrow = Arrow(
            B_text, self.output_dot,
            color = self.output_color
        )
        tup = self.get_circles_and_points(
            input_value-input_radius, 
            input_value+input_radius
        )
        input_circle, input_points, output_circle, output_points = tup

        for text, arrow in [(A_text, A_arrow), (B_text, B_arrow)]:
            self.play(
                ShimmerIn(text),
                ShowCreation(arrow)
            )
            self.dither()
        self.remove(A_text, A_arrow, B_text, B_arrow)
        self.play(ShowCreation(input_circle))
        self.dither()
        self.play(ShowCreation(input_points))
        self.dither()
        input_points_copy = input_points.copy()
        self.play(
            Transform(input_points_copy, output_points),
            run_time = 2
        )
        self.dither()
        self.play(ShowCreation(output_circle))
        self.dither()
        self.dither()
        self.remove(*[
            input_circle, input_points, 
            output_circle, input_points_copy
        ])


    def vary_circle_sizes(self):
        input_value = 0.45
        radius = 0.04
        vary_circles = VaryCircles(
            self, input_value, radius, 
            run_time = 5,
        )
        self.play(vary_circles)
        self.dither()
        text = TextMobject("Function is ``Continuous at A''")
        text.shift(2*UP).to_edge(LEFT)
        arrow = Arrow(text, self.input_dot)
        self.play(
            ShimmerIn(text),
            ShowCreation(arrow)
        )
        self.dither()
        self.remove(vary_circles.mobject, text, arrow)

    def discontinuous_point(self):
        point_description = TextMobject(
            "Point where the function jumps"
        )
        point_description.shift(3*RIGHT)
        text = TextMobject("""
            Circle around ouput \\\\ 
            points can never \\\\
            be smaller than \\\\
            the jump
        """)
        text.scale(0.75)
        text.shift(3.5*RIGHT)

        input_value = 0.5
        input_radius = 0.04
        vary_circles = VaryCircles(
            self, input_value, input_radius, 
            run_time = 5,
        )
        for dot in self.input_dot, self.output_dot:
            dot.center()
        kwargs = {
            "rate_func" : lambda t : interpolate(0.45, input_value, smooth(t))
        }
        self.play(
            Homotopy(self.input_homotopy, self.input_dot, **kwargs),
            Homotopy(self.output_homotopy, self.output_dot, **kwargs)
        )
        arrow = Arrow(
            point_description, self.output_dot,
            buff = 0.05,
            color = self.output_color
        )
        self.play(
            ShimmerIn(point_description),
            ShowCreation(arrow)
        )
        self.dither()
        self.remove(point_description, arrow)

        tup = self.get_circles_and_points(
            input_value-input_radius, 
            input_value+input_radius
        )
        input_circle, input_points, output_circle, output_points = tup
        input_points_copy = input_points.copy()
        self.play(ShowCreation(input_circle))
        self.play(ShowCreation(input_points))
        self.play(
            Transform(input_points_copy, output_points),
            run_time = 2
        )
        self.play(ShowCreation(output_circle))
        self.dither()
        self.play(ShimmerIn(text))
        self.remove(input_circle, input_points, output_circle, input_points_copy)
        self.play(vary_circles)
        self.dither()
        self.remove(vary_circles.mobject)

    def continuous_point(self):
        pass



class VaryCircles(Animation):
    def __init__(self, scene, input_value, radius, **kwargs):
        digest_locals(self)
        Animation.__init__(self, Mobject(), **kwargs)

    def update_mobject(self, alpha):
        radius = self.radius + 0.9*self.radius*np.sin(1.5*np.pi*alpha)
        self.mobject = Mobject(*self.scene.get_circles_and_points(
            self.input_value-radius,
            self.input_value+radius
        )).ingest_sub_mobjects()


class FunctionIsContinuousText(Scene):
    def construct(self):
        all_points = TextMobject("$f$ is continuous at every input point")
        continuous = TextMobject("$f$ is continuous")
        all_points.shift(UP)
        continuous.shift(DOWN)
        arrow = Arrow(all_points, continuous)

        self.play(ShimmerIn(all_points))
        self.play(ShowCreation(arrow))
        self.play(ShimmerIn(continuous))
        self.dither()


class DefineActualHilbertCurveText(Scene):
    def construct(self):
        self.add(TextMobject("""
            Finally define a Hilbert Curve\\dots
        """))
        self.dither()


class ReliesOnWonderfulProperty(Scene):
    def construct(self):
        self.add(TextMobject("""
            \\dots which relies on a certain property
            of Pseudo-Hilbert-curves.
        """))
        self.dither()


class WonderfulPropertyOfPseudoHilbertCurves(Scene):
    def construct(self):
        val = 0.3
        text = TextMobject([
            "PHC", "$_n", "(", "%3.1f"%val, ")$", 
            " has a ", "limit point ", "as $n \\to \\infty$"
        ])
        func_parts = text.copy().split()[:5]
        Mobject(*func_parts).center().to_edge(UP)
        num_str, val_str = func_parts[1], func_parts[3]
        curve = UnitInterval()
        curve.sort_points(lambda p : p[0])
        dot = Dot().shift(curve.number_to_point(val))
        arrow = Arrow(val_str, dot, buff = 0.1)
        curve.add_numbers(0, 1)

        self.play(ShowCreation(curve))
        self.play(
            ShimmerIn(val_str),
            ShowCreation(arrow),
            ShowCreation(dot)
        )
        self.dither()
        self.play(
            FadeOut(arrow),
            *[
                FadeIn(func_parts[i])
                for i in 0, 1, 2, 4
            ]
        )
        for num in range(2,9):
            new_curve = HilbertCurve(order = num)
            new_curve.scale(0.8)
            new_dot = Dot(new_curve.points[int(val*new_curve.get_num_points())])
            new_num_str = TexMobject(str(num)).replace(num_str)
            self.play(
                Transform(curve, new_curve),
                Transform(dot, new_dot),
                Transform(num_str, new_num_str)
            )
            self.dither()

        text.to_edge(UP)
        text_parts = text.split()
        for index in 1, -1:
            text_parts[index].highlight()
        starters = Mobject(*func_parts + [
            Point(mob.get_center(), point_thickness=1)
            for mob in text_parts[5:]
        ])
        self.play(Transform(starters, text))
        arrow = Arrow(text_parts[-2].get_bottom(), dot, buff = 0.1)
        self.play(ShowCreation(arrow))
        self.dither()

class FollowManyPoints(Scene):
    def construct(self):
        text = TextMobject([
            "PHC", "_n", "(", "x", ")$", 
            " has a limit point ", "as $n \\to \\infty$",
            "\\\\ for all $x$"
        ])
        parts = text.split()
        parts[-1].next_to(Mobject(*parts[:-1]), DOWN)
        parts[-1].highlight(BLUE)
        parts[3].highlight(BLUE)
        parts[1].highlight()
        parts[-2].highlight()
        text.to_edge(UP)
        curve = UnitInterval()
        curve.sort_points(lambda p : p[0])
        vals = np.arange(0.1, 1, 0.1)
        dots = Mobject(*[
            Dot(curve.number_to_point(val))
            for val in vals
        ])
        curve.add_numbers(0, 1)
        starter_dots = dots.copy().ingest_sub_mobjects()
        starter_dots.shift(2*UP)

        self.add(curve, text)
        self.dither()
        self.play(DelayByOrder(ApplyMethod(starter_dots.shift, 2*DOWN)))
        self.dither()
        self.remove(starter_dots)
        self.add(dots)
        for num in range(1, 10):
            new_curve = HilbertCurve(order = num)
            new_curve.scale(0.8)
            new_dots = Mobject(*[
                Dot(new_curve.points[int(val*new_curve.get_num_points())])
                for val in vals
            ])
            self.play(
                Transform(curve, new_curve),
                Transform(dots, new_dots),
            )
            # self.dither()


class FormalDefinitionOfHilbertCurve(Scene):
    def construct(self):
        val = 0.7
        text = TexMobject([
            "\\text{HC}(", "x", ")",
            "=\\lim_{n \\to \\infty}\\text{PHC}_n(", "x", ")"
        ])
        text.to_edge(UP)
        x1 = text.split()[1]
        x2 = text.split()[-2]
        x2.highlight(BLUE)
        explanation = TextMobject("Actual Hilbert curve function")
        exp_arrow = Arrow(explanation, text.split()[0])
        curve = UnitInterval()
        dot = Dot(curve.number_to_point(val))
        x_arrow = Arrow(x1.get_bottom(), dot, buff = 0)
        curve.sort_points(lambda p : p[0])
        curve.add_numbers(0, 1)

        self.add(*text.split()[:3])
        self.play(
            ShimmerIn(explanation),
            ShowCreation(exp_arrow)
        )
        self.dither()
        self.remove(explanation, exp_arrow)
        self.play(ShowCreation(curve))
        self.play(
            ApplyMethod(x1.highlight, BLUE),
            ShowCreation(x_arrow), 
            ShowCreation(dot)
        )
        self.dither()
        self.remove(x_arrow)
        limit = Mobject(*text.split()[3:]).ingest_sub_mobjects()
        limit.point_thickness = 1
        self.play(ShimmerIn(limit))
        for num in range(1, 9):
            new_curve = HilbertCurve(order = num)
            new_curve.scale(0.8)
            new_dot = Dot(new_curve.points[int(val*new_curve.get_num_points())])
            self.play(
                Transform(curve, new_curve),
                Transform(dot, new_dot),
            )


class CouldNotDefineForSnakeCurve(Scene):
    def construct(self):
        self.add(TextMobject("""
            You could not define a limit curve from
            snake curves.
        """))
        self.dither()

class ThreeThingsToProve(Scene):
    def construct(self):
        definition = TexMobject([
            "\\text{HC}(", "x", ")",
            "=\\lim_{n \\to \\infty}\\text{PHC}_n(", "x", ")"
        ])
        definition.to_edge(UP)
        definition.split()[1].highlight(BLUE)
        definition.split()[-2].highlight(BLUE)
        intro = TextMobject("Three things need to be proven")
        prove_that = TextMobject("Prove that HC is $\\dots$")
        prove_that.scale(0.7)
        prove_that.to_edge(LEFT)
        items = TextMobject([
            "\\begin{enumerate}",
            "\\item Well-defined: ",
            "Points on Pseudo-Hilbert-curves really do converge",
            "\\item A Curve: ",
            "HC is continuous",
            "\\item Space-filling: ",
            "Each point in the unit square is an output of HC",
            "\\end{enumerate}",
        ]).split()
        items[1].highlight(GREEN)
        items[3].highlight(YELLOW_C)
        items[5].highlight(MAROON)
        Mobject(*items).to_edge(RIGHT)

        self.add(definition)
        self.play(ShimmerIn(intro))
        self.dither()
        self.play(Transform(intro, prove_that))
        for item in items[1:-1]:
            self.play(ShimmerIn(item))
            self.dither()



class TilingSpace(Scene):
    def construct(self):
        coords_set = [ORIGIN]
        for n in range(int(2*SPACE_WIDTH)):
            for vect in UP, RIGHT:
                for k in range(n):
                    new_coords = coords_set[-1]+((-1)**n)*vect
                    coords_set.append(new_coords)
        square = Square(side_length = 1, color = WHITE)
        squares = Mobject(*[
            square.copy().shift(coords)
            for coords in coords_set
        ]).ingest_sub_mobjects()
        self.play(
            DelayByOrder(FadeIn(squares)),
            run_time = 3
        )
        curve = HilbertCurve(order = 6).scale(1./6)
        all_curves = Mobject(*[
            curve.copy().shift(coords)
            for coords in coords_set
        ]).ingest_sub_mobjects()
        all_curves.thin_out(10)
        self.play(ShowCreation(
            all_curves,
            rate_func = None,
            run_time = 15
        ))





