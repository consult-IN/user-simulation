from Dateimanagement_Actions import *
from Microsoft_Actions import *
from Windows_Actions import *
from Web_Actions import *
from random import randint

import logging


if __name__ == '__main__':
    # Setup
    createDirectories()

    logging.basicConfig(filename='example.txt',
                        level=logging.DEBUG)
    # Schleife
    while 1:
        try:
            a = random.randint(1, 4)

            if a == 1:
                randomizer_Dateimanagement()
                
            if a == 2:
                randomizer_Microsoft()
             
            if a == 3:
                randomizer_Windows()
                
            if a == 4:
                randomizer_Web()
                
        except:
            logging.info("Main-Fehler:")
            pass
