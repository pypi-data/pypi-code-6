#!/usr/bin/env python
# coding: utf-8

################################################################
# Dataset Builder ##############################################
################################################################

"""
   File Name: dataset.py
      Author: Wan Ji
      E-mail: wanji@live.com
  Created on: Sun Mar 16 12:03:09 2014 CST
"""
DESCRIPTION = """
"""

import random
from utils import *
from proto.dataset_pb2 import Sim2Query, Search, Dataset
from google.protobuf import text_format


class Builder(object):
    """ Dataset builder
    """

    # basic info
    IMAGE_LIST = 'image.lst'
    LABEL_LIST = 'label.lst'
    IMAGE_DATA = 'image.dat'
    IMAGE_DIR = 'image_dir'

    # search related
    DB_IMG_LIST = 'search/db.lst'
    QRY_IMG_LIST = 'search/query.lst'
    S2Q_LIST = 'search/sim2qry.lst'
    POS_LIST = 'search/pos.lst'
    AMB_LIST = 'search/amb.lst'
    TRAIN_LIST = 'search/train.lst'

    def __init__(self):
        # protobuf
        self.dataset = Dataset()
        self.search = Search()

        # path or name of images
        self.imglst = None
        # label of images
        self.lbslst = None
        # images in database
        self.dblst = None
        # images used as queries
        self.qrylst = None
        # similarity of database images to queries
        self.s2qlst = None
        # image similar to queries
        self.poslst = None
        # image ambiguous to queries
        self.amblst = None
        # images for training
        self.trainlst = None

        # print the doc string, which includes the PRE-REQURIES of
        # the source dir
        print self.__doc__

    def __def__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        """ Setup the command line parser
        """
        parser.add_argument('trg_dir', type=str,
                            help='target dir of dataset')

    @classmethod
    def get_name(cls, filepath):
        """ Get name of the file, excluding folder and extension
        """
        return ".".join(os.path.split(filepath)[1].split('.')[:-1])

    @staticmethod
    def ilst(arr):
        """
        Convert an array to int32 list
        """
        return [int(item) for item in arr]

    def generate_protobuf(self):
        """
        Packing and generate protobuf file
        """
        pinfo("Packing dataset protobuf ...\n")
        self.dataset.name = "Hi"
        self.dataset.comment = "Bye"
        self.dataset.images.extend(self.imglst)
        print self.dataset.labels
        print type(list(self.lbslst))
        print type(list(self.lbslst)[0])
        self.dataset.labels.extend(self.ilst(self.lbslst))
        pinfo("Done!\n")

        pinfo("Packing search protobuf ...\n")
        self.search.dblst.extend(self.ilst(self.dblst))
        self.search.trainlst.extend(self.ilst(self.trainlst))

        for qid in range(len(self.qrylst)):
            query = self.search.qrylst.add()
            query.query = self.qrylst[qid]
            query.poslst.extend(self.ilst(self.poslst[qid]))
            query.amblst.extend(self.ilst(self.amblst[qid]))

            for val, lsts in self.s2qlst.iteritems():
                sim2qrylst = query.sim2qrylst.add()
                sim2qrylst.sim2qry = val
                sim2qrylst.imglst.extend(self.ilst(lsts[qid]))
        pinfo("Done!\n")


    def generate(self, trgdir):
        """ Generate the dataset related files.
        """

        self.generate_protobuf()

        with open("%s/dataset.proto" % trgdir, "w") as dsf:
            dsf.write(text_format.MessageToString(self.dataset))

        with open("%s/search.proto" % trgdir, "w") as shf:
            shf.write(text_format.MessageToString(self.search))

        pinfo("Generating dataset files ")
        # create target dir
        os.system("mkdir -p %s/search" % trgdir)

        # store image list
        if None != self.imglst:
            np.savetxt(os.sep.join([trgdir, Builder.IMAGE_LIST]),
                       self.imglst, '%s')
            pinfo(".")
        if None != self.lbslst:
            np.savetxt(os.sep.join([trgdir, Builder.LABEL_LIST]),
                       self.lbslst, '%s')
            pinfo(".")
        if None != self.dblst:
            np.savetxt(os.sep.join([trgdir, Builder.DB_IMG_LIST]),
                       self.dblst, '%s')
            np.savetxt(os.sep.join([trgdir, Builder.DB_IMG_LIST+"_1"]),
                       [iid+1 for iid in self.dblst], '%s')
            pinfo(".")
        if None != self.qrylst:
            np.savetxt(os.sep.join([trgdir, Builder.QRY_IMG_LIST]),
                       self.qrylst, '%s')
            np.savetxt(os.sep.join([trgdir, Builder.QRY_IMG_LIST+"_1"]),
                       [iid+1 for iid in self.qrylst], '%s')
            pinfo(".")
        if None != self.trainlst:
            np.savetxt(os.sep.join([trgdir, Builder.TRAIN_LIST]),
                       self.trainlst, '%s')
            np.savetxt(os.sep.join([trgdir, Builder.TRAIN_LIST+"_1"]),
                       [iid+1 for iid in self.trainlst], '%s')
            pinfo(".")
        if None != self.s2qlst:
            for val, lsts in self.s2qlst.iteritems():
                save_lst_of_lst(os.sep.join([trgdir, Builder.S2Q_LIST +
                                             ".%.2f" % val]), lsts)
                save_lst_of_lst_plus(os.sep.join([trgdir, Builder.S2Q_LIST +
                                                  ".%.2f_1" % val]), lsts)
            pinfo(".")
        if None != self.poslst:
            save_lst_of_lst(os.sep.join([trgdir, Builder.POS_LIST]),
                            self.poslst)
            save_lst_of_lst_plus(os.sep.join([trgdir, Builder.POS_LIST+"_1"]),
                                 self.poslst)
            pinfo(".")
        if None != self.amblst:
            save_lst_of_lst(os.sep.join([trgdir, Builder.AMB_LIST]),
                            self.amblst)
            save_lst_of_lst_plus(os.sep.join([trgdir, Builder.AMB_LIST+"_1"]),
                                 self.amblst)
            pinfo(".")
        pinfo(" Done!\n")


