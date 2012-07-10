import csv

def customLogger(directory,filename,header,lists):
    
    filename=directory+'/'+filename
    f=open(filename,'w')
    f.write('#'+header+'\n')
    writer = csv.writer(f, delimiter=',')   
    
    lists=[map(lambda x:str(x),item) for item in lists]
    
    for item in lists:
        writer.writerow(item)
    

    
        