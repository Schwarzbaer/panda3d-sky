import sys
import datetime

from panda3d.core import AntialiasAttrib

from direct.showbase.ShowBase import ShowBase

import sky


# Parameters for the generation of the stars
SKY_SEED = 1  # Seed for the RNG
NUM_BRIGHTEST_STARS = 1000  # Number of stars at full brightness
NUM_STARS = int(1.0 * 10**6)  # Total number of stars
MAX_LUMINOSITY_OF_DIM_STARS = 1 # 0.66

# Orientation and speed of the sky's rotation
H = 20
P = 10
SKY_ROTATION_PERIOD = 600  # a day's length in seconds


def main():
    ShowBase()
    base.win.set_clear_color(0)
    base.set_frame_rate_meter(True)
    base.accept("escape", sys.exit)

    start_time = datetime.datetime.now()
    star_sphere = sky.stars.create_star_sphere_geom_node(
        NUM_BRIGHTEST_STARS,
        NUM_STARS,
        seed=SKY_SEED,
        max_dim_luminosity=MAX_LUMINOSITY_OF_DIM_STARS,
    )
    finish_time = datetime.datetime.now()
    print((finish_time - start_time).total_seconds())

    star_sphere_node = base.render.attach_new_node(star_sphere)
    star_sphere_node.set_scale(5)
    star_sphere_node.set_hpr(H, P, 0)
    star_sphere_node.set_antialias(AntialiasAttrib.MPoint)
    
    def rotate_sky(task):
        star_sphere_node.set_r(
            star_sphere_node,
            globalClock.dt * 360 / SKY_ROTATION_PERIOD,
        )
        return task.cont

    base.task_mgr.add(rotate_sky)
    base.run()                                        


if __name__ == '__main__':
    main()