class Oxford(Builder):
    """ Oxford-dataset builder.
    Download: http://www.robots.ox.ac.uk/~vgg/data/oxbuildings/

    !!NOTE!! `all_souls_000183.jpg` appeares in both `all_souls` and
             `radcliffe_camera` classes
    """

    ALL_LANDMARKS = ['all_souls', 'ashmolean', 'balliol', 'bodleian',
                     'christ_church', 'cornmarket', 'hertford', 'keble',
                     'magdalen', 'pitt_rivers', 'radcliffe_camera']

    def __init__(self, args):
        """ Parse the Oxford dataset
        """
        Builder.__init__(self)

        pinfo("Loading image list ... ")
        # convert the image path into relative path to the target dir
        imnames = [item.split(".jpg")[0] for item in
                   sorted(os.listdir(args.img_dir))]
        self.imglst = [os.path.relpath(os.sep.join([args.img_dir,
                                                    imname + ".jpg"]),
                                       args.trg_dir) for imname in imnames]
        self.lbslst = np.zeros(len(self.imglst), np.int32)
        pinfo("Done!\n")

        self.qrylst = []
        self.poslst = []
        self.amblst = []
        self.s2qlst = {args.good: [], args.ok: [], args.junk: []}

        clsnum = len(Oxford.ALL_LANDMARKS)
        # class id start from 1, 0 denotes background images
        for (clsid, landmark) in zip(range(1, clsnum + 1),
                                     Oxford.ALL_LANDMARKS):
            pinfo("\t%s\n" % landmark)
            for i in range(5):
                gtf = "%s_%d" % (landmark, i+1)

                qname = np.loadtxt("%s/%s_query.txt" % (args.gt_dir, gtf), dtype=np.str).\
                    tolist()[0].replace('oxc1_', '')
                qid = imnames.index(qname)
                self.qrylst.append(qid)

                good_names = loadlist("%s/%s_good.txt" % (args.gt_dir, gtf))
                good_ids = [imnames.index(x) for x in good_names]
                self.s2qlst[args.good].append(good_ids)

                ok_names = loadlist("%s/%s_ok.txt" % (args.gt_dir, gtf))
                ok_ids = [imnames.index(x) for x in ok_names]
                self.s2qlst[args.ok].append(ok_ids)

                cur_poslst = np.array(ok_ids + good_ids)
                # cur_poslst = cur_poslst[cur_poslst != qid]
                self.poslst.append(list(cur_poslst))

                junk_names = loadlist("%s/%s_junk.txt" % (args.gt_dir, gtf))
                junk_ids = [imnames.index(x) for x in junk_names]
                self.s2qlst[args.junk].append(junk_ids)
                self.amblst.append(junk_ids)
            self.lbslst[self.poslst[-1]] = clsid

        self.dblst = np.array(range(len(self.imglst)))

        self.trainlst = list(set(range(len(self.imglst))).difference(set(self.qrylst)))
        # self.trainlst = []
        # for classid in range(len(Oxford.ALL_LANDMARKS)):
        #     # select images with the same IDs, BUT NOT IN THE QUERY LIST
        #     candidates = [iid for iid in self.dblst[self.lbslst == (classid + 1)]
        #                   if iid not in self.qrylst]
        #     random.shuffle(candidates)
        #     self.trainlst += candidates[:args.selpos]

        # candidates = list(self.dblst[self.lbslst == 0])
        # random.shuffle(candidates)
        # self.trainlst += candidates[:args.selneg]

        pinfo("\n")

    def __del__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        Builder.set_parser(parser)
        parser.add_argument('img_dir', type=str,
                            help="""dir containing images extracted from
                            `oxbuild_images.tgz`""")
        parser.add_argument('gt_dir', type=str,
                            help="""dir containing groundtruth extracted from
                            `gt_files_170407.tgz`""")
        parser.add_argument('--good', type=float, default=3.0,
                            help="gain value for `good` results")
        parser.add_argument('--ok', type=float, default=2.0,
                            help="gain value for `ok` results")
        parser.add_argument('--junk', type=float, default=1.0,
                            help="gain value for `junk` results")
        parser.add_argument('--selpos', type=int, default=7,
                            help="NO. of positive image for each class")
        parser.add_argument('--selneg', type=int, default=500,
                            help="number of selected negative")


