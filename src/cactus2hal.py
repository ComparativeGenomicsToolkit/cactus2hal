#!/usr/bin/env python

########################################################################
# File:cactus2HAL.py
# 
# Purpose: Extracts addresses and database information for all files in a cactus project that
#need to be converted to HAL.
#          
#          
# Author: Glenn Hickey & Vlado Uzunangelov
# History: 4/18/2012 Created
#               
########################################################################

import argparse,sys,os
import xml.etree.ElementTree as ET
from cactus.progressive.multiCactusProject import MultiCactusProject
from cactus.progressive.multiCactusTree import MultiCactusTree
from cactus.progressive.experimentWrapper import ExperimentWrapper


class CommandLine(object) :
    
    
    def __init__(self) :
        
        self.parser = argparse.ArgumentParser(description = 'Extracts path information for all files \
                                               that need to be converted to the HAL format and initiates\
                                               their conversion. The input path information comes as an \
                                               xml file. ', 
                                             add_help = True, #default is True 
                                             prefix_chars = '-')
        self.parser.add_argument('xml_list', type=argparse.FileType('r'), action = 'store', 
                                 help="xml file of all alignments that need to be parsed")
        self.parser.add_argument('HAL_file_path', type=str, action = 'store', 
                                 help="file path where newly created HAL file is to be stored.")
        self.args = vars(self.parser.parse_args())
        
      
########################################################################
# Main
########################################################################
def main():
    myComLine=CommandLine() 
    myProj=MultiCactusProject()
    myProj.readXML(myComLine.args['xml_list'])
    
    for genomeName in myProj.expMap.keys():

        experimentFilePath = myProj.expMap[genomeName]
        experimentFileXML = ET.parse(experimentFilePath).getroot()
        experimentObject = ExperimentWrapper(experimentFileXML)
        # naming is a bit out of date.
        HALSegmentFilePath = experimentObject.getMAFPath()
        # access into cactus
        dbString = experimentObject.getDiskDatabaseString()
        
        # pass them to the c parser, parse them in there
        os.system('../bin/importCactusIlntoHAl -m {} -d {} -h{}'.format(
                                                                   HALSegmentFilePath,
                                                                   dbString,
                                                                   myComLine.args['HAL_file_path']))
        
#    testing output - will remove those when system call put in   
    print genomeName
    print experimentFilePath
    print experimentFileXML
    print experimentObject
    print HALSegmentFilePath
    print dbString
    
    
              
      
if __name__ == "__main__":
    main();
    raise SystemExit 