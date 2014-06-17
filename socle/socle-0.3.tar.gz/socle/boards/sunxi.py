
import sys
import ConfigParser
import subprocess
from generic import GenericBoard
from menu import choice

class SunxiBoard(GenericBoard):
    NAME = "SUNXI"

    # Resetting such board configuration is not possible
    DEFAULT_FEX = None

    # List of boot partitions to probe
    BOOT_PARTITIONS = (
        ("Internal NAND",   "/dev/nand1"),
        ("MicroSD card",    "/dev/mmcblk0p1")
    )

    DISP_MODE_CHOICES = (
        ("Disabled", -1),
        ("HDMI-only", 0),
        ("VGA-only", 1),
        ("Dualhead", 2),
        ("Xinerama", 3),
        ("Clone", 4)
    )

    # HDMI output choices
    SCREEN0_OUTPUT_MODE_CHOICES = (
        ("480i", 0),
        ("576i", 1),
        ("480p", 2),
        ("576p", 3),
        ("720p @ 50Hz", 4),
        ("720p @ 60Hz", 5),
        ("1080i @ 50Hz", 7),
        ("1080p @ 24Hz", 8),
        ("1080p @ 50Hz", 9),
        ("1080p @ 60Hz", 10),
    )

    # VGA output choices
    SCREEN1_OUTPUT_MODE_CHOICES = (
        ("1680x1050", 0),
        ("1440x900", 1),
        ("1360x768", 2),
        ("1280x1024", 3),
        ("1024x768", 4),
        ("800x600", 5),
        ("640x480", 6),
        ("1920x1080", 10),
        ("1280x720", 11)
    )
    
    def __init__(self, sys_config_filename=None):
        self.sys_config_filename = sys_config_filename
        self.load(sys_config_filename)

    @classmethod
    def instantiate(cls):
        targets = (
            ("Internal NAND", "/mnt/nand1"),
            ("MicroSD card", "/")
        )
        
        target = choice(targets,
            "Target",
            "With this utility you can configure software intalled on internal NAND or SD card")

        return cls()

    def mainmenu(self):
        return (
            ("Reconfigure video outputs", self.reconfigure_video_outputs),
            ("Reconfigure GPIO pins",     self.reconfigure_gpio)
        )

    def load(self, filename):
        if filename.lower().endswith(".bin"):
            fex_filename = filename[:-4] + ".fex"
            subprocess.call(("bin2fex", filename, fex_filename))
        else:
            fex_filename = filename
        self.fex = ConfigParser.RawConfigParser()
        self.fex.readfp(open(fex_filename))
        
    def reset(self):
        self.fex.readp(open(self.DEFAULT_FEX))
        
    def save(self, filename=None):
        filename = filename or self.sys_config_filename
        if filename.lower().endswith(".bin"):
            fex_filename = filename[:-4] + ".fex"
        else:
            fex_filename = filename
            
        part_filename = fex_filename + ".part"
           
        with open(part_filename, "wb") as configfile:
            self.fex.write(configfile)
            
        if filename.lower().endswith(".bin"):
            subprocess.call(("fex2bin", part_filename, filename))
        else:
            os.rename(part_filename, filename)

    def reconfigure_video_outputs(self):

        disp_mode = choice(
            self.DISP_MODE_CHOICES,
            "Video output",
            "Select video output mode")
        disp_init_enable = int(disp_mode >= 0)
        
        self.fex.set("disp_init", "disp_mode", disp_mode)
        self.fex.set("disp_init", "disp_init_enable", disp_init_enable)
        if disp_init_enable:
            if disp_mode == 0 or disp_mode >= 2:
                screen0_output_mode = choice(
                    self.SCREEN0_OUTPUT_MODE_CHOICES,
                    "HDMI output resolution",
                    "Select HDMI output resolution")
                self.fex.set("disp_init", "screen0_output_type", "3")
            else:
                self.fex.set("disp_init", "screen0_output_type", "0")
                
            if disp_mode >= 1:
                screen1_output_mode = choice(
                    self.SCREEN1_OUTPUT_MODE_CHOICES,
                    "VGA output resolution",
                    "Select VGA output resolution")
                self.fex.set("disp_init", "screen1_output_type", "4")
            else:
                self.fex.set("disp_init", "screen1_output_type", "0")

    def reconfigure_gpio(self):
        UART3_TYPE_CHOICES = (
            ("Disabled", 0),
            ("Enabled", 2),
        )

        UART4_TYPE_CHOICES = (
            ("Disabled", 0),
            ("2pin", 2),
            ("4pin", 4),
        )
            
        UART7_TYPE_CHOICES = UART3_TYPE_CHOICES

        uart3_type = choice(
            UART3_TYPE_CHOICES,
            "UART3 configuration",
            "Select UART3 operation mode")
        if uart3_type > 0:
            self.fex.set("uart_para3", "uart_used", "1")
            self.fex.set("uart_para3", "uart_port", "3")
            self.fex.set("uart_para3", "uart_type", uart3_type)
        else:
            self.fex.set("uart_para3", "uart_used", "0")

        uart4_type = choice(
            UART4_TYPE_CHOICES,
            "UART4 configuration",
            "Select UART4 operation mode")
        if uart4_type > 0:
            self.fex.set("uart_para4", "uart_used", "1")
            self.fex.set("uart_para4", "uart_port", "4")
            self.fex.set("uart_para4", "uart_type", uart4_type)
        else:
            self.fex.set("uart_para4", "uart_used", "0")
            
        uart7_type = choice(
            UART7_TYPE_CHOICES,
            "UART7 configuration",
            "Select UART7 operation mode")
        if uart7_type > 0:
            self.fex.set("uart_para7", "uart_used", "1")
            self.fex.set("uart_para7", "uart_port", "7")
            self.fex.set("uart_para7", "uart_type", uart7_type)
        else:
            self.fex.set("uart_para7", "uart_used", "0")



                
if __name__ == "__main__":
    """
    It would be nice to keep "python sunxi.py /path/to/sysconfig.bin" working :)
    """
    sys_config_filename, = sys.argv[1:]
    board = SunxiBoard(sys_config_filename)
    board.reconfigure_video_outputs()
    board.reconfigure_gpio()
    board.save()