class OxfordM(Oxford):
    """ Metric Learning Edition of `Oxford`
    """

    # selected classes for metric learning
    SEL_LANDMARKS = ['all_souls', 'ashmolean', 'bodleian', 'christ_church',
                     'hertford', 'magdalen', 'radcliffe_camera']
    # SEL_LANDMARKS = Oxford.ALL_LANDMARKS
    #

    def __init__(self, args):
        Oxford.__init__(self, args)

        all_classes = ['background'] + Oxford.ALL_LANDMARKS

        pinfo("Preparing for metric learning ... ")
        self.trainlst = []
        qry_lbs = self.lbslst[self.qrylst]
        qry_mask = np.zeros(len(self.qrylst))
        for sel_landmark in OxfordM.SEL_LANDMARKS:
            classid = all_classes.index(sel_landmark)
            qry_mask[qry_lbs == classid] = 1
            # select images with the same IDs, BUT NOT IN THE QUERY LIST
            candidates = [iid for iid in self.dblst[self.lbslst == (classid+1)]
                          if iid not in self.qrylst]
            random.shuffle(candidates)
            self.trainlst += candidates[:args.selpos]

        candidates = list(self.dblst[self.lbslst == 0])
        random.shuffle(candidates)
        self.trainlst += candidates[:500]

        self.qrylst = [self.qrylst[qid] for qid in range(len(self.qrylst))
                       if qry_mask[qid] > 0]
        self.poslst = [self.poslst[qid] for qid in range(len(self.poslst))
                       if qry_mask[qid] > 0]
        self.amblst = [self.amblst[qid] for qid in range(len(self.amblst))
                       if qry_mask[qid] > 0]

        self.dblst = [iid for iid in self.dblst
                      if iid not in self.trainlst]
        for i in range(len(self.qrylst)):
            self.poslst[i] = [iid for iid in self.poslst[i]
                              if iid not in self.trainlst]
            self.amblst[i] = [iid for iid in self.amblst[i]
                              if iid not in self.trainlst]
        for key in self.s2qlst.keys():
            self.s2qlst[key] = [self.s2qlst[key][qid] for qid
                                in range(len(self.s2qlst[key]))
                                if qry_mask[qid] > 0]
            for i in range(len(self.qrylst)):
                self.s2qlst[key][i] = [iid for iid in self.s2qlst[key][i]
                                       if iid not in self.trainlst]
        self.dblst = [iid for iid in self.dblst
                      if iid not in self.trainlst]
        pinfo("Done!\n")

    @classmethod
    def set_parser(cls, parser):
        Oxford.set_parser(parser)


