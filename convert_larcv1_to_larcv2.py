import os,sys,time
import multiprocessing as mp

def larcv1_server(someid,repodir):
    os.system("./run_larcv1_server.sh {}".format(repodir))


if __name__ == "__main__":

    someid = 0
    repodir = os.getcwd()
    p = mp.Process(target=larcv1_server,args=(someid,repodir))
    p.daemon = True
    p.start()

    print "Wait 3 seconds"
    time.sleep(3)

    print "larcv2 client"
    os.system("./run_larcv2_client.sh {}".format(repodir))
    
    print "DONE"
    
