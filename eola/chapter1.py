from mobject.tex_mobject import TexMobject
from mobject import Mobject
from mobject.image_mobject import ImageMobject
from mobject.vectorized_mobject import VMobject

from animation.animation import Animation
from animation.transform import *
from animation.simple_animations import *
from animation.playground import *
from topics.geometry import *
from topics.characters import *
from topics.functions import *
from topics.number_line import *
from topics.combinatorics import *
from scene import Scene
from camera import Camera
from mobject.svg_mobject import *
from mobject.tex_mobject import *
from mobject.vectorized_mobject import *

from eola.utils import *

import random


class Physicist(PiCreature):
    CONFIG = {
        "color" : PINK,
    }

class ComputerScientist(PiCreature):
    CONFIG = {
        "color" : PURPLE_E,
        "flip_at_start" : True,
    }    

class OpeningQuote(Scene):
    def construct(self):
        words = TextMobject(
            "``The introduction of numbers as \\\\ coordinates is an act of violence.''",
        )
        words.to_edge(UP)    
        for mob in words.submobjects[27:27+11]:
            mob.highlight(GREEN)
        author = TextMobject("-Hermann Weyl")
        author.highlight(YELLOW)
        author.next_to(words, DOWN, buff = 0.5)

        self.play(FadeIn(words))
        self.dither(1)
        self.play(Write(author, run_time = 4))
        self.dither()


