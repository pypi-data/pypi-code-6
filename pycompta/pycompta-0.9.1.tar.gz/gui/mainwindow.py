"""
User interface for pycompta
"""

import os
import os.path as osp

import gtk
import gtk.glade
import gobject

import elementtree.ElementTree as ET

from pycompta.lib.render_html import format_montant
from pycompta.gui.treemodels import PlanComptableTreeModel

BROWSER = 'firefox'

def montant2int(montant):
    if ',' not in montant and '.' not in montant:
        montant += '00'
    montant = montant.replace(',','').replace(' ','').replace('.','')
    return int(montant)

def fmtmontant(montant):
    return format_montant(montant, separator=' ')

def totaux_ecriture(ecr):
    tc, td = 0, 0
    for credit in ecr.findall('credit'):
        tc += montant2int(credit.get('montant'))
    for debit in ecr.findall('debit'):
        td += montant2int(debit.get('montant'))
    return tc, td

class PycomptaEditorApp(object):

    def __init__(self, basedir=None):
        self.xml = gtk.glade.XML(osp.join(osp.dirname(__file__),'pycompta.glade'))
        self.xml.signal_autoconnect(self)
        self._context_msg = self.xml.get_widget('statusbar').get_context_id('main')

        if basedir:
            self.basedir = basedir
            self.reload_all()

    def on_mainquit(self, *args):
        """Bye"""
        gtk.main_quit()

    def on_open(self, *args):
        self.filew = gtk.FileSelection("Directory selection")
        filew = self.filew
        filew.connect("destroy", filew.destroy)
        filew.ok_button.connect("clicked", self.on_open_ok)
        filew.cancel_button.connect("clicked", lambda w: filew.destroy())
        filew.show()

    def on_open_ok(self, *args):
        self.basedir = self.filew.get_filename()
        assert osp.isdir(self.basedir)
        self.filew.hide()
        self.reload_all()

    def on_execute(self, *args):
        self.filew = gtk.FileSelection("Directory selection")
        filew = self.filew
        filew.connect("destroy", filew.destroy)
        filew.ok_button.connect("clicked", self.on_execute_ok)
        filew.cancel_button.connect("clicked", lambda w: filew.destroy())
        filew.show()

    def on_execute_ok(self, *args):
        self.targetdir = self.filew.get_filename()
        assert osp.isdir(self.targetdir)
        self.filew.hide()
        from pycompta import main
        main.run( [self.basedir, self.targetdir] )

    def on_check(self, *args):
        from pycompta import main
        config = main.get_config(self.basedir, '/tmp/')
        ecritures = main.read_ecritures(config['repertoire_ecritures'])
        debut = main.make_date(config['debut'])
        fin = main.make_date(config['fin'], -1)
        messages = main.check_ecritures(ecritures, debut, fin)
        if messages:
            import pigg.utils
            pigg.utils.show_msg('\n'.join(messages))

    def on_display(self, *args):
        os.system('%s %s' % (BROWSER, self.targetdir))

    def reload_all(self):
        if self.basedir[-1] == '/':
            self.basedir = self.basedir[:-1]
        self.xml.get_widget('window_main').set_title('%s - Pycompta' % osp.basename(self.basedir))

        # load plan comptable
        self.planc_tree = ET.parse(osp.join(self.basedir, 'plan-comptable.xml'))
        self.planc = {}
        for compte in self.planc_tree.findall('.//compte'):
            self.planc[compte.get('numero')] = compte.get('nom')
        self.plancmodel = PlanComptableTreeModel(self.planc_tree)
        self.setup_planc()

        # models
        self.data = None
        self.files = gtk.ListStore( gobject.TYPE_STRING, # filename
                                    )
        self.ecritures = gtk.ListStore( gobject.TYPE_STRING, # date
                                        gobject.TYPE_STRING, # libelle
                                        gobject.TYPE_STRING,    # total
                                        gobject.TYPE_STRING, # bgcolor
                                        gobject.TYPE_PYOBJECT,
                                        )
        self.detail = gtk.ListStore( gobject.TYPE_STRING, # compte
                                     gobject.TYPE_STRING, # libelle
                                     gobject.TYPE_INT,    # debit
                                     gobject.TYPE_STRING, # debit affichage
                                     gobject.TYPE_INT,    # credit
                                     gobject.TYPE_STRING, # credit affichage
                                     )
        self.setup_files_list()
        self.setup_ecritures_list()
        self.setup_detail()
        self.reload_files()
        self.detail_modified = False
        self.file_modified = False
        self.current_ecriture = None
        self.current_ecriture_it = None
        self.current_file = None

    def statusmsg(self, text):
        statusbar = self.xml.get_widget('statusbar')
        statusbar.pop(self._context_msg)
        statusbar.push(self._context_msg, text)

    def setup_planc(self):
        tree = self.xml.get_widget( "treeview_planc" )

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Compte", rend, text=0)
        tree.append_column( col )

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Libelle", rend, text=1)
        tree.append_column( col )

        tree.set_model( self.plancmodel )

    def setup_files_list(self):
        """
        setup the files list treeview
        """
        tree = self.xml.get_widget( "treeview_files" )
        tree.get_selection().connect("changed", self.fileselection_changed )

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Filename", rend, text=0 )
        tree.append_column( col )

        tree.set_model( self.files )

    def reload_files(self):
        treeview = self.xml.get_widget('treeview_list')
        treeview.freeze_notify()
        self.files.clear()
        self.ecritures.clear()
        self.detail.clear()
        ecr_dir = osp.join(self.basedir, 'ecritures')
        filenames = [filename[:-4] for filename in os.listdir(ecr_dir) if filename.endswith('.xml')]
        for filename in sorted(filenames):
            self.files.append( (filename,) )
        treeview.thaw_notify()

    def setup_ecritures_list(self):
        # Setup the list treeview
        tree = self.xml.get_widget( "treeview_list" )
        tree.get_selection().connect("changed", self.ecritureselection_changed )

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Date", rend, text=0, background=3)
        tree.append_column( col )

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Libelle", rend, text=1, background=3)
        col.set_property('expand', True)
        tree.append_column( col )

        rend = gtk.CellRendererText()
        rend.set_property('xalign', 1)
        col = gtk.TreeViewColumn("Total", rend, text=2, background=3)
        tree.append_column( col )

        tree.set_model( self.ecritures )

    def reload_ecritures(self, selected_file):
        treeview = self.xml.get_widget('treeview_list')
        treeview.freeze_notify()
        self.ecritures.clear()
        self.detail.clear()
        self.data = ET.parse(selected_file)
        self.current_file = selected_file
        for ecr in self.data.findall('.//ecriture'):
            tc, td = totaux_ecriture(ecr)
            if tc == td:
                color = None
            else:
                color = 'red'
            item =  (ecr.get('date'), unicode(ecr.find('libelle').text), fmtmontant(tc), color, ecr)
            self.ecritures.append(item)
        treeview.thaw_notify()

    def setup_detail(self):
        # Setup the detail treeview
        tree = self.xml.get_widget( "treeview_detail" )
        tree.get_selection().connect("changed", self.detailselection_changed )

        rend = gtk.CellRendererText()
        rend.set_property('editable', True)
        rend.connect('edited', self.detail_edited, 0)
        col = gtk.TreeViewColumn("Compte", rend, text=0)
        tree.append_column( col )

        rend = gtk.CellRendererText()
        col = gtk.TreeViewColumn("Libelle", rend, text=1)
        col.set_property('expand', True)
        tree.append_column( col )

        rend = gtk.CellRendererText()
        rend.set_property('xalign', 1)
        rend.set_property('editable', True)
        rend.connect('edited', self.detail_edited, 3)
        col = gtk.TreeViewColumn("Debit", rend, text=3)
        tree.append_column( col )

        rend = gtk.CellRendererText()
        rend.set_property('xalign', 1)
        rend.set_property('editable', True)
        rend.connect('edited', self.detail_edited, 5)
        col = gtk.TreeViewColumn("Credit", rend, text=5)
        tree.append_column( col )

        tree.set_model( self.detail )

    def reload_detail(self, selected_ecriture):
        treeview = self.xml.get_widget( "treeview_detail" )
        treeview.freeze_notify()
        self.detail.clear()
        for debit in selected_ecriture.findall('debit'):
            cpt = debit.get('compte')
            montant = montant2int(debit.get('montant'))
            item = (cpt, self.planc.get(cpt,'??'), montant, fmtmontant(montant), 0, '')
            self.detail.append(item)
        for credit in selected_ecriture.findall('credit'):
            cpt = credit.get('compte')
            montant = montant2int(credit.get('montant'))
            item = (cpt, self.planc.get(cpt,'??'), 0, '', montant, fmtmontant(montant))
            self.detail.append(item)
        self.detail_modified = False
        treeview.thaw_notify()

    def fileselection_changed(self, selection):
        model, it = selection.get_selected()
        if it:
            selected_file = model.get(it, 0)[0] + '.xml'
            selected_file = osp.join(self.basedir, 'ecritures', selected_file)
            if self.file_modified:
                self.data.write(self.current_file, encoding='iso-8859-1')
            self.reload_ecritures(selected_file)

    def ecritureselection_changed(self, selection):
        model, it = selection.get_selected()
        if it:
            selected_ecriture = model.get(it, 4)[0]
            if self.detail_modified:
                for item in self.current_ecriture.findall('credit'):
                    self.current_ecriture.remove(item)
                for item in self.current_ecriture.findall('debit'):
                    self.current_ecriture.remove(item)
                for entry in self.detail:
                    assert (entry[2],entry[4]) != (0,0)
                    if entry[2] != 0:
                        tag = ET.Element('debit')
                        tag.attrib['montant'] = entry[3]
                    else:
                        tag = ET.Element('credit')
                        tag.attrib['montant'] = entry[5]
                    tag.attrib['compte'] = entry[0]
                    self.current_ecriture.append(tag)
                    tc, td = totaux_ecriture(self.current_ecriture)
                    if tc == td:
                        color = None
                    else:
                        color = 'red'
                    model[self.current_ecriture_it][3] = 'red'
            self.reload_detail(selected_ecriture)
            self.current_ecriture_it = it
            self.current_ecriture = selected_ecriture

    def detailselection_changed(self, selection):
        model, it = selection.get_selected()
        if it:
            print 'youpla', model.get(it,0)

    def detail_edited(self, cell, path, new_text, col):
        print cell, path, new_text, col
        if col == 0:
            if new_text in self.planc:
                self.detail[path][col] = new_text
                self.detail[path][col+1] = self.planc[new_text]
            else:
                self.statusmsg("Le compte %s n'est pas dans le plan comptable." % new_text)
        elif col == 3:
            montant = montant2int(new_text)
            self.detail[path][col-1] = montant
            self.detail[path][col] = fmtmontant(montant)
        elif col == 5:
            montant = montant2int(new_text)
            self.detail[path][col-1] = montant
            self.detail[path][col] = fmtmontant(montant)
        else:
            assert False # FIXME
        self.detail_modified = True
        self.file_modified = True

def main(args):
    if args:
        basedir = args[0]
    else:
        basedir = None
    app = PycomptaEditorApp(basedir)
    gtk.main()

if __name__ == '__main__':
    import sys
    main(sys.argv[1])