class Paris(Builder):
    """ Paris-dataset builder.
    Download: http://www.robots.ox.ac.uk/~vgg/data/parisbuildings/
    """

    ALL_LANDMARKS = ['defense', 'eiffel', 'invalides', 'louvre', 'moulinrouge',
                     'museedorsay', 'notredame', 'pantheon', 'pompidou',
                     'sacrecoeur', 'triomphe']

    def __init__(self, args):
        """ Parse the Parse dataset
        """
        Builder.__init__(self)

        pinfo("Loading image list ... ")
        self.imglst = []
        # convert the image path into relative path to the target dir
        for dpath, _, files in os.walk(args.img_dir):
            for fpath in files:
                self.imglst.append(os.path.relpath(os.path.join(dpath, fpath),
                                                   args.trg_dir))
        self.imglst = sorted(self.imglst)
        imnames = [Builder.get_name(path) for path in self.imglst]
        self.lbslst = np.zeros(len(self.imglst), np.int32)
        pinfo("Done!\n")

        self.qrylst = []
        self.poslst = []
        self.amblst = []
        self.s2qlst = {args.good: [], args.ok: [], args.junk: []}

        clsnum = len(Oxford.ALL_LANDMARKS)
        # class id start from 1, 0 denotes background images
        for (clsid, landmark) in zip(range(1, clsnum + 1),
                                     Paris.ALL_LANDMARKS):
            pinfo("\t%s\n" % landmark)
            for i in range(5):
                gtf = "%s_%d" % (landmark, i+1)

                qname = np.loadtxt("%s/%s_query.txt" % (args.gt_dir, gtf), dtype=np.str).\
                    tolist()[0].replace('oxc1_', '')
                qid = imnames.index(qname)
                self.qrylst.append(qid)

                good_names = loadlist("%s/%s_good.txt" % (args.gt_dir, gtf))
                good_ids = [imnames.index(x) for x in good_names]
                self.s2qlst[args.good].append(good_ids)

                ok_names = loadlist("%s/%s_ok.txt" % (args.gt_dir, gtf))
                ok_ids = [imnames.index(x) for x in ok_names]
                self.s2qlst[args.ok].append(ok_ids)

                cur_poslst = np.array(ok_ids + good_ids)
                # cur_poslst = cur_poslst[cur_poslst != qid]
                self.poslst.append(list(cur_poslst))

                junk_names = loadlist("%s/%s_junk.txt" % (args.gt_dir, gtf))
                junk_ids = [imnames.index(x) for x in junk_names]
                self.s2qlst[args.junk].append(junk_ids)
                self.amblst.append(junk_ids)
            self.lbslst[self.poslst[-1]] = clsid
            print clsid, len(self.poslst[-1])

        self.dblst = np.array(range(len(self.imglst)))

        self.trainlst = list(set(range(len(self.imglst))).difference(set(self.qrylst)))
        # self.trainlst = []
        # for classid in range(len(Paris.ALL_LANDMARKS)):
        #     # select images with the same IDs, BUT NOT IN THE QUERY LIST
        #     candidates = [iid for iid in self.dblst[self.lbslst == (classid+1)]
        #                   if iid not in self.qrylst]
        #     random.shuffle(candidates)
        #     self.trainlst += candidates[:args.selpos]

        # candidates = list(self.dblst[self.lbslst == 0])
        # random.shuffle(candidates)
        # self.trainlst += candidates[:args.selneg]

        pinfo("\n")

    def __del__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        Builder.set_parser(parser)
        parser.add_argument('img_dir', type=str,
                            help="""dir containing images extracted from
                            `paris_1.tgzk` and `paris_2.tgz`""")
        parser.add_argument('gt_dir', type=str,
                            help="""dir containing groundtruth extracted from
                            `paris_120310.tgz`""")
        parser.add_argument('--good', type=float, default=3.0,
                            help="gain value for `good` results")
        parser.add_argument('--ok', type=float, default=2.0,
                            help="gain value for `ok` results")
        parser.add_argument('--junk', type=float, default=1.0,
                            help="gain value for `junk` results")
        parser.add_argument('--selpos', type=int, default=15,
                            help="NO. of positive image for each class")
        parser.add_argument('--selneg', type=int, default=500,
                            help="number of selected negative")


