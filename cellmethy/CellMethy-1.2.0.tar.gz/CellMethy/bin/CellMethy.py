#!/usr/bin/python

import sys,os,time
from optparse import OptionParser 
from tempfile import gettempdir
def splitfile(Input):
    path=os.getcwd()
    title='tmp'
    new_path=os.path.join(path,title)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
    else:
        file=os.listdir(new_path)
        for ele in file:
            os.remove(os.path.join(new_path,ele))
    fp=open(Input)
    for line in fp:
        x=line[0:-1].split('\t')
        if len(x)>2:
            chr=x[2]
            out=open(os.path.join(new_path,chr),'a')
            print >> out,line[0:-1]
def get_readmeth(read_set):
    """ input was all read mapping a CG site"""
    readid=[]
    state=[]
    for ele in read_set:
        readid.append(ele.split(',')[0])
        state.append(ele.split(',')[1])
    return readid,state
def get_overlapmeth(x,m,read,state): 
    """ input were read of one CG, methylation state corresponding to read, read of overlap, methylstion state of cg """
    k=x.index(read)
    state=state+m[k]
    return state        
def bin_fm(state,cg_number):
    """input were methylation state of overlap read for all CpGs in bin"""
    fmp=0
    standard=''
    i=0
    while i < cg_number:
        standard=standard+'Z'
        i=i+1
    for ele in state:
        if ele==standard:
            fmp=fmp+1
    fmp=float(fmp)/float(len(state))
    return fmp
def FMRcs(Inputfile,cg_number,coverage):
    """Inputfile was bismark processed including five columns: read, strand, chromosome, position, methylation state z(unmethylated) or Z(methylatyed)"""
    """Outputfile was three columns including chromosome, position, read and methylation split by "," """
    filename=open(os.path.join(os.getcwd(),'tmp')+'/'+Inputfile,'r')
    tempout=open(os.path.join(os.getcwd(),'tmp')+'/tempcfm.out','wb')
    dict_position={}  #store position for each chromosome
    for line in filename:
        x=line[0:-1].split('\t')
        read=x[0]
        position=x[3]
        state=x[4]
        dict_position.setdefault(int(position),[]).append(read+','+state)
    filename.close()
    position=sorted(dict_position.keys())
    c=0
    p=0
    while (p+c) in range(len(position)):
        bin_read=[]
        bin_state=[]
        bin_position=[]
        while c in range(cg_number):
            if p+c < len(position):
                bin_position.append(position[p+c])
                read_set=dict_position[position[p+c]]
                (read_id,state)=get_readmeth(read_set)
                bin_read.append(read_id)
                bin_state.append(state)
                c=c+1
            else:
                break
        bin_overlap=bin_read[0]
        c=1
        while c < len(bin_read):
            bin_overlap=list(set(bin_overlap)&set(bin_read[c]))
            c=c+1
        if len(bin_overlap)>= coverage:
            bin_meth=[]
            r=0
            while r < len(bin_overlap):
                cg_meth=''
                c=0
                while c < len(bin_read):
                    cg_meth=get_overlapmeth(bin_read[c],bin_state[c],bin_overlap[r],cg_meth)
                    c=c+1
                bin_meth.append(cg_meth)
                r=r+1
            bin_fmp=bin_fm(bin_meth,cg_number)
            cg=''
            for pos in bin_position:
                cg=cg+str(pos)+','
            out=Inputfile+'\t'+str(min(bin_position))+'\t'+str(max(bin_position))+'\t'+str(bin_fmp)+'\t'+cg
            print >> tempout,out
        p=p+1
        c=0
    dict_position.clear()
    tempout.close()
