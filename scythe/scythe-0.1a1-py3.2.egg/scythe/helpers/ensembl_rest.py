#import httplib2
import sys
import json
from decimal import Decimal
from datetime import datetime, date, timedelta
import mysql.connector
import os
import time
from ftplib import FTP
import tarfile
import zipfile
import gzip
from helpers.fastahelper import FastaParser
import os
def getSequencesFromFTP(outdir, release, specieslist=[]):
    path=outdir+os.sep+"fa"
    print(outdir, release, specieslist)
    if len(release)==1:
        release = release[0]
        dirlist = []
        if not os.path.isdir(path):
                os.makedirs(path)
        if (specieslist==[]):
            print("Warning: No set of species selected")
            exit(0)
        ftp = FTP('ftp.ensembl.org')
        ftp.login()
        ftp.cwd('pub') #ftp://ftp.ensembl.org/pub/
        ftp.retrlines('LIST', callback=dirlist.append)           # list directory contents
        #print(dirlist)
        dirlist = [r for r in dirlist if "release-"+str(release)  in r and "fasta" in r]
        print(dirlist)
        if(len(dirlist )==0):
            print("Nothing available for release-"+str(release))
            exit(1)
        ftprelhome = dirlist[0].split(" ")[-1]
        ftp.cwd(ftprelhome)
        ftp.retrlines('LIST', callback=dirlist.append)

        for s in specieslist:
            tmp = [d for d in dirlist if s in d][0]
            spec = tmp.split(" ")[-1]
            ftp.cwd(spec)
            ftp.cwd('pep')
            falist = []
            ftp.retrlines('LIST', callback=falist.append)
            falist = [f for f in falist if "all.fa" in f][0]
            fafile = falist.split(" ")[-1]
            outfaname = spec+".fa.gz"
            outfa = open(outfaname,'wb')
            ftp.retrbinary("RETR "+fafile,outfa.write)
            outfa.close()
            xtract(outfaname, path)
            ftp.cwd("/pub/"+ftprelhome)
       #nucleotides
        for s in specieslist:
            tmp = [d for d in dirlist if s in d][0]
            spec = tmp.split(" ")[-1]
            ftp.cwd(spec)
            ftp.cwd('cds')
            falist = []
            ftp.retrlines('LIST', callback=falist.append)
            falist = [f for f in falist if "all.fa" in f][0]
            fafile = falist.split(" ")[-1]
            outfaname = spec+".cds.all.fa.gz"
            print(outfaname, "cds\n")
            print(falist, "falist\n")
            outfa = open(outfaname,'wb')
            ftp.retrbinary("RETR "+fafile,outfa.write)
            outfa.close()
            if not os.path.exists(path+"_cds"):
                    os.makedirs(path+"_cds")
            xtract(outfaname, path+"_cds")
            ftp.cwd("/pub/"+ftprelhome)
        ftp.quit()

    else:
        print("Releases:")
        for a in zip(release,specieslist):
            print(a)
        for a in zip(release,specieslist):
            getSequencesFromFTP(outdir, release=[a[0]], specieslist=[a[1]])


def xtract(cfile, outpath = "."):

    if cfile.endswith('.gz'):
        dzf = ".".join(cfile.split(".")[:-1])
        #gzip
        gzf = gzip.open(cfile,'rb')
        content = gzf.read()
        out = open(outpath+os.sep+dzf,'wb')
        out.write(content)
        out.close
        gzf.close()
    else:
        print("Can't extract "+cfile)

###########################
class Pep(object):
    def __init__(self,pep,gene,length ):
        self.gene = gene
        self.pep  = pep
        self.length = length
        self.isLongest = None
def prepareLocFromFasta(fasta, outpath, specname):
    genes = {}
    longest = {}
    print(fasta, outpath)
    if not os.path.isdir(outpath):
        os.makedirs(outpath)


    if not outpath:
        out = fasta+".loc"
    else:
        out = outpath+os.sep+specname+".loc"
    fp = FastaParser()
    out = open(out,'w')
    print(out)
    for i in fp.read_fasta(fasta):
        tmp = i[0].split(" ")
        geneid = [t for t in tmp if "gene:" in t]
        geneid = geneid[0].split("gene:")[-1]
        proteinid = tmp[0]
        protlen=len(i[1])
        peptide= Pep(proteinid,geneid,protlen)
        try:
            genes[geneid].append(peptide)
            if peptide.length > longest[geneid].length:
                longest[geneid].isLongest =False
                longest[geneid]=peptide
                peptide.isLongest = True
        except KeyError as e:
            genes[geneid] = [peptide]
            longest[geneid] = peptide
            peptide.isLongest=True
    for g in genes:
        print(g)
        firstcol = [w for w in genes[g] if w.isLongest==True ]
        restcol = [w for w in genes[g] if w.isLongest!=True ]
        s = firstcol[0].gene+"\t"+firstcol[0].pep+"\t"
        s+="\t".join([v.pep for v in restcol])
        s+="\n"
        out.write(s)
        print(s)
    out.close()
    print("done")
#######################