class ParisM(Paris):
    """ Metric Learning Edition of `Paris`
    """

    # selected classes for metric learning
    SEL_LANDMARKS = Paris.ALL_LANDMARKS

    def __init__(self, args):
        Paris.__init__(self, args)

        all_classes = ['background'] + Paris.ALL_LANDMARKS

        pinfo("Preparing for metric learning ... ")
        self.trainlst = []
        qry_lbs = self.lbslst[self.qrylst]
        qry_mask = np.zeros(len(self.qrylst))
        for sel_landmark in ParisM.SEL_LANDMARKS:
            classid = all_classes.index(sel_landmark)
            qry_mask[qry_lbs == classid] = 1
            candidates = [iid for iid in self.dblst[self.lbslst == (classid+1)]
                          if iid not in self.qrylst]
            random.shuffle(candidates)
            self.trainlst += candidates[:args.selpos]

        candidates = list(self.dblst[self.lbslst == 0])
        random.shuffle(candidates)
        self.trainlst += candidates[:500]

        self.qrylst = [self.qrylst[qid] for qid in range(len(self.qrylst))
                       if qry_mask[qid] > 0]
        self.poslst = [self.poslst[qid] for qid in range(len(self.poslst))
                       if qry_mask[qid] > 0]
        self.amblst = [self.amblst[qid] for qid in range(len(self.amblst))
                       if qry_mask[qid] > 0]

        self.dblst = [iid for iid in self.dblst
                      if iid not in self.trainlst]
        for i in range(len(self.qrylst)):
            self.poslst[i] = [iid for iid in self.poslst[i]
                              if iid not in self.trainlst]
            self.amblst[i] = [iid for iid in self.amblst[i]
                              if iid not in self.trainlst]
        for key in self.s2qlst.keys():
            self.s2qlst[key] = [self.s2qlst[key][qid] for qid
                                in range(len(self.s2qlst[key]))
                                if qry_mask[qid] > 0]
            for i in range(len(self.qrylst)):
                self.s2qlst[key][i] = [iid for iid in self.s2qlst[key][i]
                                       if iid not in self.trainlst]
        self.dblst = [iid for iid in self.dblst
                      if iid not in self.trainlst]
        pinfo("Done\n")

    @classmethod
    def set_parser(cls, parser):
        Paris.set_parser(parser)