class DifferentConceptions(Scene):
    def construct(self):
        physy = Physicist()
        mathy = Mathematician(mode = "pondering")        
        compy = ComputerScientist()
        creatures = [physy, compy, mathy]
        physy.title = TextMobject("Physics student").to_corner(DOWN+LEFT)
        compy.title = TextMobject("CS student").to_corner(DOWN+RIGHT)
        mathy.title = TextMobject("Mathematician").to_edge(DOWN)
        names = VMobject(physy.title, mathy.title, compy.title)
        names.arrange_submobjects(RIGHT, buff = 1)
        names.to_corner(DOWN+LEFT)
        for pi in creatures:
            pi.next_to(pi.title, UP)

        vector, symbol, coordinates = self.intro_vector()
        for pi in creatures:
            self.play(
                Write(pi.title),
                FadeIn(pi),
                run_time = 1
            )
        self.dither(2)
        self.remove(symbol, coordinates)
        self.physics_conception(creatures, vector)
        self.cs_conception(creatures)
        self.handle_mathy(creatures)

    def intro_vector(self):
        plane = NumberPlane()
        labels = VMobject(*plane.get_coordinate_labels())
        vector = Vector(RIGHT+2*UP, color = YELLOW)
        coordinates = vector_coordinate_label(vector)
        symbol = TexMobject("\\vec{\\textbf{v}}")
        symbol.shift(0.5*(RIGHT+UP))

        self.play(ShowCreation(
            plane, 
            submobject_mode = "lagged_start",
            run_time = 3
        ))
        self.play(ShowCreation(
            vector,
            submobject_mode = "one_at_a_time"
        ))
        self.play(
            Write(labels),
            Write(coordinates),
            Write(symbol)
        )
        self.dither(2)
        self.play(
            FadeOut(plane),
            FadeOut(labels),
            ApplyMethod(vector.shift, 4*LEFT+UP),
            ApplyMethod(coordinates.shift, 2.5*RIGHT+0.5*DOWN),
            ApplyMethod(symbol.shift, 0.5*(UP+LEFT))
        )
        self.remove(plane, labels)
        return vector, symbol, coordinates

    def physics_conception(self, creatures, original_vector):
        self.fade_all_but(creatures, 0)
        physy, compy, mathy = creatures

        vector = Vector(2*RIGHT)
        vector.next_to(physy, UP+RIGHT)
        brace = Brace(vector, DOWN)
        length = TextMobject("Length")
        length.next_to(brace, DOWN)
        group = VMobject(vector, brace, length)
        group.rotate_in_place(np.pi/6)
        vector.get_center = lambda : vector.get_start()        

        direction = TextMobject("Direction")
        direction.next_to(vector, RIGHT)
        direction.shift(UP)

        two_dimensional = TextMobject("Two-dimensional")
        three_dimensional = TextMobject("Three-dimensional")
        two_dimensional.to_corner(UP+RIGHT)
        three_dimensional.to_corner(UP+RIGHT)

        random_vectors = VMobject(*[
            Vector(
                random.uniform(-2, 2)*RIGHT + \
                random.uniform(-2, 2)*UP
            ).shift(
                random.uniform(0, 4)*RIGHT + \
                random.uniform(-1, 2)*UP
            ).highlight(random_color())
            for x in range(5)
        ])

        self.play(
            Transform(original_vector, vector),
            ApplyMethod(physy.change_mode, "speaking")
        )
        self.remove(original_vector)
        self.add(vector )
        self.dither()
        self.play(
            GrowFromCenter(brace),
            Write(length),
            run_time = 1
        )
        self.dither()
        self.remove(brace, length)
        self.play(
            Rotate(vector, np.pi/3, in_place = True),
            Write(direction),
            run_time = 1
        )
        for angle in -2*np.pi/3, np.pi/3:
            self.play(Rotate(
                vector, angle,
                in_place = True,
                run_time = 1
            ))
        self.play(ApplyMethod(physy.change_mode, "plain")) 
        self.remove(direction)
        for point in 2*UP, 4*RIGHT, ORIGIN:
            self.play(ApplyMethod(vector.move_to, point))
        self.dither()
        self.play(
            Write(two_dimensional),
            ApplyMethod(physy.change_mode, "pondering"),
            ShowCreation(random_vectors, submobject_mode = "lagged_start"),
            run_time = 1 
        )
        self.dither(2)
        self.remove(random_vectors, vector)
        self.play(Transform(two_dimensional, three_dimensional))
        self.dither(5)
        self.remove(two_dimensional)
        self.restore_creatures(creatures)

    def cs_conception(self, creatures):
        self.fade_all_but(creatures, 1)
        physy, compy, mathy = creatures

        title = TextMobject("Vectors $\\Leftrightarrow$ lists of numbers")
        title.to_edge(UP)

        vectors = VMobject(*map(matrix_to_mobject, [
            [2, 1],
            [5, 0, 0, -3],
            [2.3, -7.1, 0.1],
        ]))
        vectors.arrange_submobjects(RIGHT, buff = 1)
        vectors.to_edge(LEFT)

        self.play(
            ApplyMethod(compy.change_mode, "sassy"),
            Write(title, run_time = 1)
        )
        self.play(Write(vectors))
        self.dither()
        self.play(ApplyMethod(compy.change_mode, "pondering"))
        self.house_example(vectors, title)
        self.restore_creatures(creatures)


    def house_example(self, starter_mobject, title):
        house = SVGMobject("house")
        house.set_stroke(width = 0)
        house.set_fill(BLUE_C, opacity = 1)
        house.scale_to_fit_height(3)
        house.center()
        square_footage_words = TextMobject("Square footage:")
        price_words = TextMobject("Price: ")
        square_footage = TexMobject("2{,}600\\text{ ft}^2")
        price = TextMobject("\\$300{,}000")

        house.to_edge(LEFT).shift(UP)
        square_footage_words.next_to(house, RIGHT)
        square_footage_words.shift(0.5*UP)
        square_footage_words.highlight(RED)
        price_words.next_to(square_footage_words, DOWN, aligned_edge = LEFT)
        price_words.highlight(GREEN)
        square_footage.next_to(square_footage_words)
        square_footage.highlight(RED)
        price.next_to(price_words)
        price.highlight(GREEN)

        vector = Matrix([square_footage.copy(), price.copy()])
        vector.next_to(house, RIGHT).shift(0.25*UP)
        new_square_footage, new_price = vector.get_mob_matrix().flatten()
        not_equals = TexMobject("\\ne")
        not_equals.next_to(vector)
        alt_vector = Matrix([
            TextMobject("300{,}000\\text{ ft}^2").highlight(RED),
            TextMobject("\\$2{,}600").highlight(GREEN)
        ])
        alt_vector.next_to(not_equals)

        brace = Brace(vector, RIGHT)
        two_dimensional = TextMobject("2 dimensional")
        two_dimensional.next_to(brace)
        brackets = vector.get_brackets()

        self.play(Transform(starter_mobject, house))
        self.remove(starter_mobject)
        self.add(house)
        self.add(square_footage_words)
        self.play(Write(square_footage, run_time = 2))
        self.add(price_words)
        self.play(Write(price, run_time = 2))
        self.dither()
        self.play(
            FadeOut(square_footage_words), FadeOut(price_words),
            Transform(square_footage, new_square_footage),
            Transform(price, new_price),
            Write(brackets),
            run_time = 1
        )
        self.remove(square_footage_words, price_words)
        self.dither()
        self.play(
            Write(not_equals),
            Write(alt_vector),
            run_time = 1
        )
        self.dither()
        self.play(FadeOut(not_equals), FadeOut(alt_vector))
        self.remove(not_equals, alt_vector)
        self.dither()
        self.play(
            GrowFromCenter(brace),
            Write(two_dimensional),
            run_time = 1
        )
        self.dither()

        everything = VMobject(
            house, square_footage, price, brackets, brace, 
            two_dimensional, title
        )
        self.play(ApplyMethod(everything.shift, 2*SPACE_WIDTH*LEFT))
        self.remove(everything)


    def handle_mathy(self, creatures):
        self.fade_all_but(creatures, 2)
        physy, compy, mathy = creatures

        v_color = YELLOW 
        w_color = BLUE
        sum_color = GREEN

        v_arrow = Vector([1, 1])
        w_arrow = Vector([2, 1])
        w_arrow.shift(v_arrow.get_end())
        sum_arrow = Vector(w_arrow.get_end())
        arrows = VMobject(v_arrow, w_arrow, sum_arrow)
        arrows.scale(0.7)
        arrows.to_edge(LEFT, buff = 2)

        v_array = matrix_to_mobject([3, -5])
        w_array = matrix_to_mobject([2, 1])
        sum_array = matrix_to_mobject(["3+2", "-5+1"])
        arrays = VMobject(
            v_array, TexMobject("+"), w_array, TexMobject("="), sum_array
        )
        arrays.arrange_submobjects(RIGHT)
        arrays.scale(0.5)
        arrays.to_edge(RIGHT).shift(UP)

        v_sym = TexMobject("\\vec{\\textbf{v}}")
        w_sym = TexMobject("\\vec{\\textbf{w}}")
        syms = VMobject(v_sym, TexMobject("+"), w_sym)
        syms.arrange_submobjects(RIGHT)
        syms.center().shift(2*UP)

        VMobject(v_arrow, v_array, v_sym).highlight(v_color)
        VMobject(w_arrow, w_array, w_sym).highlight(w_color)
        VMobject(sum_arrow, sum_array).highlight(sum_color)

        self.play(
            Write(syms), Write(arrays),
            ShowCreation(arrows, submobject_mode = "one_at_a_time"),
            ApplyMethod(mathy.change_mode, "pondering"),
            run_time = 2
        )
        self.play(Blink(mathy))
        self.add_scaling(arrows, syms, arrays)

    def add_scaling(self, arrows, syms, arrays):
        s_arrows = VMobject(
            TexMobject("2"), Vector([1, 1]).highlight(YELLOW), 
            TexMobject("="), Vector([2, 2]).highlight(WHITE)
        )
        s_arrows.arrange_submobjects(RIGHT)
        s_arrows.scale(0.75)
        s_arrows.next_to(arrows, DOWN)

        s_arrays = VMobject(
            TexMobject("2"), 
            matrix_to_mobject([3, -5]).highlight(YELLOW),
            TextMobject("="),
            matrix_to_mobject(["2(3)", "2(-5)"])
        )
        s_arrays.arrange_submobjects(RIGHT)
        s_arrays.scale(0.5)
        s_arrays.next_to(arrays, DOWN)

        s_syms = TexMobject(["2", "\\vec{\\textbf{v}}"])
        s_syms.split()[-1].highlight(YELLOW)
        s_syms.next_to(syms, DOWN)

        self.play(
            Write(s_arrows), Write(s_arrays), Write(s_syms),
            run_time = 2
        )
        self.dither()



    def fade_all_but(self, creatures, index):
        self.play(*[
            FadeOut(VMobject(pi, pi.title))
            for pi in creatures[:index] + creatures[index+1:]
        ])

    def restore_creatures(self, creatures):
        self.play(*[
            ApplyFunction(lambda m : m.change_mode("plain").highlight(m.color), pi)
            for pi in creatures
        ] + [
            ApplyMethod(pi.title.set_fill, WHITE, 1.0)
            for pi in creatures
        ])