def getSequences(stableids,outdir, specname):
    res = ""
    http = httplib2.Http(".cache")
    server = "http://beta.rest.ensembl.org"
    path=outdir+os.sep+"fa"
    if not os.path.isdir(path):
            os.makedirs(path)
    print(path)
    out = open(outdir+os.sep+"fa"+os.sep+specname+".fa",'w')
    for g in stableids:
            ext = "/sequence/id/"+g
            resp, content = http.request(server+ext, method="GET", headers={"Content-Type":"text/x-fasta"})
            print(content.decode("utf8"))
            out.write(content.decode("utf8"))
            time.sleep(0.4)
    out.close()


def getHomology(targetspecies, queryspecies, querystableids, outdir):
    path=outdir+os.sep+"ensembl_ortho_tsv"
    if not os.path.isdir(path):
            os.makedirs(path)
    out = open(outdir+os.sep+"ensembl_ortho_tsv"+os.sep+queryspecies+"__"+targetspecies+".tsv",'w')
    print("target:",targetspecies)
    print("query",queryspecies)
    print("stableids",querystableids)
    res = ""
    http = httplib2.Http(".cache")
    server = "http://beta.rest.ensembl.org"
    for g in  querystableids:
        ext = "/homology/id/"+g+"?content-type=application/json;format=condensed;type=orthologues;target_species="+targetspecies
        print(ext)
        resp, content = http.request(server+ext, method="GET", headers={"Content-Type":"application/json"})
        print(content.decode("utf8"))
        data = json.loads(content.decode("utf8"))
        print("data:",data)

        for f in data.values():
            try:
                tmp1 = f[0]["id"]
                tmp2 = f[0]["homologies"][0]
                print(tmp2)
                if (tmp2["type"] == "ortholog_one2one" ):
                    tmp2 = tmp2["id"]
                    out.write("\t".join([tmp1,tmp2]))
                    out.write("\n")

            except IndexError as e:
                    pass
            time.sleep(0.2)



def getGeneProteinRelation( outdir, specname, release):
    stableids=[]
    http = httplib2.Http(".cache")
    server = "http://beta.rest.ensembl.org"
    cmd = 'show databases like "'+specname+'_core_'+str(release)+'_%";'
    cnx = mysql.connector.connect(user='anonymous', host='ensembldb.ensembl.org' )

    curA = cnx.cursor(buffered=True)
    curB = cnx.cursor(buffered=True)
    curA.execute(cmd)


    size =dict()
    gene = dict()
    parent = dict()


    for a in curA:
        cmd = "use "+a[0]+";"
        print(cmd)
        curB.execute(cmd)
        cmd = 'select stable_id from gene where biotype="protein_coding" and source ="ensembl" limit 10;'
        curB.execute(cmd)
        path=outdir+os.sep+"ensembl_gene_tsv"
        if not os.path.isdir(path):
            os.makedirs(path)
        out = open(outdir+os.sep+"ensembl_gene_tsv"+os.sep+specname+"_"+str(release)+".tsv",'w')
        seen = set()

        for b in curB:#tuples
            print(b)
            for bb in b:
                time.sleep(0.2)
                ext = "/feature/id/"+bb+"?feature=cds"
                resp, content = http.request(server+ext, method="GET", headers={"Content-Type":"application/json"})
                data = json.loads(content.decode("utf8"))
                for f in data:
                    try:
                        size[f["ID"]]+=f["end"]-f["start"]+1
                        parent[bb].add(f["ID"])
                    except KeyError as e:
                        size[f["ID"]]=f["end"]-f["start"]+1
                        gene[f["ID"]]=bb
                    try:
                        parent[bb].add(f["ID"])
                    except KeyError as e:
                        parent[bb]=set()
    for g in parent:
        for gg in parent[g]:
            stableids.append(gg)
            out.write("\t".join([g,gg,str(size[gg])]))
            out.write("\n")
            #print(g,gg,size[gg] )
    curA.close()
    curB.close()
    return(stableids, parent.keys())

def useEnsemblDB(specs,rel, outdir):#, targets):
    res = ""
    http = httplib2.Http(".cache")
    server = "http://beta.rest.ensembl.org"

    for i in range(0,len(specs)):
        print(i)
        stableids, geneids = getGeneProteinRelation( outdir, specs[i], rel[i])
        getSequences(stableids,  outdir,specs[i] )
        if(i+1<len(specs)):
                getHomology(specs[i+1],specs[i],geneids, outdir)
def specInfo():
    pass
    http = httplib2.Http(".cache")
    server = "http://beta.rest.ensembl.org"
    ext = "/info/species"
    resp, content = http.request(server+ext, method="GET", headers={"Content-Type":"application/json"})
    data = json.loads(content.decode("utf8"))
    return(data)
def selectSpecies(data, namelist):
    backupdct={}
    specs = []
    rels =[]
    for s in data["species"]:
        print(s["release"], s["name"], s["aliases"], s["groups"])
        if (s["name"] in namelist ):
            specs.append(s["name"])
            rels.append(s["release"])
        else:
            aliases = s["aliases"]
            print(aliases)
            found = [a for a in aliases if a in namelist]
            if found:
                specs.append(s["name"])
                rels.append(s["release"])
    return(specs, rels)
def main():
    namelist = ["bos taurus", "human", "chimp"]
    data = specInfo()
    outdir=None
    if not outdir:
        outdir = "./"
    specs, rels = selectSpecies(data, namelist)
    useEnsemblDB(specs, rels, outdir)

if __name__ == "__main__":
    main()