class Holidays(Builder):
    """ Holidays-dataset builder.
    Download: http://lear.inrialpes.fr/~jegou/data.php
    """

    def __init__(self, args):
        """ Parse the Parse dataset
        """
        Builder.__init__(self)

        pinfo("Loading image list ... ")
        # convert the image path into relative path to the target dir
        imnames = [item.split(".jpg")[0] for item in
                   sorted(os.listdir(args.img_dir))]
        self.imglst = [os.path.relpath(os.sep.join([args.img_dir,
                                                    imname + ".jpg"]),
                                       args.trg_dir) for imname in imnames]
        pinfo("Done!\n")

        self.qrylst = []
        self.poslst = []
        self.amblst = []
        self.s2qlst = {args.good: [], args.ok: [], args.junk: []}

        for imname in imnames:
            imidx = imnames.index(imname)
            print imidx, len(self.qrylst)
            if (int(imname) % 100 == 0):
                self.qrylst.append(imidx)
                self.poslst.append([])
                self.amblst.append([imidx])
                self.s2qlst[args.good].append([])
                self.s2qlst[args.ok].append([])
                self.s2qlst[args.junk].append([])
            else:
                self.poslst[len(self.qrylst)-1].append(imidx)
                self.s2qlst[args.ok][len(self.qrylst)-1].append(imidx)

        self.dblst = range(len(self.imglst))
        pinfo("\n")

    def __del__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        Builder.set_parser(parser)
        parser.add_argument('img_dir', type=str,
                            help="""dir containing images extracted from
                            `jpg1.tar.gz` and `jpg2.tar.gz`""")
        parser.add_argument('--good', type=float, default=3.0,
                            help="gain value for `good` results")
        parser.add_argument('--ok', type=float, default=2.0,
                            help="gain value for `ok` results")
        parser.add_argument('--junk', type=float, default=1.0,
                            help="gain value for `junk` results")


class UKBench(Builder):
    """ UKBench-dataset builder.
    Download: http://vis.uky.edu/~stewe/ukbench/
    """

    def __init__(self, args):
        """ Parse the Parse dataset
        """
        Builder.__init__(self)

        pinfo("Loading image list ... ")
        # convert the image path into relative path to the target dir
        imnames = [item.split(".jpg")[0] for item in
                   sorted(os.listdir(args.img_dir))]
        self.imglst = [os.path.relpath(os.sep.join([args.img_dir,
                                                    imname + ".jpg"]),
                                       args.trg_dir) for imname in imnames]
        pinfo("Done!\n")

        self.qrylst = []
        self.poslst = []
        self.amblst = []

        for idx in range(0, len(imnames), 4):
            self.qrylst.append(idx)
            self.poslst.append(range(idx, idx+4))
            self.amblst.append([])

        self.dblst = range(len(self.imglst))
        pinfo("\n")

    def __del__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        Builder.set_parser(parser)
        parser.add_argument('img_dir', type=str,
                            help="""dir containing full sized images extracted from
                            `ukbench.zip`""")


class Caltech(Builder):
    """ Caltech101/256-dataset builder.
    Download: http://www.vision.caltech.edu/Image_Datasets/Caltech101/
              http://www.vision.caltech.edu/Image_Datasets/Caltech256/

    NOTE: the image list are generated by another program.
        The list contains lines of image information:
            `path_of_image_0` `class_label_of_image_0`
            `path_of_image_1` `class_label_of_image_1`
            `path_of_image_2` `class_label_of_image_2`
            ...
    """

    def __init__(self, args, pos=1):
        """
        """
        Builder.__init__(self)

        self.s2qlst = {pos: []}

        pinfo("Loading image list ")
        pinfo(".")
        imglst = [line.split() for line in loadlist(args.imglst)]
        pinfo(".")
        self.imglst = [line[0] for line in imglst]
        pinfo(".")
        raw_lbs = [int(line[1]) for line in imglst]
        uniqlbs = list(np.unique(raw_lbs))
        self.lbslst = np.array([uniqlbs.index(lbl) for lbl in raw_lbs])
        pinfo(".")
        pinfo(" Done!\n")

        self.trainlst = np.ndarray(0, np.int64)
        self.dblst = np.ndarray(0, np.int64)
        self.qrylst = np.ndarray(0, np.int64)

        imgnum = len(self.imglst)
        clsnum = len(uniqlbs)
        imgrange = np.array(range(imgnum))
        for i in range(clsnum):
            cur_ids = imgrange[self.lbslst == i]
            np.random.shuffle(cur_ids)
            self.trainlst = np.hstack((self.trainlst, cur_ids[:args.trnum]))
            self.qrylst = np.hstack((self.qrylst,
                                     cur_ids[args.trnum:
                                             args.trnum + args.tsnum]))
            self.dblst = np.hstack((self.dblst,
                                    cur_ids[args.trnum:
                                            args.trnum + args.tsnum]))

        pinfo("\tGenerating label list ")
        pinfo(".")
        self.dlblst = self.lbslst[self.dblst]
        pinfo(".")
        self.qlblst = self.lbslst[self.qrylst]
        pinfo(".")
        pinfo(" Done!\n")

        pinfo("\tGenerating pos list \n")
        self.poslst = []
        self.amblst = []
        qrynum = len(self.qrylst)
        for qid in range(qrynum):
            if qid % 10 == 0:
                pinfo("\r\t\t%d/%d" % (qid, qrynum))
            self.poslst.append(self.dblst[self.dlblst == self.qlblst[qid]])
            self.amblst.append([])
        self.s2qlst[pos] = self.poslst
        pinfo("\r\t\t%d/%d\tDone!\n" % (len(self.qrylst), len(self.qrylst)))

    def __del__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        Builder.set_parser(parser)
        parser.add_argument('imglst', type=str,
                            help="image image list")
        parser.add_argument('trnum', type=int, nargs='?', default=30,
                            help="NO. of training images per class")
        parser.add_argument('tsnum', type=int, nargs='?', default=20,
                            help="NO. of test images per class")


