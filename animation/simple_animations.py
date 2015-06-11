import numpy as np
import itertools as it

from animation import Animation
from constants import *
from helpers import *

class Rotating(Animation):
    def __init__(self,
                 mobject,
                 axis = None,
                 axes = [[0, 0, 1], [0, 1, 0]], 
                 radians = 2 * np.pi,
                 run_time = 20.0,
                 alpha_func = None,
                 *args, **kwargs):
        Animation.__init__(
            self, mobject,
            run_time = run_time,
            alpha_func = alpha_func,
            *args, **kwargs
        )
        self.axes = [axis] if axis else axes
        self.radians = radians

    def update_mobject(self, alpha):
        self.mobject.points = self.starting_mobject.points
        for axis in self.axes:
            self.mobject.rotate(
                self.radians * alpha,
                axis
            )

class RotationAsTransform(Rotating):
    def __init__(self, mobject, radians, axis = (0, 0, 1), axes = None,
                 run_time = DEFAULT_ANIMATION_RUN_TIME,
                 alpha_func = high_inflection_0_to_1,
                 *args, **kwargs):
        Rotating.__init__(
            self,
            mobject,
            axis = axis,
            axes = axes,
            run_time = run_time,
            radians = radians,
            alpha_func = alpha_func,
        )

class FadeOut(Animation):
    def update_mobject(self, alpha):
        self.mobject.rgbs = self.starting_mobject.rgbs * (1 - alpha)

class FadeIn(Animation):
    def update_mobject(self, alpha):
        self.mobject.rgbs = self.starting_mobject.rgbs * alpha
        if self.mobject.points.shape != self.starting_mobject.points.shape:
            self.mobject.points = self.starting_mobject.points
            #TODO, Why do you need to do this? Shouldn't points always align?

class ShowCreation(Animation):
    def update_mobject(self, alpha):
        #TODO, shoudl I make this more efficient?
        new_num_points = int(alpha * self.starting_mobject.points.shape[0])
        for attr in ["points", "rgbs"]:
            setattr(
                self.mobject, 
                attr, 
                getattr(self.starting_mobject, attr)[:new_num_points, :]
            )

class Flash(Animation):
    def __init__(self, mobject, color = "white", slow_factor = 0.01,
                 run_time = 0.1, alpha_func = None,
                 *args, **kwargs):
        Animation.__init__(self, mobject, run_time = run_time, 
                           alpha_func = alpha_func,
                           *args, **kwargs)
        self.intermediate = Mobject(color = color)
        self.intermediate.add_points([
            point + (x, y, 0)
            for point in self.mobject.points
            for x in [-1, 1]
            for y in [-1, 1]
        ])
        self.reference_mobjects.append(self.intermediate)
        self.slow_factor = slow_factor

    def update_mobject(self, alpha):
        #Makes alpha go from 0 to slow_factor to 0 instead of 0 to 1
        alpha = self.slow_factor * (1.0 - 4 * (alpha - 0.5)**2)
        Mobject.interpolate(
            self.starting_mobject, 
            self.intermediate, 
            self.mobject, 
            alpha
        )

class Homotopy(Animation):
    def __init__(self, homotopy, *args, **kwargs):
        """
        Homotopy a function from (x, y, z, t) to (x', y', z')
        """
        self.homotopy = homotopy
        Animation.__init__(self, *args, **kwargs)

    def update_mobject(self, alpha):
        self.mobject.points = np.array([
            self.homotopy((x, y, z, alpha))
            for x, y, z in self.starting_mobject.points
        ])

class ComplexHomotopy(Homotopy):
    def __init__(self, complex_homotopy, *args, **kwargs):
        """
        Complex Hootopy a function (z, t) to z'
        """
        def homotopy((x, y, z, t)):
            c = complex_homotopy((complex(x, y), t))
            return (c.real, c.imag, z)
        if len(args) > 0:
            args = list(args)
            mobject = args.pop(0)
        elif "mobject" in kwargs:
            mobject = kwargs["mobject"]
        else:
            mobject = Grid()
        Homotopy.__init__(self, homotopy, mobject, *args, **kwargs)
        self.name = "ComplexHomotopy" + \
            to_cammel_case(complex_homotopy.__name__)







