import numpy as np

from constants import ORIGIN
from constants import UP
from utils.space_ops import get_unit_normal
from utils.space_ops import get_norm


def get_3d_vmob_gradient_start_and_end_points(vmob):
    return (
        get_3d_vmob_start_corner(vmob),
        get_3d_vmob_end_corner(vmob),
    )


def get_3d_vmob_start_corner_index(vmob):
    return 0


def get_3d_vmob_end_corner_index(vmob):
    return ((len(vmob.points) - 1) // 6) * 3


def get_3d_vmob_start_corner(vmob):
    if vmob.get_num_points() == 0:
        return np.array(ORIGIN)
    return vmob.points[get_3d_vmob_start_corner_index(vmob)]


def get_3d_vmob_end_corner(vmob):
    if vmob.get_num_points() == 0:
        return np.array(ORIGIN)
    return vmob.points[get_3d_vmob_end_corner_index(vmob)]


def get_3d_vmob_unit_normal(vmob, point_index):
    n_points = vmob.get_num_points()
    if vmob.get_num_points() == 0:
        return np.array(UP)
    i = point_index
    im1 = i - 1 if i > 0 else (n_points - 2)
    ip1 = i + 1 if i < (n_points - 1) else 1
    unit_normal = get_unit_normal(
        vmob.points[ip1] - vmob.points[i],
        vmob.points[im1] - vmob.points[i],
    )
    if get_norm(unit_normal) == 0:
        return np.array(UP)
    return unit_normal


def get_3d_vmob_start_corner_unit_normal(vmob):
    return get_3d_vmob_unit_normal(
        vmob, get_3d_vmob_start_corner_index(vmob)
    )


def get_3d_vmob_end_corner_unit_normal(vmob):
    return get_3d_vmob_unit_normal(
        vmob, get_3d_vmob_end_corner_index(vmob)
    )