class ImageNet2012(Builder):
    """ ImageNet 2012 dataset builder.
    Download: http://www.image-net.org/challenges/LSVRC/2012/

    NOTE: the training/validation image list are generated by another program.
        both list contain lines of image information:
            `path_of_image_0` `class_label_of_image_0`
            `path_of_image_1` `class_label_of_image_1`
            `path_of_image_2` `class_label_of_image_2`
            ...
    """

    def __init__(self, args, pos=1):
        """
        """
        Builder.__init__(self)

        self.s2qlst = {pos: []}

        pinfo("Loading image list ")
        pinfo(".")
        trainlst = [line.split() for line in loadlist(args.trainlst)]
        pinfo(".")
        vallst = [line.split() for line in loadlist(args.vallst)]
        pinfo(".")
        self.imglst = [line[0] for line in trainlst] + \
            [line[0] for line in vallst]
        pinfo(".")
        pinfo(" Done!\n")

        pinfo("\tGenerating DB/query list ")
        pinfo(".")
        self.dblst = np.array(range(len(trainlst)))
        pinfo(".")
        self.qrylst = np.array(range(len(vallst)))
        pinfo(".")
        pinfo(" Done!\n")

        pinfo("\tGenerating label list ")
        pinfo(".")
        self.dlblst = np.array([int(line[1]) for line in trainlst])
        pinfo(".")
        self.qlblst = np.array([int(line[1]) for line in vallst])
        pinfo(".")
        pinfo(" Done!\n")

        pinfo("\tGenerating pos list \n")
        self.poslst = []
        self.amblst = []
        for qid in self.qrylst:
            if qid % 100 == 0:
                pinfo("\r\t\t%d/%d" % (qid, len(self.qrylst)))
            self.poslst.append(self.dblst[self.dlblst == self.qlblst[qid]])
            self.amblst.append([])
        self.s2qlst[pos] = self.poslst
        pinfo("\r\t\t%d/%d\tDone!\n" % (len(self.qrylst), len(self.qrylst)))

    def __del__(self):
        pass

    @classmethod
    def set_parser(cls, parser):
        Builder.set_parser(parser)
        parser.add_argument('trainlst', type=str,
                            help="""training image list""")
        parser.add_argument('vallst', type=str,
                            help="""validation image list""")


DATASETS = {
    'caltech':     Caltech,
    'imgnet2012':  ImageNet2012,
    'ukbench':     UKBench,
    'holidays':    Holidays,
    'parism':      ParisM,
    'paris':       Paris,
    'oxfordm':     OxfordM,
    'oxford':      Oxford}
