import math

def calc_time_julian_cent(jd):
    t = (jd - 2451545.0)/36525.0
    return t


def calc_JD_from_julian_cent(t):
    jd = t*36525.0 + 2451545.0
    return jd


def is_leapyear(yr):
    return (yr % 4 == 0 and yr % 100 != 0) or yr % 400 == 0

#should probably check this lmao
def calc_doy_from_jd(jd):
    z = math.floor(jd+0.5)
    f = (jd + 0.5) - z
    if z < 2299161:
        a = z
    else:
        alpha = math.floor((z - 1867216.25) / 36524.25);
        a = z + 1 + alpha - math.floor(alpha/4)
    b = a + 1524
    c = math.floor((b - 122.1)/265.25)
    d = math.floor(365.25 * c)
    e = math.floor((b - d)/30.6001)
    day = b - d- math.floor(30.6001 * e) + f
    if e < 14:
        month = e - 1
    else:
        month = e - 13
    if month > 2:
        year = c - 4716
    else:
        year = c - 4715
    if is_leapyear(year):
        k = 1
    else:
        k = 2
    doy = math.floor((275 * month)/9) - k * math.floor((month + 9)/12) + day - 30
    return doy

def rad_to_deg(angleRad):
    return (180.0 * angleRad)/math.pi

def deg_to_rad(angleDeg):
    return (math.pi * angleDeg)/180.0


def calc_geom_mean_long_sun(t):
    l0 = 280.46646 + t * (36000.76983 + t * 0.0003032)
    while l0 > 360.0:
        l0 -= 360.0
    while l0 < 0.0:
        l0 += 360.0
    #in degrees
    return l0

def calc_geom_mean_anomaly_sun(t):
    m = 357.52911 + t * (35999.05029 - 0.0001537 * t)
    #in degrees
    return m

def calc_eccentricity_earth_orbit(t):
    e = 0.016708634 - t * (0.000042037 + 0.0000001267 * t)
    #unitless
    return e

def calc_sun_eq_of_center(t):
    m = calc_geom_mean_anomaly_sun(t)
    mrad = deg_to_rad(m)
    sinm = math.sin(mrad)
    sin2m = math.sin(mrad+mrad)
    sin3m = math.sin(mrad+mrad+mrad)
    c = sinm * (1.914602 - t * (0.004817 + 0.000014 * t)) + sin2m * (0.019993 - 0.000101 * t) + sin3m * 0.000289
    #in degrees
    return c


def calc_sun_true_long(t):
    l0 = calc_geom_mean_long_sun(t)
    c = calc_sun_eq_of_center(t)
    o = l0 + c
    #in degrees
    return o

def calc_sun_true_anomaly(t):
    m = calc_geom_mean_anomaly_sun(t)
    c = calc_sun_eq_of_center(t)
    v = m + c
    #in degrees
    return v

def calc_sun_rad_vector(t):
    v = calc_sun_true_anomaly(t)
    e = calc_eccentricity_earth_orbit(t)
    r = 1.000001018 * (1 - e * e) / (1 + e * math.cos(deg_to_rad(v)))
    # in AUs
    return r

def calc_sun_apparent_long(t):
    o = calc_sun_true_long(t)
    omega = 125.04 - 1934.136 * t
    val = o - 0.00569 - 0.00478 * math.sin(deg_to_rad(omega))
    #in degrees
    return val

def calc_mean_obliquity_of_ecliptic(t):
    seconds = 21.448 - t * (46.8150 + t*(0.00059 - t*(0.001813)))
    e0 = 23.0 + (26.0 + (seconds/60.0))/60.0
    #in degrees
    return e0

def calc_obliquity_correction(t):
    e0 = calc_mean_obliquity_of_ecliptic(t)
    omega = 125.04 - 1934.136 * t
    e = e0 + 0.00256 * math.cos(deg_to_rad(omega))
    #in degrees
    return e

