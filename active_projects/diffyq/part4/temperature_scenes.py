from manimlib.imports import *
from active_projects.diffyq.part2.heat_equation import BringTwoRodsTogether
from active_projects.diffyq.part3.staging import FourierSeriesIllustraiton


class StepFunctionExample(BringTwoRodsTogether, FourierSeriesIllustraiton):
    CONFIG = {
        "axes_config": {
            "y_min": -1.5,
            "y_max": 1.5,
            "y_axis_config": {
                "unit_size": 2.5,
                "tick_frequency": 0.5,
            },
            "x_min": 0,
            "x_max": 1,
            "x_axis_config": {
                "unit_size": 8,
                "tick_frequency": 0.1,
                "include_tip": False,
            },
        },
        "graph_x_min": 0,
        "graph_x_max": 1,
        "midpoint": 0.5,
        "min_temp": -1,
        "max_temp": 1,
        "alpha": 0.25,
        "step_size": 0.01,
        "n_range": range(1, 41, 2),
    }

    def construct(self):
        self.setup_axes()
        self.setup_graph()
        self.setup_clock()

        self.bring_rods_together()
        self.let_evolve_for_a_bit()
        self.add_labels()
        self.compare_to_sine_wave()
        self.sum_of_sine_waves()

    def bring_rods_together(self):
        rods = VGroup(
            self.get_rod(0, 0.5),
            self.get_rod(0.5, 1),
        )
        rods.add_updater(self.update_rods)

        arrows = VGroup(
            Vector(RIGHT).next_to(rods[0], UP),
            Vector(LEFT).next_to(rods[1], UP),
        )

        words = VGroup(
            TextMobject("Hot").next_to(rods[0], DOWN),
            TextMobject("Cold").next_to(rods[1], DOWN),
        )

        for pair in rods, words:
            pair.save_state()
            pair.space_out_submobjects(1.2)

        black_rects = VGroup(*[
            Square(
                side_length=1,
                fill_color=BLACK,
                fill_opacity=1,
                stroke_width=0,
            ).move_to(self.axes.c2p(0, u))
            for u in [1, -1]
        ])
        black_rects[0].add_updater(
            lambda m: m.align_to(rods[0].get_right(), LEFT)
        )
        black_rects[1].add_updater(
            lambda m: m.align_to(rods[1].get_left(), RIGHT)
        )

        self.add(
            self.axes,
            self.graph,
            self.clock,
        )
        self.add(rods, words)
        self.add(black_rects)

        kw = {
            "run_time": 2,
            "rate_func": rush_into,
        }
        self.play(
            Restore(rods, **kw),
            Restore(words, **kw),
            *map(ShowCreation, arrows)
        )
        self.remove(black_rects)

        self.to_fade = VGroup(words, arrows)
        self.rods = rods

    def let_evolve_for_a_bit(self):
        rods = self.rods
        # axes = self.axes
        time_label = self.time_label
        graph = self.graph
        graph.save_state()

        graph.add_updater(self.update_graph)
        time_label.next_to(self.clock, DOWN)
        time_label.add_updater(
            lambda d, dt: d.increment_value(dt)
        )
        rods.add_updater(self.update_rods)

        self.add(time_label)
        self.play(
            FadeOut(self.to_fade),
            self.get_clock_anim(1)
        )
        self.play(self.get_clock_anim(3))

        time_label.clear_updaters()
        graph.clear_updaters()
        self.play(
            self.get_clock_anim(
                -4,
                run_time=1,
                rate_func=smooth,
            ),
            graph.restore,
            time_label.set_value, 0,
        )
        rods.clear_updaters()
        self.wait()

    def add_labels(self):
        axes = self.axes
        y_axis = axes.y_axis
        x_axis = axes.x_axis
        y_numbers = y_axis.get_number_mobjects(
            *np.arange(-1, 1.5, 0.5),
            number_config={
                "unit": "^\\circ",
                "num_decimal_places": 1,
            }
        )
        x_numbers = x_axis.get_number_mobjects(
            *np.arange(0.2, 1.2, 0.2),
            number_config={
                "num_decimal_places": 1,
            },
        )

        self.play(FadeIn(y_numbers))
        self.play(ShowCreationThenFadeAround(y_numbers[-1]))
        self.play(ShowCreationThenFadeAround(y_numbers[0]))
        self.play(
            LaggedStartMap(
                FadeInFrom, x_numbers,
                lambda m: (m, UP)
            ),
            self.rods.set_opacity, 0.8,
        )
        self.wait()

    def compare_to_sine_wave(self):
        phi_tracker = ValueTracker(0)
        get_phi = phi_tracker.get_value
        k_tracker = ValueTracker(TAU)
        get_k = k_tracker.get_value
        A_tracker = ValueTracker(1)
        get_A = A_tracker.get_value

        sine_wave = always_redraw(lambda: self.axes.get_graph(
            lambda x: get_A() * np.sin(
                get_k() * x - get_phi()
            ),
            x_min=self.graph_x_min,
            x_max=self.graph_x_max,
        ).color_using_background_image("VerticalTempGradient"))

        self.play(ShowCreation(sine_wave, run_time=3))
        self.wait()
        self.play(A_tracker.set_value, 1.25)
        self.play(A_tracker.set_value, 0.75)
        self.play(phi_tracker.set_value, -PI / 2)
        self.play(k_tracker.set_value, 3 * TAU)
        self.play(k_tracker.set_value, 2 * TAU)
        self.play(
            k_tracker.set_value, PI,
            A_tracker.set_value, 4 / PI,
            run_time=3
        )
        self.wait()

        self.sine_wave = sine_wave

    def sum_of_sine_waves(self):
        curr_sine_wave = self.sine_wave
        axes = self.axes

        sine_graphs = self.get_sine_graphs(axes)
        partial_sums = self.get_partial_sums(axes, sine_graphs)

        curr_partial_sum = partial_sums[0]
        curr_partial_sum.set_color(WHITE)
        self.play(
            FadeOut(curr_sine_wave),
            FadeIn(curr_partial_sum),
            FadeOut(self.rods),
        )
        # Copy-pasting from superclass...in theory,
        # this should be better abstracted, but eh.
        pairs = list(zip(sine_graphs, partial_sums))[1:]
        for sine_graph, partial_sum in pairs:
            anims1 = [
                ShowCreation(sine_graph)
            ]
            partial_sum.set_stroke(BLACK, 4, background=True)
            anims2 = [
                curr_partial_sum.set_stroke,
                {"width": 1, "opacity": 0.25},
                curr_partial_sum.set_stroke,
                {"width": 0, "background": True},
                ReplacementTransform(
                    sine_graph, partial_sum,
                    remover=True
                ),
            ]
            self.play(*anims1)
            self.play(*anims2)
            curr_partial_sum = partial_sum

    #
    def setup_axes(self):
        super().setup_axes()
        self.axes.shift(
            self.axes.c2p(0, 0)[1] * DOWN
        )


class NewSceneName(Scene):
    def construct(self):
        pass