def extendme(data,position,ifm,ifmp,p,f,b,biny,cg): # hot extend
    """input were value of hot spot , initial value of x and y direction and bin"""
    if f!=0: # x direction extend
        if (p-f)>=0:
            forward=data[p-f][0:-1].split('\t')
            start=forward[1]
            distance=int(min(position))-int(start)
            forwardvalue=float(forward[3])
            if forwardvalue==0 or distance > 200 or distance <0:
                f=0
            elif forwardvalue > 0 :
                position.append(int(forward[1]))
                position.append(int(forward[2]))
                df=distance/float(100)
                ifm1=ifm+float(forwardvalue)*df
                ifmp1=ifm1/((int(max(position))-int(min(position)))/float(100))
                cgforward=forward[4].split(',')[0:-1]
                for ele in cgforward:
                    cg.append(ele)
                f=f+1
                ifm=ifm1
                ifmp=ifmp1
        else:
            f=0
    if b!=0: # y direction extend
        if (p+b)<=len(data)-1:
            back=data[p+b][0:-1].split('\t')
            end=back[2]
            distance=int(end)-int(max(position))
            backvalue=float(back[3])
            if backvalue==0 or distance > 200 or distance < 0:
                biny=b
                b=0
            elif backvalue > 0 :
                position.append(int(back[1]))
                position.append(int(back[2]))
                db=distance/float(100)
                ifm2=ifm+float(backvalue)*db
                ifmp2=ifm2/((int(max(position))-int(min(position)))/float(100))
                cgback=back[4].split(',')[0:-1]
                for ele in cgback:
                    cg.append(ele)
                b=b+1
                ifm=ifm2
                ifmp=ifmp2
                biny=b
        else:
            b=0
    return ifm,ifmp,position,f,b,biny,cg      

def FMCS(tempcfm):
    """Inputfile was the output of def FMRcs"""
    dataname=open(tempcfm,'r')
    tempout=open(os.path.join(os.getcwd(),'tmp')+'/tempfmp.out','wb')
    data=dataname.readlines()
    j=0
    while j < len(data):
        inint=data[j][0:-1].split('\t')
        chr=inint[0]
        value=inint[3]
        end=inint[2]
        if value!='0.0':
            k=1
            while 1:
                if (j+k) < len(data):
                    y=data[j+k][0:-1].split('\t')
                    value1=y[3]
                    end1=y[2]
                    d=int(end1)-int(end)
                    if value1 >= value and d <=200:
                        value=value1
                        k=k+1
                    else:
                        break
                else:
                    break
            p=j+k-1 #end index of full methylation region 
            position=[] # CG position in full methylation
            hot=data[p][0:-1].split('\t')
            hotvalue=hot[3]
            position.append(int(hot[1]))
            position.append(int(hot[2]))
            d=(int(hot[2])-int(hot[1]))/float(100)
            f=1 #x direction extend
            b=1 #y direction extend
            ifmp=float(hotvalue)
            ifm=ifmp*d
            biny=1 # extend bin number
            cg=hot[4].split(',')[0:-1]  # CG position in full methylation region
            while 1:
                (ifm,ifmp,position,f,b,biny,cg)=extendme(data,position,ifm,ifmp,p,f,b,biny,cg) 
                if f==0 and b==0:
                    break 
            meout=chr+'\t'+str(min(position))+'\t'+str(max(position))+'\t'+str(ifmp)+'\t'+str(len(list(set(cg))))
            print >> tempout, meout
            j=p+biny
        else:
            j=j+1
    dataname.close()
    tempout.close()        
