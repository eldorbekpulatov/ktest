"""
Usage:
    test.py <path> [-d <dvmAdd>]... [-o <oscAdd>]... [-r <relAdd>]... [-a <anaAdd>]... [-e <eldAdd>]... 

Options:
    -d <dvmAdd>
    -o <oscAdd>
    -r <relAdd>
    -a <anaAdd>
    -e <eldAdd>
"""

import os
import time
import logging
from docopt import docopt

def test_function():    
    for each in range(0,100, 1):
        logging.info("counting UP: "+str(each))
    return each == 100

def master(args):
    logging.basicConfig(filename=args['<path>'], level=logging.INFO, 
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt=' %b %d, %Y %H:%M:%S', filemode='w')
    
    # beginning time
    tick_01 = time.time()
    logging.info('Starting Project: {}'.format("test"))

    
    if test_function():
        print("Passeed test!")
    else:
        print("Failed test!")

    
    # ending time
    tock_01 = time.time()
    logging.info('Finished Project {} in: {} seconds.'.format("test", (tock_01-tick_01)))


if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments is not None:    
        master(arguments)
    else:
        os.sys.exit()
        