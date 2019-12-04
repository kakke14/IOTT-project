import os                                                                       
from multiprocessing import Pool                                                
                                                                                
                                                                                
processes = ('mqqtBrooker.py', 'RestAPI.py', 'weatherStation.py')                                    
                                                  
                                                                                
def run_process(process):                                                             
    os.system('py -3 {}'.format(process))                                       
                                                                                
                                                                                
pool = Pool(processes=3)                                                        
pool.map(run_process, processes)   