def merge(tempcfm,tempfmp,FMRcsout):
    datacfm=open(tempcfm,'r')
    datafmp=open(tempfmp,'r')
    dataout=open(FMRcsout,'a')
    dict={}
    for line in datacfm:
        x=line[0:-1].split('\t')
        chr=x[0]
        start=int(x[1])
        end=int(x[2])
        cg=x[4]
        dict[start]=cg
    data=datafmp.readlines()
    j=0
    while j < len(data):
        x=data[j][0:-1].split('\t')
        chr=x[0]
        start=int(x[1])
        end=int(x[2])
        fmp=[]
        fmp.append(float(x[3]))
        cgnumber=int(x[4])
        cg=[]
        cfm=sorted(dict.keys())
        k=cfm.index(start)
        while 1:
            if k < len(cfm) and cfm[k]<=end:
                cgsite=dict[cfm[k]].split(',')[0:-1]
                for ele in cgsite:
                    cg.append(int(ele))
                k=k+1
            else:
                break
        p=1
        while j+p < len(data):
            y=data[j+p][0:-1].split('\t')
            start1=int(y[1])
            end1=int(y[2])
            if start1 in range(start, end+1) or (start1-end <= 100):
                end=end1
                fmp.append(float(y[3]))
                k=cfm.index(start1)
                while 1:
                    if k < len(cfm) and cfm[k]<=end1:
                        cgsite=dict[cfm[k]].split(',')[0:-1]
                        for ele in cgsite:
                            cg.append(int(ele))
                            k=k+1
                    else:
                        break
                p=p+1
            else:
                j=j+p-1
                break
        fmcs=sum(fmp)/float(len(fmp))
        number=len(list(set(cg)))
        out=chr+'\t'+str(start)+'\t'+str(end)+'\t'+str(fmcs)+'\t'+str(number)
        print >> dataout,out
        j=j+1


def main():
    usage = "usage: python %prog <-f filename> <-c coverage> [...]"
    description = "Select reads from two sam files. For example: python %prog -f inputfile -b 5 -c 10 -o outputfile"
    op = OptionParser(version="%prog 0.1",description=description,usage=usage,add_help_option=False)
    op.add_option("-h","--help",action="help",
                  help="Show this help message and exit.")
    op.add_option("-f","--infilename",dest="infilename",type="str",
                  help="The file name of input file after bismark processed, include five columns: read ID, strand, chromosome, position of CpG and methylation states Z (methylated) or z (unmethylated) separated by \t")
    op.add_option("-b","--BinLength",dest="BinLength",type="int",default="5",
                  help="number of CpGs in each bin, default is 5")
    op.add_option("-c","--coverage_cutoff",dest="coverage_cutoff",type="int",default="10",
                  help="Lowest coverage cutoff in each bin, default is 10")
    op.add_option("-o","--outfilename",dest="outfilename",type="str",default="FMcs.out",
                  help="The file name of output file showing full methylation of cell subpopulation, include five columns: chromosome, start, end, 3FMcs, and CpGs number in the region separated by \t")
    (options,args) = op.parse_args()
    if not options.infilename:
        op.print_help()
        sys.exit(1)
    inputfilename = options.infilename
    bin_length = options.BinLength
    coverage_cutoff=options.coverage_cutoff
    outputfilename=options.outfilename
    if os.path.exists(outputfilename):
        os.remove(outputfilename)
    #-------- step1: data spliting and processing
    print "data spliting and processing"
    splitfile(inputfilename)
    filedir=os.listdir(os.path.join(os.getcwd(),'tmp'))
    for ele in filedir:
        print ele
    #-------- step 2: calculate the fraction of full methylation in each bin -------#
        print "Calculating the fraction of full methylation in each bin"
        FMRcs(ele,bin_length,coverage_cutoff)
        
    #-------- step 3: hot spot extension and infer full methylation region-------#    
        print "Hot spot extension and inferring full methylation region" 
        tempcfm=os.path.join(os.getcwd(),'tmp')+'/tempcfm.out'
        FMCS(tempcfm)
           
    #-------- step 4: merge full methylation region which distance less than 100bp-------#    
        print "Merge full methylation region which distances are less than 100bp, and output"
        tempfmp=os.path.join(os.getcwd(),'tmp')+'/tempfmp.out'
        merge(tempcfm,tempfmp,outputfilename)
           

if __name__ == "__main__":
    
    try:
        main()
    except KeyboardInterrupt:
        sys.stderr.write("User interrupt me, see you!\n")
        sys.exit(0)    

            
                    
    



     
