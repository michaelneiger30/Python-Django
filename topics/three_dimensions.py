
from helpers import *

from mobject.vectorized_mobject import VGroup, VMobject, VectorizedPoint
from topics.geometry import Square, Line
from scene import Scene
from camera import Camera
from animation.continual_animation import AmbientRotation
from animation.transform import ApplyMethod

class CameraWithPerspective(Camera):
    CONFIG = {
        "camera_distance" : 20,
    }
    def points_to_pixel_coords(self, points):
        distance_ratios = np.divide(
            self.camera_distance,
            self.camera_distance - points[:,2]
        )
        scale_factors = interpolate(0, 1, distance_ratios)
        adjusted_points = np.array(points)
        for i in 0, 1:
            adjusted_points[:,i] *= scale_factors

        return Camera.points_to_pixel_coords(self, adjusted_points)

class ThreeDCamera(CameraWithPerspective):
    CONFIG = {
        "sun_vect" : 5*UP+LEFT,
        "shading_factor" : 0.5,
        "distance" : 5,
        "phi" : 0, #Angle off z axis
        "theta" : -np.pi/2, #Rotation about z axis
    }
    def __init__(self, *args, **kwargs):
        Camera.__init__(self, *args, **kwargs)
        self.unit_sun_vect = self.sun_vect/np.linalg.norm(self.sun_vect)
        self.position_mobject = VectorizedPoint()
        self.set_position(self.phi, self.theta, self.distance)

    def get_color(self, method):
        color = method()
        vmobject = method.im_self
        if should_shade_in_3d(vmobject):
            return Color(rgb = self.get_shaded_rgb(
                color_to_rgb(color),
                normal_vect = self.get_unit_normal_vect(vmobject)
            ))
        else:
            return color

    def get_stroke_color(self, vmobject):
        return self.get_color(vmobject.get_stroke_color)

    def get_fill_color(self, vmobject):
        return self.get_color(vmobject.get_fill_color)

    def get_shaded_rgb(self, rgb, normal_vect):
        brightness = np.dot(normal_vect, self.unit_sun_vect)**2
        if brightness > 0:
            alpha = self.shading_factor*brightness
            return interpolate(rgb, np.ones(3), alpha)
        else:
            alpha = -self.shading_factor*brightness
            return interpolate(rgb, np.zeros(3), alpha)

    def get_unit_normal_vect(self, vmobject):
        anchors = vmobject.get_anchors()
        if len(anchors) < 3:
            return OUT
        normal = np.cross(anchors[1]-anchors[0], anchors[2]-anchors[1])
        if normal[2] < 0:
            normal = -normal
        length = np.linalg.norm(normal)
        if length == 0:
            return OUT
        return normal/length

    def display_multiple_vectorized_mobjects(self, vmobjects):
        def z_cmp(*vmobs):
            #Compare to three dimensional mobjects based on their
            #z value, otherwise don't compare.
            three_d_status = map(should_shade_in_3d, vmobs)
            has_points = [vm.get_num_points() > 0 for vm in vmobs]
            if all(three_d_status) and all(has_points):
                cmp_vect = self.get_unit_normal_vect(vmobs[1])
                return cmp(*[
                    np.dot(vm.get_center(), cmp_vect)
                    for vm in vmobs
                ])
            else:
                return 0
        Camera.display_multiple_vectorized_mobjects(
            self, sorted(vmobjects, cmp = z_cmp)
        )

    def get_position(self):
        return self.position_mobject.points[0]

    def get_phi(self):
        x, y, z = self.get_position()
        return angle_of_vector([z, np.sqrt(x**2 + y**2)])

    def get_theta(self):
        x, y, z = self.get_position()
        return angle_of_vector([x, y])

    def get_distance(self):
        return np.linalg.norm(self.get_position())

    def spherical_coords_to_point(self, phi, theta, distance):
        phi = phi or self.get_phi()
        theta = theta or self.get_theta()
        distance = distance or self.get_distance()
        return distance*np.array([
            np.sin(phi)*np.cos(theta),
            np.sin(phi)*np.sin(theta),
            np.cos(phi)
        ])

    def set_position(self, phi = None, theta = None, distance = None):
        point = self.spherical_coords_to_point(phi, theta, distance)
        self.position_mobject.move_to(point)
        self.phi = self.get_phi()
        self.theta = self.get_theta()
        self.distance = self.get_distance()

    def get_view_transformation_matrix(self):
        return np.dot(
            rotation_matrix(self.get_phi(), LEFT),
            rotation_about_z(-self.get_theta() - np.pi/2),
        )

    def points_to_pixel_coords(self, points):
        matrix = self.get_view_transformation_matrix()
        new_points = np.dot(points, matrix.T)
        return Camera.points_to_pixel_coords(self, new_points)

class ThreeDScene(Scene):
    CONFIG = {
        "camera_class" : ThreeDCamera,
    }

    def set_camera_position(self, phi = None, theta = None, distance = None):
        self.camera.set_position(phi, theta, distance)

    def begin_ambient_camera_rotation(self, rate = 0.01):
        self.ambient_camera_rotation = AmbientRotation(
            self.camera.position_mobject,
            axis = OUT, 
            rate = rate
        )
        self.add(self.ambient_camera_rotation)

    def move_camera(
        self, 
        phi = None, theta = None, distance = None,
        added_anims = [],
        **kwargs
        ):
        target_point = self.camera.spherical_coords_to_point(phi, theta, distance)
        movement = ApplyMethod(
            self.camera.position_mobject.move_to,
            target_point,
            **kwargs
        )
        if hasattr(self, "ambient_camera_rotation"):
            self.remove(self.ambient_camera_rotation)
        self.play(movement, *added_anims)
        if hasattr(self, "ambient_camera_rotation"):
            self.add(self.ambient_camera_rotation)

    def separate_moving_and_static_mobjects(self, *animations):
        moving, static = Scene.separate_moving_and_static_mobjects(self, *animations)
        if self.camera.position_mobject in moving:
            return moving + static, []
        return moving, static

##############

def should_shade_in_3d(mobject):
    return hasattr(mobject, "shade_in_3d")

def shade_in_3d(mobject):
    for submob in mobject.submobject_family():
        submob.shade_in_3d = True

class ThreeDMobject(VMobject):
    def __init__(self, *args, **kwargs):
        VMobject.__init__(self, *args, **kwargs)
        shade_in_3d(self)

class Cube(ThreeDMobject):
    CONFIG = {
        "fill_opacity" : 0.75,
        "fill_color" : BLUE,
        "stroke_width" : 0,
        "propogate_style_to_family" : True,
        "side_length" : 2,
    }
    def generate_points(self):
        for vect in IN, OUT, LEFT, RIGHT, UP, DOWN:
            face = Square(side_length = self.side_length)
            face.shift(self.side_length*OUT/2.0)
            face.apply_function(lambda p : np.dot(p, z_to_vector(vect).T))

            self.add(face)

class Prism(Cube):
    CONFIG = {
        "dimensions" : [3, 2, 1]
    }
    def generate_points(self):
        Cube.generate_points(self)
        for dim, value in enumerate(self.dimensions):
            self.rescale_to_fit(value, dim, stretch = True)


























