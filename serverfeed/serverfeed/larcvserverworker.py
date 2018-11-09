import os,sys,time
from worker import WorkerService
import numpy as np
import zlib
import zmq

from larcv import larcv

import msgpack
import msgpack_numpy as m
m.patch()

os.environ["GLOG_minloglevel"] = "1"

class LArCVServerWorker( WorkerService ):
    """ This worker uses a user function to prepare data. """

    def __init__( self,identity,inputfile,ipaddress,load_func,batchsize=None,verbosity=0,queuesize=1,randomaccess=True):
        super( LArCVServerWorker, self ).__init__(identity,ipaddress,verbosity=verbosity,queuesize=queuesize)
        self.inputfile = inputfile
        self.io = larcv.IOManager(larcv.IOManager.kREAD)
        self.io.add_in_file(self.inputfile)
        self.io.initialize()
        self.nentries = self.io.get_n_entries()
        self.batchsize = batchsize
        self.products = {}
        self.compression_level = 4
        self.print_msg_size = False
        self.num_reads = 0
        self.current_idx = 0
        self.randomaccess = randomaccess
        self.load_func = load_func
        if not callable(self.load_func.loadevent):
            raise ValueError("'load_func' argument needs to be a function returning a dict of numpy arrays")
        print "LArCVServerWorker[{}] is loaded.".format(self._identity)
        
    def process_message(self, frames ):
        """ just a request. nothing to parse
        """
        return True

    def fetch_data(self):
        """ load up the next data set. we've already sent out the message. so here we try to hide latency while gpu running. """

        tstart = time.time()
        # get data
        if self.randomaccess:
            indices = np.random.randint(0,high=self.nentries,size=(self.batchsize))
        else:
            indices = np.arange( self.current_idx, self.current_idx+self.batchsize, dtype=np.int )
            if self.current_idx+self.batchsize>=self.nentries:
                # reset
                overidx = (self.current_idx+self.batchsize) - self.nentries                                    
                if overidx+1<self.batchsize:
                    indices[overidx:] = np.arange(0,self.batchsize-overidx,dtype=np.int)
                self.current_idx = self.batchsize-overidx-1
            else:
                self.current_idx += self.batchsize
                    
                
        batch = []
        keylist = None
        for ib,idx in enumerate(indices):
            self.io.read_entry(idx)
            batch.append( self.load_func.loadevent( self.io ) )
            if keylist is None:
                keylist = batch[-1].keys()

        self.products = {}
        for k in keylist:
            nchannels = 1
            datashape = batch[0][k].shape
            if len(datashape)==3:
                nchannels = datashape[0]
            self.products[k] = np.zeros( (self.batchsize,nchannels,datashape[-2],datashape[-1]), dtype=batch[0][k].dtype )
        for ib,batchdata in enumerate(batch):
            for k in keylist:
                if len(batchdata[k].shape)!=3:
                    self.products[k][ib,0,:,:] = batchdata[k][:,:]
                else:
                    self.products[k][ib,:,:,:] = batchdata[k][:,:,:]
            
        self.num_reads += 1
        tload = time.time()-tstart
        if self._verbosity>0:
            print "LArCVServerWorker[{}] fetched data. time={} secs. nreads={}".format(self._identity,tload,self.num_reads)
        return
    
    def generate_reply(self):
        """
        our job is to return our data set, then load another
        """
        self.fetch_data()
        
        reply = [self._identity]
        totmsgsize = 0.0
        totcompsize = 0.0
        tstart = time.time()
        for key,arr in self.products.items():
                
            # encode
            x_enc = msgpack.packb( arr, default=m.encode )
            x_comp = zlib.compress(x_enc,self.compression_level)

            # for debug: inspect compression gains (usually reduction to 1% or lower of original size)
            if self.print_msg_size:
                encframe = zmq.Frame(x_enc)
                comframe = zmq.Frame(x_comp)
                totmsgsize  += len(encframe.bytes)
                totcompsize += len(comframe.bytes)
                
            reply.append( key.encode('utf-8') )
            reply.append( x_comp )

        if self._verbosity>1:
            if self.print_msg_size:
                print "LArCVServerWorker[{}]: size of array portion={} MB (uncompressed {} MB)".format(self._identity,totcompsize/1.0e6,totmsgsize/1.0e6)
            print "LArCVServerWorker[{}]: generate msg in {} secs".format(self._identity,time.time()-tstart)
        return reply
        
            

if __name__ == "__main__":
    pass


    