class ThreeDVectorField(Scene):
    pass


class HelpsToHaveOneThought(Scene):
    def construct(self):
        morty = Mortimer()
        morty.to_corner(DOWN+RIGHT)
        morty.look(DOWN+LEFT)
        new_morty = morty.copy().change_mode("speaking")  
        new_morty.look(DOWN+LEFT)      

        randys = VMobject(*[
            Randolph(color = color).scale(0.8)
            for color in BLUE_D, BLUE_C, BLUE_E
        ])
        randys.arrange_submobjects(RIGHT)
        randys.to_corner(DOWN+LEFT)
        randy = randys.split()[1]

        speech_bubble = morty.get_bubble("speech")
        words = TextMobject("Think of some vector...")
        speech_bubble.position_mobject_inside(words)
        thought_bubble = randy.get_bubble()
        arrow = Vector([2, 1]).scale(0.7)
        or_word = TextMobject("or")
        array = Matrix([2, 1]).scale(0.5)
        q_mark = TextMobject("?")
        thought = VMobject(arrow, or_word, array, q_mark)
        thought.arrange_submobjects(RIGHT, buff = 0.2)
        thought_bubble.position_mobject_inside(thought)
        thought_bubble.set_fill(BLACK, opacity = 1)


        self.add(morty, randys)
        self.play(
            ShowCreation(speech_bubble),
            Transform(morty, new_morty),
            Write(words)
        )
        self.dither(2)
        self.play(
            FadeOut(speech_bubble),
            FadeOut(words),
            ApplyMethod(randy.change_mode, "pondering"),
            ShowCreation(thought_bubble),
            Write(thought)
        )
        self.dither(2)


