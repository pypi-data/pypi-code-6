import time
from lightwriter import LightWriter, Frame


def main():
    lw = LightWriter()

    while True:
        # Set all lights to Blue for 1 second.
        frame = Frame()
        frame.set_color_by_name('blue')
        lw.write_frame(frame)
        time.sleep(1)

        # Make a gradient of Blue across the strip and rotate it through.
        frame.gradiant()
        lw.write_frame(frame)
        lw.rotate()

        # Turn off all lights fr 1 second.
        lw.clear()
        time.sleep(1)

        # Set an exact RGB value for 3 seconds.
        frame = Frame()
        frame.set_color_by_rgb(50, 100, 150)
        lw.write_frame(frame)
        time.sleep(3)

        # Set the color of a specific node on the strip (there are 10, 0 indexed).
        frame.set_color_by_name('purple', node=9)
        lw.write_frame()
        time.sleep(3)

        # Shift the purple node back and forth
        lw.back_and_forth()

        # Set a few color groups and rotate them
        frame.set_node_colors_by_name(
            ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        )
        lw.write_frame(frame)
        time.sleep(1)
        lw.rotate()

        # Go Crazy
        lw.random()


if __name__ == '__main__':
    main()
