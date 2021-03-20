OVERLAP_AREA_THRESHOLD = 0.6
import numpy as np
# 1) Full Overlap
# check box is inside stable box return TRUE/FALSE
# Scenario-5
def check_if_box_inside(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box
    if xmin < xomin < xomax < xmax and ymin < yomin < yomax < ymax:
        return True
    else:
        return False


# check stable box is inside overlap box return TRUE/FALSE
# Scenario-14
def check_if_box_cover(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if xomin < xmin < xmax < xomax and yomin < ymin < ymax < yomax:
        return True
    else:
        return False


# 2) Cross Overlap
# check if boxes are cross overlaped
# returns tuple (TRUE/FALSE,intersection points[ymin, xmin, ymax, xmax])
def check_cross_overlap(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if (
        xmin < xomin < xomax < xmax and yomin < ymin < ymax < yomax
    ):  ## Scenario-15: stable box width big, height small
        return (True, np.array([ymin, xomin, ymax, xomax]))
    elif (
        xomin < xmin < xmax < xomax and ymin < yomin < yomax < ymax
    ):  ## Scenario-16: stable box width small, height big
        return (True, np.array([yomin, xmin, yomax, xmax]))
    else:
        return (False,)


# 3) Partial Overlap
# 3.1) Partial overlap in corners
# Scenario-01 : check overlap in Top Left corner
# returns tuple (TRUE/FALSE,intersection points np.array([ymin, xmin, ymax, xmax]))
def check_topleft_corner_overlap(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if xomin < xmin < xomax < xmax and yomin < ymin < yomax < ymax:
        return (True, np.array([ymin, xmin, yomax, xomax]))
    else:
        return (False,)


# Scenario-02 : check overlap in Bottom Left corner
# returns tuple (TRUE/FALSE,intersection points ->np.array([ymin, xmin, ymax, xmax]))
def check_bottomleft_corner_overlap(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if xomin < xmin < xomax < xmax and ymin < yomin < ymax < yomax:
        return (True, np.array([yomin, xmin, ymax, xomax]))
    else:
        return (False,)


# Scenario-03 : check overlap in Bottom Right corner
# returns tuple (TRUE/FALSE,intersection points ->np.array([ymin, xmin, ymax, xmax]))
def check_bottomright_corner_overlap(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if xmin < xomin < xmax < xomax and ymin < yomin < ymax < yomax:
        return (True, np.array([yomin, xomin, ymax, xmax]))
    else:
        return (False,)


# Scenario-04 : check overlap in Top Right corner
# returns tuple (TRUE/FALSE,intersection points ->np.array([ymin, xmin, ymax, xmax]))
def check_topright_corner_overlap(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if xmin < xomin < xmax < xomax and yomin < ymin < yomax < ymax:
        return (True, np.array([ymin, xomin, yomax, xmax]))
    else:
        return (False,)


# Check All Overlaps
# returns tuple (TRUE/FALSE,Overlap type,intersection points ->np.array([ymin, xmin, ymax, xmax]))
def check_for_partial_overlap(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if (
        xomin < xmin < xomax < xmax and yomin < ymin < yomax < ymax
    ):  # Scenario-01 : check overlap in Top Left corner
        return (True, np.array([ymin, xmin, yomax, xomax]))
    elif (
        xomin < xmin < xomax < xmax and ymin < yomin < ymax < yomax
    ):  # Scenario-02 : check overlap in Bottom Left corner
        return (True, np.array([yomin, xmin, ymax, xomax]))
    elif (
        xmin < xomin < xmax < xomax and ymin < yomin < ymax < yomax
    ):  # Scenario-03 : check overlap in Bottom Right corner
        return (True, np.array([yomin, xomin, ymax, xmax]))
    elif (
        xmin < xomin < xmax < xomax and yomin < ymin < yomax < ymax
    ):  # Scenario-04 : check overlap in Top Right corner
        return (True, np.array([ymin, xomin, yomax, xmax]))
    elif (
        xomin < xmin < xomax < xmax and yomin < ymin < ymax < yomax
    ):  # Scenario-06 : check overlap in Left side Big Box
        return (True, np.array([ymin, xmin, ymax, xomax]))
    elif (
        xomin < xmin < xomax < xmax and ymin < yomin < yomax < ymax
    ):  # Scenario-07 : check overlap in Left side Small Box
        return (True, np.array([yomin, xmin, yomax, xomax]))
    elif (
        xmin < xomin < xomax < xmax and ymin < yomin < ymax < yomax
    ):  # Scenario-08 : check overlap in Bottom side Small Box
        return (True, np.array([yomin, xomin, ymax, xomax]))
    elif (
        xmin < xomin < xomax < xmax and yomin < ymin < yomax < ymax
    ):  # Scenario-09 : check overlap in Bottom side Big Box
        return (True, np.array([ymin, xomin, yomax, xomax]))
    elif (
        xmin < xomin < xmax < xomax and ymin < yomin < yomax < ymax
    ):  # Scenario-10 : check overlap in Right side Small Box
        return (True, np.array([yomin, xomin, yomax, xmax]))
    elif (
        xmin < xomin < xmax < xomax and yomin < ymin < ymax < yomax
    ):  # Scenario-11 : check overlap in Right side Big Box
        return (True, np.array([ymin, xomin, ymax, xmax]))
    elif (
        xomin < xmin < xmax < xomax and yomin < ymin < yomax < ymax
    ):  # Scenario-12 : check overlap in Top side Big Box
        return (True, np.array([ymin, xmin, yomax, xmax]))
    elif (
        xmin < xomin < xomax < xmax and yomin < ymin < yomax < ymax
    ):  # Scenario-13 : check overlap in Top side Small Box
        return (True, np.array([ymin, xomin, yomax, xomax]))
    elif (
        xmin < xomin < xomax < xmax and yomin < ymin < ymax < yomax
    ):  ## Scenario-15: stable box width big, height small
        return (True, np.array([ymin, xomin, ymax, xomax]))
    elif (
        xomin < xmin < xmax < xomax and ymin < yomin < yomax < ymax
    ):  ## Scenario-16: stable box width small, height big
        return (True, np.array([yomin, xmin, yomax, xmax]))
    else:
        return (False,)


# Find box overlap
def is_inside_by_partial_overlap(stable_box, overlap_box):
    overlap_tuple = check_for_partial_overlap(
        stable_box, overlap_box
    )  # returns tuple (TRUE/FALSE,intersection points[ymin, xmin, ymax, xmax])

    if overlap_tuple[0]:
        percentage = overlap_area_percentage(overlap_box, overlap_tuple[1])
        if percentage > OVERLAP_AREA_THRESHOLD:
            return True
        else:
            return False
    else:
        return False


def is_inside_by_full_overlap(stable_box, overlap_box):
    return check_if_box_inside(stable_box, overlap_box) or check_if_box_cover(
        stable_box, overlap_box
    )


def trim_inside_stable_box(stable_box, overlap_box):
    ymin, xmin, ymax, xmax = stable_box
    yomin, xomin, yomax, xomax = overlap_box

    if not (xmin <= xomin):
        xomin = xmin

    if not (xomax <= xmax):
        xomax = xmax

    if not (ymin <= yomin):
        yomin = ymin

    if not (yomax <= ymax):
        yomax = ymax

    # Changed here from np array to list
    return [yomin, xomin, yomax, xomax]


def rotate_image(image, degree):
    return ndimage.rotate(image, degree)


def rotate_box_rightangle_clockwise(box):
    ymin, xmin, ymax, xmax = box

    # Rotate box
    yrmin = xmin
    xrmin = 640 - ymax
    yrmax = xmax
    xrmax = 640 - ymin

    return [yrmin, xrmin, yrmax, xrmax]


def rotate_box_rightangle_clockwise(box):
    ymin, xmin, ymax, xmax = box

    # Rotate box
    yrmin = xmin
    xrmin = 1 - ymax
    yrmax = xmax
    xrmax = 1 - ymin

    return [yrmin, xrmin, yrmax, xrmax]


def change_box_to_int(box):
    return (box * 640).astype(np.int64)


def change_box(box):
    return rotate_box_rightangle_clockwise(change_box_to_int(box))


def area_of_the_box(ymin, xmin, ymax, xmax):
    h = ymax - ymin
    w = xmax - xmin
    return h * w


def area_of_the_box(box):
    ymin, xmin, ymax, xmax = box
    h = ymax - ymin
    w = xmax - xmin
    return h * w


# percentage of overlaping area
def overlap_area_percentage(box_area, overlap_area):
    return overlap_area / box_area


# percentage of overlaping area
def overlap_area_percentage(box, overlap_box):
    box_area = area_of_the_box(box)
    overlap_area = area_of_the_box(overlap_box)
    return overlap_area / box_area
