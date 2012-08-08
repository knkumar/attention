#!/usr/bin/python
from optparse import OptionParser
import os 

def gen_csv(fname):
    session = open("data/"+fname+"/session.log", "rb")
    csv = open("results/"+fname+".csv", "wb")
    # the format for the file
    header = "TrialNum,Response,ResponseTime,Target,Item1,Item2,Item3\n"
    csv.write(header)
    for line in session.readlines():
        main = line.split('\t')[2]
        if ',' in main:
            csv.write(main[:-2]+"\n")
    session.close()
    csv.close()

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="file",
                      help="filename for the stat generation", metavar="FILE")
    parser.add_option("-a", "--all", action="store_true", dest="all", default=False,
                      help="generate csv for all the logs in data" )

    (options, args) = parser.parse_args()


    if not (options.file or options.all):
        print "Usage is getStats.py <-f|--file file> <-a|-all>"
    
    if options.file:
        gen_csv(options.file)

    if options.all:
        names = os.popen("ls data")
        for name in names.readlines():
            gen_csv(name.strip())
            print "done "+name.strip()