def calc_sun_rt_ascension(t):
    e = calc_obliquity_correction(t)
    val = calc_sun_apparent_long(t)
    tananum = (math.cos(deg_to_rad(e)) * math.sin(deg_to_rad(val)))
    tanadenom = (math.cos(deg_to_rad(val)))
    alpha = rad_to_deg(math.atan2(tananum, tanadenom))
    #in degrees
    return alpha

def calc_sun_declination(t):
    e = calc_obliquity_correction(t)
    val = calc_sun_apparent_long(t)
    sint = math.sin(deg_to_rad(e)) * math.sin(deg_to_rad(val))
    theta = rad_to_deg(math.asin(sint))
    #in degrees
    return theta

def calc_equation_of_time(t):
    epsilon = calc_obliquity_correction(t)
    l0 = calc_geom_mean_long_sun(t)
    e = calc_eccentricity_earth_orbit(t)
    m = calc_geom_mean_anomaly_sun(t)

    y = math.tan(deg_to_rad(epsilon)/2.0)
    y *= y

    sin2l0 = math.sin(2.0 * deg_to_rad(l0))
    sinm = math.sin(deg_to_rad(m))
    cose2l0 = math.cos(2.0 * deg_to_rad(l0))
    sin4l0 = math.sin(4.0 * deg_to_rad(l0))
    sin2m = math.sin(2.0 * deg_to_rad(m))

    e_time = y * sin2l0 - 2.0 * e * sinm + 4.0 * e * y * sinm * cos2l0 - 0.5 * y * y * sin4l0 - 1.25 * e * e * sin2m
    #in minutes of time
    return rad_to_deg(e_time) * 4.0

def calc_hour_angle_sunrise(lat, solar_dec):
    lat_rad = deg_to_rad(lat)
    sd_rad = deg_to_rad(solar_dec)
    HA_arg = (math.cos(deg_to_rad(90.833))/(math.cos(lat_rad)*math.cos(sd_rad))-math.tan(lat_rad) * math.tan(sd_rad))
    HA = math.acos(HA_arg)
    #in radians (for sunset, use -HA
    return HA

def is_number(input_val):
    one_decimal = False
    input_str = "" + str(input_val)
    for i in range(0, len(input_str)):
        one_char = input_str[i]
        if i == 0 and (one_char == "-" or one_char == "+"):
            continue
        if one_char == "." and one_decimal is False:
            one_decimal = True
            continue
        if one_char < "0" or one_char > "9":
            return False
    return True

def zero_pad(n, digits):
    diff = digits - len(str(n))
    pad = '0' * diff
    n = pad + str(n)
    return n

month_dict = {
    "January" : {"num_days": 31, "abbr":"Jan"},
    "February": {"num_days": 28, "abbr": "Jan"},
    "March": {"num_days": 31, "abbr": "Jan"},
    "April": {"num_days": 30, "abbr": "Jan"},
    "May": {"num_days": 31, "abbr": "Jan"},
    "June": {"num_days": 30, "abbr": "Jan"},
    "July": {"num_days": 31, "abbr": "Jan"},
    "August": {"num_days": 31, "abbr": "Jan"},
    "September": {"num_days": 30, "abbr": "Jan"},
    "October": {"num_days": 31, "abbr": "Jan"},
    "November": {"num_days": 30, "abbr": "Jan"},
    "December": {"num_days": 31, "abbr": "Jan"},

}

def clean_input(val, intgr, pad, min, max, default):
    if intgr:
        val = math.floor(val)
    if val < min:
        val = min
    elif val > max:
        val = max
    elif math.isnan(val):
        val = default
    if pad and intgr:
        val = zero_pad(val, 2)
    return val


