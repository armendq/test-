from nkit import *


def bow10(c, x, y, s, rot=0.0, col=CORAL):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for sg in (-1, 1):
        c.new_path(); c.move_to(sg * 4, 0); c.line_to(sg * 30, -17); c.line_to(sg * 30, 17); c.close_path(); fs(c, col, 4)
    c.new_path(); c.arc(0, 0, 7, 0, 2 * math.pi); fs(c, GOLD, 3)
    c.restore()