class HowIWantYouToThinkAboutVectors(Scene):
    def construct(self):
        vector = Vector([-2, 3])
        plane = NumberPlane()
        axis_labels = plane.get_axis_labels()
        other_vectors = VMobject(*map(Vector, [
            [1, 2], [2, -1], [4, 0]
        ]))
        colors = [GREEN_B, MAROON_B, PINK]
        for v, color in zip(other_vectors.split(), colors):
            v.highlight(color)
        shift_val = 4*RIGHT+DOWN

        dot = Dot(radius = 0.1)
        dot.highlight(RED)
        tail_word = TextMobject("Tail")
        tail_word.shift(0.5*DOWN+2.5*LEFT)
        line = Line(tail_word, dot)

        self.play(ShowCreation(vector, submobject_mode = "one_at_a_time"))
        self.dither(2)
        self.play(
            ShowCreation(plane, summobject_mode = "lagged_start"),
            Animation(vector)
        )
        self.play(Write(axis_labels, run_time = 1))
        self.dither()
        self.play(
            GrowFromCenter(dot),
            ShowCreation(line),
            Write(tail_word, run_time = 1)
        )
        self.dither()
        self.play(
            FadeOut(tail_word),
            ApplyMethod(VMobject(dot, line).scale, 0.01) 
        )
        self.remove(tail_word, line, dot)
        self.dither()

        self.play(ApplyMethod(
            vector.shift, shift_val,
            path_arc = 3*np.pi/2,
            run_time = 3
        ))
        self.play(ApplyMethod(
            vector.shift, -shift_val,
            rate_func = rush_into,
            run_time = 0.5
        ))
        self.dither(3)

        self.play(ShowCreation(
            other_vectors, 
            submobject_mode = "one_at_a_time",
            run_time = 3
        ))
        self.dither(3)

        x_axis, y_axis = plane.get_axes().split()
        x_label = axis_labels.split()[0]
        x_axis = x_axis.copy()
        x_label = x_label.copy()
        everything = VMobject(*self.mobjects)
        self.play(
            FadeOut(everything),
            Animation(x_axis), Animation(x_label)
        )


