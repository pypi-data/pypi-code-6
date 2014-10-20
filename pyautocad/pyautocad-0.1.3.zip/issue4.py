import sys
import pygtk
if not sys.platform == 'win32':
    pygtk.require('2.0')

import gtk,gobject,time
import os.path
import datetime
from pyautocad import Autocad, utils
from pyautocad.contrib.tables import Table

now = datetime.datetime.now()
today_date = str(now.year) + str(now.month) + str(now.day) + "_" + str(now.hour) + "-" + str(now.minute)
acad = Autocad()

def set_file_name(self):
#This method checks the existance of an XLS file, and allows the user to overwrite it, 
#or use a different file.
    tableFilename = raw_input("Enter table name: ")
    tableFilename = tableFilename + ".xls"
    if os.path.isfile(tableFilename):
        fileoverwrite = 'n'
        while (fileoverwrite != 'y' or fileoverwrite != 'Y' or (os.path.isfile(tableFilename))):
            fileoverwrite = raw_input("File " + tableFilename + " exist. Overwrite (y/n)?")
            if fileoverwrite == 'y' or fileoverwrite == 'Y':
                break
            elif fileoverwrite == 'n' or fileoverwrite == 'N':
                tableFilename = raw_input("Enter table name: ")
                tableFilename = tableFilename + ".xls"
                if os.path.isfile(tableFilename):
                    continue
                else:
                    break
            else:
                print "Goodbye!"
                sys.exit(0)
    return tableFilename            


def line_lengths_excel(filename, draw_units):
# This function iterate over all the layers in the opened DWG and write sum of line lengths of each layer into one MS-Excel sheet.
# Parameters needed:
# 1. Name of an MS-Excel file (doesn't have to exist)
# 2. Units of the drwaing

        tableFilename = filename + '.xls'#set_file_name(self)
        table = Table()
        layers = []
        total_length = []
        units_scale = {"m":1, "cm":100, "mm":1000}
        units = draw_units #raw_input("Enter the used units for scaling(m/cm/mm): ")
        scale = units_scale[units]
        acad.prompt("Creating a table of line lengths")
        # value = 0.0
        for line in acad.iter_objects('line'):
            # pbar.set_fraction(value)
            # value = value + 0.01
            l1 = line.Length
            #print line.Layer
            if line.Layer in layers:
                i = layers.index(line.Layer)
                total_length[i] += l1
            else:
                layers.append(line.Layer)
                total_length.append(l1)
        print layers
        print total_length
        # Add data to table
        table.writerow(["COMPANY NAME", "Lines Lengths, Created:"+today_date])
        table.writerow(["Layer", "Length [" + units+"]"])
        for i in range(len(layers)):
            table.writerow([layers[i], total_length[i]])
        # Save table in xls
        table.save(tableFilename, 'xls')
        # raw_input("Press Enter to continue...")

def count_blocks_excel(filename):
# This function iterate over all the layers in the opened DWG and summing up all the blocks in the file into one MS-Excel sheet.
# Parameters needed:
# 1. Name of an MS-Excel file (doesn't have to exist)

        tableFilename = filename + '.xls'#set_file_name(self)
        table = Table()
        block_list = []
        block_layer = []
        total_blocks = []
        acad.prompt("Creating a table of blocks count")
        for layer in acad.iter_layouts():
            for block in acad.iter_objects('block'):
                b1 = block
                if block.name in block_list:
                    i = block_list.index(block.name)
                    total_blocks[i] += 1
                else:
                    block_list.append(block.name)
                    block_layer.append(block.Layer)
                    total_blocks.append(1)
        print block_list
        print total_blocks
        # Add data to table
        table.writerow(["Layer","Block", "Amount"])
        for i in range(len(block_list)):
            table.writerow([block_layer[i], block_list[i], total_blocks[i]])
        # Save table in xls
        table.save(tableFilename, 'xls')
        # raw_input("Press Enter to continue...")

class PyAPP():
    def __init__(self):
        self.window = gtk.Window()
        self.window.set_title("Automating AutoCAD Calculations")

        self.create_widgets()
        self.connect_signals()
        try:
            self.window.set_icon_from_file("Logo25.png")
        except Exception, e:
            print e.message
            sys.exit(1)
        self.window.show_all()
        gtk.main()

    def create_widgets(self):
        self.vbox = gtk.VBox(spacing=10)

        self.hbox_0 = gtk.HBox(spacing=10)      
        self.company_logo = gtk.Image()
        self.company_logo.set_from_file("company25mm90.png")
        self.hbox_0.pack_start(self.company_logo)

        self.hbox_1 = gtk.HBox(spacing=10)
        self.label = gtk.Label("File Name: ")
        self.hbox_1.pack_start(self.label)
        self.entry = gtk.Entry()
        self.hbox_1.pack_start(self.entry)
        self.unitsLabel = gtk.Label("DWG units: ")
        self.hbox_1.pack_start(self.unitsLabel)
        self.units = gtk.combo_box_new_text()
        self.units.append_text('m')
        self.units.append_text('cm')
        self.units.append_text('mm')
        self.units.set_active(1)
        self.hbox_1.pack_start(self.units)

        self.hbox_2 = gtk.HBox(spacing=10)
        self.bLineLength = gtk.Button("Sum Lines Lengths in a DWG to MS-Excel")
        self.hbox_2.pack_start(self.bLineLength)
        self.bBlocksCount = gtk.Button("Count Blocks in a DWG to MS-Excel")
        self.hbox_2.pack_start(self.bBlocksCount)

        self.hbox_3 = gtk.HBox(spacing=10)
        self.pbar = gtk.ProgressBar()
        self.hbox_3.pack_start(self.pbar)
        self.button_exit = gtk.Button("Exit")
        self.hbox_3.pack_start(self.button_exit)

        self.hbox_4 = gtk.HBox(spacing=10)
        self.se_logo = gtk.Image()
        self.se_logo.set_from_file("Logo25.png")
        self.hbox_4.pack_start(self.se_logo)
        self.se_label = gtk.Label("(2013)")
        self.hbox_4.pack_start(self.se_label)

        self.vbox.pack_start(self.hbox_0)
        self.vbox.pack_start(self.hbox_1)
        self.vbox.pack_start(self.hbox_2)
        self.vbox.pack_start(self.hbox_3)
        self.vbox.pack_start(self.hbox_4)

        self.window.add(self.vbox)

    def connect_signals(self):
        self.filename = self.entry.set_text('temp'+today_date)
        self.button_exit.connect("clicked", self.callback_exit)
        self.bLineLength.connect('clicked', self.callback_lines_lengths)
        self.bBlocksCount.connect('clicked', self.callback_blocks_count)    

    def callback_lines_lengths(self, widget, callback_data=None):
        filename = self.entry.get_text()
        draw_units = self.units.get_active_text()
        line_lengths_excel(filename, draw_units)

    def callback_blocks_count(self, widget, callback_data=None):
        filename = self.entry.get_text()
        count_blocks_excel(filename) 

    def callback_exit(self, widget, callback_data=None):
        gtk.main_quit()


if __name__ == "__main__":
    from pyautocad import ACAD
    print ACAD.acDataRow
    app = PyAPP()