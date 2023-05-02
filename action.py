from persistence import *
from dbtools import *

import sys
import os
import sqlite3
import atexit

def main(args : list):
    inputfilename : str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline : list[str] = line.strip().split(", ")
            #TODO: apply the action (and insert to the table) if possible
            if (int)(splittedline[1]) < 0 :
                product = repo.products.find(id = splittedline[0])
                toSale = (int)(splittedline[1])
                if ( -1*toSale <= product[0].quantity) :
                    newQuantity = product[0].quantity + (int)(splittedline[1])
                    repo.products.update(newQuantity,splittedline[0])
                    activity = Activitie(splittedline[0], splittedline[1], splittedline[2], splittedline[3])
                    repo.activities.insert(activity)
            
            elif (int)(splittedline[1]) > 0:
                product = repo.products.find(id = splittedline[0])
                newQuantity = product[0].quantity + (int)(splittedline[1])
                repo.products.update(newQuantity,splittedline[0])
                activity = Activitie(splittedline[0], splittedline[1], splittedline[2], splittedline[3])
                repo.activities.insert(activity)
                
if __name__ == '__main__':
    main(sys.argv)