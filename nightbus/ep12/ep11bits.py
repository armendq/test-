from nkit import *


def petal(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(0, 26); c.curve_to(-26, 6, -20, -26, 0, -34); c.curve_to(20, -26, 26, 6, 0, 26); fs(c, WHITE, 4)
    c.new_path(); c.move_to(0, 22); c.line_to(0, -16); rgb(c, hx('BFE3C0')); c.set_line_width(4); c.stroke()
    c.restore()


