import numpy as np



"""
definition of angles:

"""

# compute tilt angle from height and l, w
def height_and_lw_to_tilt_angle(height, width):
    """
    input:
        height: float, height of the roof
        l: float, length of the roof
        w: float, width of the roof

    output:
        angle: float, tilt angle of the roof

    assumption:
        smaller of l,w is the width of the roof
    """
    width_angle = width/2 # get the with and compute the middle point
    angle = np.arctan(width_angle/height)
    return angle


# angle  normal
def angles_to_normal(angle):
    pass


# height and area to scaled area
def height_and_area_to_scaled_area(height, width, length):
    """
    input:
        height: float, height of the roof - 0 if flat?
        width: float, width of the roof
        length: float, length of the roof

    output:
        scaled_area: float, scaled area of the roof

    """
    width = width/2 # get the with and compute the middle point
    scaled_width = np.sqrt(width**2 + height**2)
    scaled_area = scaled_width * length
    return scaled_area
    
# compute normal and areas given type, area, direction, height
def compute_normal_and_areas(type, width, length, direction = None, height = None):
    """
    input:
        type: string, "flat" or "gabled"
        area: float, area of the roof (from top)
        direction: float, direction of the roof regards south and north (azimuth angle)
        height: float, height of the roof - for gabled roofs 

    output:
        n1: np.array, normal vector of the roof or tilt and azimuth angle
        area1: float, area of the roof according to normal1
        n2: np.array, normal vector of the roof
        area2: float, area of the roof according to normal2

        or:
        tilt: float, tilt angle of the roof - if gabled for both sides the same
        azimuth1: float, azimuth angle of the roof
        azimuth2: float, azimuth angle of the roof - if gabled roof
        area: float, area of the roof according to normal1

    """

    if type == "flat":
        area =  width * length
        tilt = 0
        azimuth = 180 # indepent of direction assumed to be optimal -> 180
        return tilt, azimuth, None, area
    
    # if gabled need scaled area
    elif type == "gabled":
        width = min(length,width) # assume width is the smaller one
        scaled_area = height_and_area_to_scaled_area(height, width, length)
        # normal_vector1 = angles_to_normal(direction)
        # normal_vector2 = angles_to_normal(direction + 180)
        azimuth1 = direction
        tilt = height_and_lw_to_tilt_angle(hieght=height, width=width)
        azimuth2 = direction + 180
        #normal_vector1 = np.array([np.cos(azimuth1)*np.sin(tilt), np.sin(azimuth1)*np.sin(tilt), np.cos(tilt)])
        return tilt, azimuth1, azimuth2, scaled_area
    
    else:

        assert("not implemented yet")

        return None, None, None, None