class ListsOfNumbersAddOn(Scene):
    def construct(self):
        arrays = VMobject(*map(matrix_to_mobject, [
            [-2, 3], [1, 2], [2, -1], [4, 0]
        ]))
        arrays.arrange_submobjects(buff = 0.4)
        arrays.scale(2)
        self.play(Write(arrays))
        self.dither(2)


class CoordinateSystemWalkthrough(VectorScene):
    def construct(self):
        self.introduce_coordinate_plane()
        self.show_vector_coordinates()
        self.coords_to_vector([3, -1])
        self.vector_to_coords([-2, -1.5], integer_labels = False)

    def introduce_coordinate_plane(self):
        plane = NumberPlane()
        x_axis, y_axis = plane.get_axes().copy().split()
        x_label, y_label = plane.get_axis_labels().split()
        number_line = NumberLine(tick_frequency = 1)
        x_tick_marks = number_line.get_tick_marks()
        y_tick_marks = x_tick_marks.copy().rotate(np.pi/2)
        tick_marks = VMobject(x_tick_marks, y_tick_marks)
        tick_marks.highlight(WHITE)
        plane_lines = filter(
            lambda m : isinstance(m, Line),
            plane.submobject_family()
        )
        origin_words = TextMobject("Origin")
        origin_words.shift(2*UP+2*LEFT)
        dot = Dot(radius = 0.1).highlight(RED)
        line = Line(origin_words.get_bottom(), dot.get_corner(UP+LEFT))

        unit_brace = Brace(Line(RIGHT, 2*RIGHT))
        one = TexMobject("1").next_to(unit_brace, DOWN)

        self.add(x_axis, x_label)
        self.dither()
        self.play(ShowCreation(y_axis))
        self.play(Write(y_label, run_time = 1))
        self.dither(2)
        self.play(
            Write(origin_words),
            GrowFromCenter(dot),
            ShowCreation(line),
            run_time = 1
        )
        self.dither(2)
        self.play(
            FadeOut(VMobject(origin_words, dot, line))
        )
        self.remove(origin_words, dot, line)
        self.dither()
        self.play(
            ShowCreation(tick_marks, submobject_mode = "one_at_a_time")
        )
        self.play(
            GrowFromCenter(unit_brace),
            Write(one, run_time = 1)            
        )
        self.dither(2)
        self.remove(unit_brace, one)
        self.play(
            *map(GrowFromCenter, plane_lines) + [
            Animation(x_axis), Animation(y_axis)
        ])
        self.dither()
        self.play(
            FadeOut(plane),
            Animation(VMobject(x_axis, y_axis, tick_marks))
        )
        self.remove(plane)
        self.add(tick_marks)

    def show_vector_coordinates(self):
        starting_mobjects = list(self.mobjects)

        vector = Vector([-2, 3])
        x_line = Line(ORIGIN, -2*RIGHT)
        y_line = Line(-2*RIGHT, -2*RIGHT+3*UP)
        x_line.highlight(X_COLOR)
        y_line.highlight(Y_COLOR)

        array = vector_coordinate_label(vector)
        x_label, y_label = array.get_mob_matrix().flatten()
        x_label_copy = x_label.copy()
        x_label_copy.highlight(X_COLOR)
        y_label_copy = y_label.copy()
        y_label_copy.highlight(Y_COLOR)

        point = Dot(4*LEFT+2*UP)
        point_word = TextMobject("(-4, 2) as \\\\ a point")
        point_word.scale(0.7)
        point_word.next_to(point, DOWN)
        point.add(point_word)

        self.play(ShowCreation(vector, submobject_mode = "one_at_a_time"))
        self.play(Write(array))
        self.dither(2)
        self.play(ApplyMethod(x_label_copy.next_to, x_line, DOWN))
        self.play(ShowCreation(x_line))
        self.dither(2)
        self.play(ApplyMethod(y_label_copy.next_to, y_line, LEFT))
        self.play(ShowCreation(y_line))
        self.dither(2)
        self.play(FadeIn(point))
        self.dither()
        self.play(ApplyFunction(
            lambda m : m.scale_in_place(1.25).highlight(YELLOW),
            array.get_brackets(),
            rate_func = there_and_back
        ))
        self.dither()
        self.play(FadeOut(point))
        self.remove(point)
        self.dither()
        self.clear()
        self.add(*starting_mobjects)

