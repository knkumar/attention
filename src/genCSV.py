#!/usr/bin/python
from optparse import OptionParser
import os 

def match():
    f = open("results/mapping.txt","rb")
    mapping = {}
    for line in f.readlines():
        k,v = line.split(",")
        mapping[k.strip()] = v.strip()
    return mapping

def gen_csv(fname, mapping):
    name = fname[:-4]
    ID = mapping[name]
    day = fname[-4:]
    session = open("data/gabor/"+fname+"/session.log", "rb")
    csv = open("results/gabor/"+ID+day+".csv", "wb")
    # the format for the file
    header = "ID, day,TrialNum,Response,RT,T,TOr,TPos,D1,D1Or,D1Pos,D2,D2Or,D2Pos,NumDist,Presence\n"
    positions = {"square":4, "red":5, "size":6}

    def drill(cols, position, out):
        item, other = cols[position].split("=")
        orient,pos = other.split("|")
        out.append(item)
        out.append(orient)
        out.append(pos)

    csv.write(header)
    for line in session.readlines():
        dists = [4,5,6]
        main = line.split('\t')[2]
        if ',' in main:
            cols = main.split(",")
            out = [ID,day]
            out.extend(cols[:3])
            target = positions[cols[3]]
            dists.remove(target)
            if cols[target]:
                drill(cols, target, out)
            else:
                out.extend["","",""])
            if cols[dists[0]]:
                drill(cols, dists[0], out)
            if cols[dists[1]]:
                drill(cols, dists[1], out)
            out.extend(["","",""]* (2-int(cols[7])) )
            out.extend(cols[7:])
            print out
            csv.write(",".join(out))
    session.close()
    csv.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                      help="filename for the stat generation", metavar="FILE")
    parser.add_option("-a", "--all", action="store_true", dest="all", default=False,
                      help="generate csv for all the logs in data" )

    (options, args) = parser.parse_args()

    mapping = match()

    if not (options.file or options.all):
        print "Usage is getStats.py <-f|--file file> <-a|-all>"
    
    if options.file:
        gen_csv(options.file, mapping)

    if options.all:
        names = os.popen("ls data/gabor")
        for name in names.readlines():
            gen_csv(name.strip(),mapping)
            print "done "+name.strip()
