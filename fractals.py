import numpy as np
import PIL
import math

from numba import jit, prange

class Fractal:
    def __init__(self, func, xrange=(-2.0, 2.0), yrange=(-2.0, 2.0), max_iterations=1000, power=2, img=None):
        self.func = func
        self.xrange = xrange
        self.yrange = yrange
        self.max_iterations = max_iterations
        self.power = power
        self.img = img

@jit(nopython=False, parallel=True, fastmath=True)
def multibrot(width, height, max_iterations, mouse, rmin, rmax, imin, imax, power):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    scaleX = (rmax - rmin) / width
    scaleY = (imax - imin) / height

    if len(mouse) != 2:
        rmin2 = mouse[0]*scaleX + rmin
        rmax2 = mouse[2]*scaleX + rmin
        imax2 = imax - mouse[1]*scaleY
        imin2 = imax - mouse[3]*scaleY

        neww = (rmax2 - rmin2)
        newh = (imax2 - imin2)
        oldw = (rmax - rmin)
        oldh = (imax - imin)

        rw = oldw / neww
        rh = oldh / newh

        r_range = (rmax - rmin) / rw
        i_range = (imax - imin) / rh

        mx = rmax2 - ((rmax2 - rmin2) / 2)
        my = imax2 - ((imax2 - imin2) / 2)
        rmin = mx - r_range/2
        rmax = mx + r_range/2
        imin = my - i_range/2
        imax = my + i_range/2
        scaleX = (rmax - rmin) / width
        scaleY = (imax - imin) / height


    for y in np.arange(height):
        for x in np.arange(width):
            cReal = rmin + x*scaleX
            cIm = imax - y*scaleY

            zr = 0
            zi = 0
            n = 0
            while -2 < zr < 2 and -2 < zi < 2 and n < max_iterations:
                if (power == 2):
                    temp = zr * zr - zi * zi + cReal
                    zi = 2.0 * zr * zi + cIm
                    zr = temp
                elif (power == 3):
                    temp = zr**3.0 - 3.0*zr*(zi*zi) + cReal
                    zi = 3.0*(zr*zr)*zi - zi**3.0 + cIm
                    zr = temp
                elif (power == 5):
                    temp = zr**5 - 10*(zr**3)*(zi*zi) + 5*zr*(zi**4) + cReal
                    zi = 5*(zr**4)*zi - 10*(zr*zr)*(zi**3) + (zi**5) + cIm
                    zr = temp
                elif (power > 0):
                    xy = np.power(zr*zr + zi*zi, power/2)
                    angle = power*np.arctan2(zi, zr)
                    temp = xy*np.cos(angle) + cReal
                    zi = xy*np.sin(angle) + cIm
                    zr = temp

                n += 1

            n = max_iterations if n >= max_iterations else n + 1 - np.log(np.log2(np.sqrt(zr * zr + zi * zi)))
            hue = int(255 * n / max_iterations)
            sat = 255
            val = 255 if n < max_iterations else 0
            image[int(y), (int(x))] = (hue, sat, val)

    return image, (rmin, rmax), (imin, imax)

@jit(nopython=False, parallel=True, fastmath=True)
def julia(cx, cy, width, height, max_iterations, mouse, rmin, rmax, imin, imax, power):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    scaleX = (rmax - rmin) / width
    scaleY = (imax - imin) / height

    if cx < 0 and cy < 0:
        cReal = -0.5478515625
        cIm = -0.5390625
    else:
        cIm = imax - cy*scaleY
        cReal = cx*scaleX + rmin

    if len(mouse) != 2:
        rmin2 = mouse[0]*scaleX + rmin
        rmax2 = mouse[2]*scaleX + rmin
        imax2 = imax - mouse[1]*scaleY
        imin2 = imax - mouse[3]*scaleY

        neww = (rmax2 - rmin2)
        newh = (imax2 - imin2)

        oldw = (rmax - rmin)
        oldh = (imax - imin)

        rw = oldw / neww
        rh = oldh / newh

        r_range = (rmax - rmin) / rw
        i_range = (imax - imin) / rh

        mx = rmax2 - ((rmax2 - rmin2) / 2)
        my = imax2 - ((imax2 - imin2) / 2)
        rmin = mx - r_range/2
        rmax = mx + r_range/2
        imin = my - i_range/2
        imax = my + i_range/2
        scaleX = (rmax - rmin) / width
        scaleY = (imax - imin) / height

    for y in np.arange(height):
        for x in np.arange(width):
            zr = rmin + x*scaleX
            zi = imax - y*scaleY
            n = 0
            while -2 < zr < 2 and -2 < zi < 2 and n < max_iterations:
                '''temp = zi
                zi = 2.0 * zr * zi + cIm
                zr = zr * zr - temp * temp + cReal'''
                temp = zr * zr - zi * zi + cReal
                zi = 2.0 * zr * zi + cIm
                zr = temp
                n += 1

            n = max_iterations if n >= max_iterations else n + 1 - np.log(np.log2(np.sqrt(zr * zr + zi * zi)))
            hue = int(255 * n / max_iterations)
            sat = 255
            val = 255 if n < max_iterations else 0
            image[y, x] = (hue, sat, val)

    return image, (rmin, rmax), (imin, imax)

@jit(nopython=False, parallel=True, fastmath=True)
def burning_ship(width, height, max_iterations, mouse, rmin, rmax, imin, imax, power):
    image = np.zeros((height, width, 3), dtype=np.uint8)
    scaleX = (rmax - rmin) / width
    scaleY = (imax - imin) / height

    if len(mouse) != 2:
        rmin2 = mouse[0]*scaleX + rmin
        rmax2 = mouse[2]*scaleX + rmin
        imax2 = imax - mouse[1]*scaleY
        imin2 = imax - mouse[3]*scaleY

        neww = (rmax2 - rmin2)
        newh = (imax2 - imin2)
        oldw = (rmax - rmin)
        oldh = (imax - imin)

        rw = oldw / neww
        rh = oldh / newh
        #z = 50
        r_range = (rmax - rmin) / rw
        i_range = (imax - imin) / rh

        mx = rmax2 - ((rmax2 - rmin2) / 2)
        my = imax2 - ((imax2 - imin2) / 2)
        rmin = mx - r_range/2
        rmax = mx + r_range/2
        imin = my - i_range/2
        imax = my + i_range/2
        scaleX = (rmax - rmin) / width
        scaleY = (imax - imin) / height


    for y in np.arange(height):
        for x in np.arange(width):
            cReal = rmin + x*scaleX
            cIm = imax - y*scaleY

            zr = 0
            zi = 0
            n = 0
            while -2 < zr < 2 and -2 < zi < 2 and n < max_iterations:
                temp = zi
                zi = abs(2.0 * zr * zi + cIm)
                zr = abs(zr * zr - temp * temp + cReal)
                n += 1

            n = max_iterations if n >= max_iterations else n + 1 - np.log(np.log2(np.absolute(zr * zr + zi * zi)))
            hue = int(255 * n / max_iterations)
            sat = 255
            val = 255 if n < max_iterations else 0
            image[y, x] = (hue, sat, val)

    return image, (rmin, rmax), (imin, imax)