def get_JD(month, day, year):
    year = clean_input(year, 5, True, 0, -2000, 3000, 2009)
    if is_leapyear(year) and month == 2:
        if day > 29:
            day = 29
        else:
            if day > month_dict[month]["num_days"]:
                day = month_dict[month_dict]["num_days"]
    if month <= 2:
        year -= 1
        month += 12

    a = math.floor(year/100)
    b = 2 - a + math.floor(a/4)
    JD = math.floor(365.25 * (year + 4716)) + math.floor(30.6001 * (month + 1)) + day + b - 1524.5
    return JD

def clean_input(val, intgr, pad, min, max, default):


def get_time_local(hour, minute, second, am_or_pm, daylight_savings):
    hr = clean_input(hour, True, True, 0, 23, 12)
    mn = clean_input(minute, True, True, 0, 59, 0)
    sec = clean_input(second, True, 0, 59, 0)
    if am_or_pm == "pm" and hr < 12:
        hr += 12
    if daylight_savings:
        hr -= 1
    mn = hr * mn + sec/60.0
    return mn

def calc_az_el(T, localtime, latitude, longitude, zone):
    eq_time = calc_equation_of_time(T)
    theta = calc_sun_declination(T)
    solar_time_fix = eq_time + 4.0 * longitude - 60.0 * zone
    earth_rad_vec = calc_sun_rad_vector(T)
    true_solar_time = localtime + solar_time_fix
    while true_solar_time > 1440:
        true_solar_time -= 1440
    hour_angle = true_solar_time / 4.0 - 180.0
    if hour_angle < -180:
        hour_angle += 360.0
    ha_rad = deg_to_rad(hour_angle)
    csz = math.sin(deg_to_rad(latitude)) * math.sin(deg_to_rad(theta)) + math.cos(deg_to_rad(latitude)) * math.cos(deg_to_rad(theta)) * math.cos(ha_rad)
    if csz > 1.0:
        csz = 1.0
    elif csz < -1.0:
        csz = -1.0
    zenith = rad_to_deg(math.acos(csz))
    az_denom = (math.cos(deg_to_rad(latitude)) * math.sin(deg_to_rad(zenith)) )
    if math.abs(az_denom) > 0.001:
        az_rad = ((math.sin(deg_to_rad(latitude)) * math.cos(deg_to_rad(zenith))) - math.sin(deg_to_rad(theta))) / az_denom
        if math.abs(az_rad) > 1.0:
            if az_rad < 0:
                az_rad  = -1.0
            else:
                az_rad = 1.0
        azimuth = 180.0 - rad_to_deg(math.acos(az_rad))
        if hour_angle > 0.0:
            azimuth *= -1
    else:
        if latitude > 0.0:
            azimuth = 180.0
        else:
            azimuth = 0.0
    if azimuth < 0.0:
        azimuth += 360.0

    #removed atmospheric refraction correction
    return azimuth

def calc_sunrise_set_UTC(rise, JD, latitude, longitude):
    t = calc_time_julian_cent(JD)
    eq_time = calc_equation_of_time(t)
    solar_dec = calc_sun_declination(t)
    hour_angle = calc_hour_angle_sunrise(latitude, solar_dec)
    if rise is False:
        hour_angle *= -1
    delta = longitude + rad_to_deg(hour_angle)
    #in minutes
    time_UTC = 720 - (4.0 * delta) - eq_time
    return time_UTC


def calc_sunrise_set (rise, JD, latitude, longitude, timezone, dst):
    #rise = 1 for sunrise, 0 for sunset
    timeUTC = calc_sunrise_set_UTC(rise, JD, latitude, longitude)
    new_time_UTC = calc_sunrise_set_UTC(rise, JD + timeUTC/1440.0, latitude, longitude)
    if is_number(new_time_UTC):
        time_local = new_time_UTC + (timezone*60.0)






def calculate(month, day, year, hour, minute, second, lat, long, am_or_pm, daylight_savings):
    jday = get_JD(month, day, year)
    tl = get_time_local(hour, minute, second, am_or_pm, daylight_savings)


















