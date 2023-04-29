import numpy as np



"""
definition of angles:

"""

# angle of cos(theta_i)
def angle_inzidence_tilted(beta, alpha_w):
    """
    input:
        tilt surface: np.array, 
        azimuth surface: np.array,

    output:
        cos(theta_i) - scaleing: float, angle of the inzidence

    assumptions:
        alpha = solar tilt angle
        alpha_s = solar azimuth angle
        beta = surface tilt angle
        alpha_w = surface azimuth angle - 0 in south
    """
    alpha = 30 # solar tilt angle
    alpha_s = 0 # solar azimuth angle

    scaling = np.cos(alpha) * np.cos(alpha_s-alpha_w)*np.sin(beta) + \
        np.sin(alpha) * np.cos(beta)
    
    return scaling

# compute radiation on tilted surface
def radiation_on_tilted_surface(rad_hori, beta, alpha_w):
    """
    input:
        rad_hori: float, horizontal radiation
        beta: float, tilt angle of the roof
        alpha_w: float, azimuth angle of the roof

    output:
        rad: float, radiation on the roof
    """

    # rad = rad_hori * angle of incidence tilt / angle of incidence horizontal
    rad = rad_hori * angle_inzidence_tilted(beta, alpha_w)/angle_inzidence_tilted(0, 0)

    return rad

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
    
def get_radiation_from_angle(rad_hori, direction, tilt):
    """
    input:
        rad_hori: float, horizontal radiation
        direction: float, direction of the roof regards south and north (azimuth angle)
        tilt: float, tilt angle of the roof

    output:
        rad: float, radiation on the roof per square kilometer
    """
    alpha_w = 180 - direction # with 0 in south

    rad = radiation_on_tilted_surface(rad_hori=rad_hori, 
                                      beta = tilt, alpha_w = alpha_w)

    return rad

def get_radiation_from_area(rad_hori, direction, tilt, area):
    """
    input:
        rad_hori: float, horizontal radiation
        direction: float, direction of the roof regards south and north (azimuth angle)
        tilt: float, tilt angle of the roof
        area: float, area of the roof

    output:
        rad: float, radiation on the roof
    """
    rad = get_radiation_from_angle(rad_hori, direction, tilt) * area/(1000**2)

    return rad

# compute normal and areas given type, area, direction, height
def compute_rad_per_roof(type, width, length, rad_hori, direction = None, height = None):
    """
    input:
        type: string, "flat" or "gabled"
        width, length: float, width and length of the roof in square meters
        rad_hori: float, horizontal radiation
        direction: float, direction of the roof regards south and north (azimuth angle)
        height: float, height of the roof - for gabled roofs 

    output:
        rad_roof: float, radiation on the roof
        rad_roof2: float, radiation on the roof - for gabled roofs

    """

    if type == "flat":
        area =  width * length
        tilt = 0
        azimuth = 180 # indepent of direction assumed to be optimal -> 180
        rad_roof = get_radiation_from_area(rad_hori=rad_hori, direction=azimuth, tilt=tilt, area=area)
        return rad_roof, None
    
    # if gabled need scaled area
    elif type == "gabled":
        width = min(length,width) # assume width is the smaller one
        scaled_area = height_and_area_to_scaled_area(height, width, length)
        # normal_vector1 = angles_to_normal(direction)
        # normal_vector2 = angles_to_normal(direction + 180)
        azimuth1 = direction
        tilt = height_and_lw_to_tilt_angle(hieght=height, width=width)
        #normal_vector1 = np.array([np.cos(azimuth1)*np.sin(tilt), np.sin(azimuth1)*np.sin(tilt), np.cos(tilt)])
        rad_roof1 = get_radiation_from_area(rad_hori=rad_hori, direction=direction, tilt=tilt, area=scaled_area)
        rad_roof2 = get_radiation_from_area(rad_hori=rad_hori, direction=direction+180, tilt=tilt, area=scaled_area)
        return rad_roof1, rad_roof2
    
    else:

        assert("not implemented yet")

        return None, None