class LabeledThreeDVector(Scene):
    pass

class WriteZ(Scene):
    def construct(self):
        z = TexMobject("z").highlight(Z_COLOR)
        z.scale_to_fit_height(4)
        self.play(Write(z, run_time = 2))
        self.dither(3)


class Write3DVector(Scene):
    def construct(self):
        array = Matrix([2, 1, 3]).scale(2)
        x, y, z = array.get_mob_matrix().flatten()
        brackets = array.get_brackets()
        x.highlight(X_COLOR)
        y.highlight(Y_COLOR)
        z.highlight(Z_COLOR)

        self.add(brackets)
        for mob in x, y, z:
            self.play(Write(mob), run_time = 2)
        self.dither()


class VectorAddition(VectorScene):
    def construct(self):
        self.add_plane()
        self.define_addition()
        self.answer_why()

    def define_addition(self):
        v1 = self.add_vector([1, 2])
        v2 = self.add_vector([3, -1], color = MAROON_B)
        l1 = self.label_vector(v1, "v")
        l2 = self.label_vector(v2, "w")
        self.dither()
        self.play(ApplyMethod(v2.shift, v1.get_end()))
        self.dither()
        v_sum = self.add_vector(v2.get_end(), color = PINK)
        sum_tex = "\\vec{\\textbf{v}} + \\vec{\\textbf{w}}"
        self.label_vector(v_sum, sum_tex, rotate = True)
        self.dither(3)

    def answer_why(self):
        pass


class ItDoesntMatterWhich(Scene):
    def construct(self):
        physy = Physicist()
        compy = ComputerScientist()
        physy.title = TextMobject("Physics student").to_corner(DOWN+LEFT)
        compy.title = TextMobject("CS student").to_corner(DOWN+RIGHT)
        for pi in physy, compy:
            pi.next_to(pi.title, UP)
            self.add(pi, pi.title)
        compy_speech = compy.get_bubble("speech")
        physy_speech = physy.get_bubble("speech")
        arrow = Vector([2, 1])
        array = matrix_to_mobject([2, 1])
        goes_to = TexMobject("\\Rightarrow")
        physy_statement = VMobject(arrow, goes_to, array)
        physy_statement.arrange_submobjects(RIGHT)
        compy_statement = physy_statement.copy()
        compy_statement.arrange_submobjects(LEFT)
        physy_speech.position_mobject_inside(physy_statement)
        compy_speech.position_mobject_inside(compy_statement)

        new_arrow = Vector([2, 1])
        x_line = Line(ORIGIN, 2*RIGHT, color = X_COLOR)
        y_line = Line(2*RIGHT, 2*RIGHT+UP, color = Y_COLOR)
        x_mob = TexMobject("2").next_to(x_line, DOWN)
        y_mob = TexMobject("1").next_to(y_line, RIGHT)
        new_arrow.add(x_line, y_line, x_mob, y_mob)
        back_and_forth = VMobject(
            new_arrow,
            TexMobject("\\Leftrightarrow"),
            matrix_to_mobject([2, 1])
        )
        back_and_forth.arrange_submobjects(LEFT).center()


        self.dither()
        self.play(
            ApplyMethod(physy.change_mode, "speaking"),
            ShowCreation(physy_speech),
            Write(physy_statement),
            run_time = 1
        )
        self.play(Blink(compy))
        self.play(
            ApplyMethod(physy.change_mode, "sassy"),
            ApplyMethod(compy.change_mode, "speaking"),
            FadeOut(physy_speech),
            ShowCreation(compy_speech),
            Transform(physy_statement, compy_statement, path_arc = np.pi)
        )
        self.dither(2)
        self.play(
            ApplyMethod(physy.change_mode, "pondering"),
            ApplyMethod(compy.change_mode, "pondering"),
            Transform(compy_speech, VectorizedPoint(compy_speech.get_tip())),
            Transform(physy_statement, back_and_forth)
        )
        self.dither()











