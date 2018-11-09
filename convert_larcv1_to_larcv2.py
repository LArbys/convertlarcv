import os,sys,time
import multiprocessing as mp

def larcv1_server(someid,repodir,filename,productargs):
    os.system("./run_larcv1_server.sh {} {} {}".format(repodir,filename,productargs))


if __name__ == "__main__":

    if len(sys.argv)<3:
        print "usage: python convert_larcv1_to_larcv2.py filename.root {PRODUCT_NAME_LIST}"
        print "PRODUCT_NAME_LIST, pairs of [type]:[producername] e.g.  image2d:wire image2d:segment chstatus:wire ..."
        
    filename    = sys.argv[1]
    productlist = sys.argv[2:]
    
    productargs = ""
    for n,p in enumerate(productlist):
        productargs += p
        if n+1<len(productlist):
            productargs += " "

    someid = 0
    repodir = os.getcwd()
    p = mp.Process(target=larcv1_server,args=(someid,repodir,productargs))
    p.daemon = True
    p.start()

    print "Wait 3 seconds"
    time.sleep(3)

    print "larcv2 client"
    os.system("./run_larcv2_client.sh {}".format(repodir))
    
    print "DONE"
    
