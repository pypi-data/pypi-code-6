import queue
import tkinter
import logging
import multiprocessing
import random
import threading
import time
log = multiprocessing.log_to_stderr()
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter("[%(processName)s %(threadName)s] %(message)s")
)
#log.handlers = (handler,)
# #log.setLevel(level=99)


# FAKED_CPU_LOAD = 10
# FAKED_CPU_LOAD = 100
FAKED_CPU_LOAD = 1000
# FAKED_CPU_LOAD = 10000


class FakeCPU(threading.Thread):
    def __init__(self, display_queue):
        super(FakeCPU, self).__init__(name="FakeCPU")
        #log.critical("FakeCPU thread init")
        self.display_queue = display_queue

    def run(self):
        #log.critical("FakeCPU thread run")
        address = 0x0400
        cpu_cycles = 0
        op_address = 0
        while True:
            op_address += 1
            for __ in range(FAKED_CPU_LOAD):
                cpu_cycles += 1

            if address > 0x0600:
                op_address = 0
                address = 0x0400

            value = random.randrange(0, 255, 8)

            data = (cpu_cycles, op_address, address, value)
            #log.critical("new display data: %s", repr(data))
            try:
                self.display_queue.put(data, block=False)
            except queue.Full:
                #                 log.critical("display_queue is full -> put with wait")
                self.display_queue.put(data, block=True)
            address += 1


class MC6847_TextModeCanvas(object):
    """
    The GUI stuff
    """
    CACHE = {}
    def __init__(self, root):
        self.rows = 32
        self.columns = 16

        self.width = 12
        self.height = 12

        self.total_width = self.width * self.rows
        self.total_height = self.height * self.columns

        self.canvas_image_id_map = {}
        self.canvas = tkinter.Canvas(root,
            width=self.total_width,
            height=self.total_height,
            bd=0,  # Border
            bg="#ff0000",
        )

        self.img_count = 0
        self.next_update = time.time() + 1

    def write_byte(self, cpu_cycles, op_address, address, value):
        self.img_count += 1
        #log.critical("create_image $%04x $%02x", address, value)
        try:
            img = self.CACHE[value]
        except KeyError:
            img = tkinter.PhotoImage(
                width=self.width,
                height=self.height
            )
            for y in range(self.width):
                for x in range(self.height):
                    color = "#%02x%02x%02x" % (value, value, value)
    #                 #log.critical("%s %i x %i", color, x, y)
                    img.put(color, (x, y))
            self.CACHE[value] = img

        position = address - 0x400
        column, row = divmod(position, self.rows)
        x = self.width * row
        y = self.height * column

        try:
            existing_image_id = self.canvas_image_id_map[(x, y)]
        except KeyError:
            image_id = self.canvas.create_image(x, y,
                image=img,
                state="normal",
                anchor=tkinter.NW  # NW == NorthWest
            )
            self.canvas_image_id_map[(x, y)] = image_id
        else:
            self.canvas.itemconfigure(existing_image_id, image=img)

        if time.time() > self.next_update:
            log.critical("%i images/s (Cache size: %i)", self.img_count, len(self.CACHE))

            self.img_count = 0
            self.next_update = time.time() + 1


class DragonTkinterGUI(object):

    def __init__(self, display_queue):
        self.display_queue = display_queue

        self.root = tkinter.Tk()
        self.root.title("example")

        self.display = MC6847_TextModeCanvas(self.root)
        self.display.canvas.grid(row=0, column=0)

        self.status_widget = tkinter.Label(self.root, text="Press any key for log output\nand abort with Esc!")
        self.status_widget.grid(row=1, column=0)

        self.root.bind("<Key>", self.event_key_pressed)
        self.root.update()

    def event_key_pressed(self, event):
        char_or_code = event.char or event.keycode
        log.critical("keypress: %s", repr(char_or_code))
        if char_or_code == "\x1b":  # Esc
            log.critical("Escape!")
            self.root.destroy()

    def display_queue_interval(self, interval):
        """
        consume all exiting "display RAM write" queue items and render them.
        """
        max_time = time.time() + 0.25
        while True:
            try:
                cpu_cycles, op_address, address, value = self.display_queue.get_nowait()
            except queue.Empty:
                #log.critical("display_queue empty -> exit loop")
                #                 log.critical(
                #                     "call display.write_byte() (display_queue._qsize(): %i)",
                #                     self.display_queue._qsize()
                #                 )
                break
            self.display.write_byte(cpu_cycles, op_address, address, value)
            if time.time() > max_time:
                log.critical("Abort display_queue_interval() loop: %.4fs", (time.time() - max_time))
                self.root.update()
#                 break
                self.root.after_idle(self.display_queue_interval, interval)
                return

        self.root.after(interval, self.display_queue_interval, interval)

    def mainloop(self):
        #log.critical("Start display_queue_interval()")
        self.display_queue_interval(interval=50)

        #log.critical("Start root.mainloop()")
        self.root.mainloop()
        #log.critical("root.mainloop() has quit!")

if __name__ == "__main__":
    display_queue = queue.Queue(maxsize=64)  # Display RAM write outputs

    g = DragonTkinterGUI(display_queue)

    cpu = FakeCPU(display_queue)
    cpu.deamon = True
    cpu.start()

    log.critical("mainloop start")
    g.mainloop()
    log.critical("mainloop end")
