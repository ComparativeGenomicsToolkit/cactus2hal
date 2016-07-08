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

import argparse,sys,os,subprocess,time

import xml.etree.ElementTree as ET
from cactus.progressive.multiCactusProject import MultiCactusProject
from cactus.progressive.multiCactusTree import MultiCactusTree
from cactus.shared.experimentWrapper import ExperimentWrapper
from sonLib.bioio import system
from sonLib.nxnewick import NXNewick
from toil.job import Job

def initParser():
    parser = argparse.ArgumentParser(description = 'Convert Cactus database to HAL database ', 
                                          add_help = True, #default is True 
                                          prefix_chars = '-')
    parser.add_argument('cactus_project', type=argparse.FileType('r'), action = 'store', 
                             help="cactus project xml file")
    parser.add_argument('HAL_file_path', type=str, action = 'store', 
                             help="file path where newly created HAL file is to be stored.")
    parser.add_argument('--event', type=str, action = 'store', default=None,
                        help='root event of the input phylogeny')
    parser.add_argument('--cacheBytes', type=int, default=None,
                      help="maximum size in bytes of regular hdf5 cache")
    parser.add_argument('--cacheMDC', type=int, default=None,
                      help="number of metadata slots in hdf5 cache")
    parser.add_argument('--cacheRDC', type=int, default=None,
                      help="number of regular slots in hdf5 cache")
    parser.add_argument('--cacheW0', type=int, default=None,
                      help="w0 parameter for hdf5 cache")
    parser.add_argument('--chunk', type=int, default=None,
                      help="hdf5 chunk size")
    parser.add_argument('--deflate', type=int, default=None,
                      help="hdf5 compression factor")
    parser.add_argument('--inMemory', action = 'store_true', default=False,
                      help="keep entire hdf5 arrays in memory, overriding"
                        " the cache.")
    parser.add_argument('--append', action='store_true', default=False,
                        help='append to an existing hal file instead of '
                        'overwriting')
    Job.Runner.addToilOptions(parser)

    return vars(parser.parse_args())
        
########################################################################
# Main
########################################################################

def exportHal(job, project, event=None, cacheBytes=None, cacheMDC=None, cacheRDC=None, cacheW0=None, chunk=None, deflate=None, inMemory=False):

    # some quick stats
    totalTime = time.time()
    totalAppendTime = 0

    HALPath = os.path.join(job.fileStore.getLocalTempDir(), "tmp.hal")

    # traverse tree to make sure we are going breadth-first
    tree = project.mcTree

    # find subtree if event specified
    rootNode = None
    if event is not None:
        assert event in tree.nameToId and not tree.isLeaf(tree.nameToId[event])
        rootNode = tree.nameToId[event]

    for node in tree.breadthFirstTraversal(rootNode):
        genomeName = tree.getName(node)
        if genomeName in project.expMap:
            experimentFilePath = job.fileStore.readGlobalFile(project.expIDMap[genomeName])
            experiment = ExperimentWrapper(ET.parse(experimentFilePath).getroot())

            outgroups = experiment.getOutgroupEvents()
            expTreeString = NXNewick().writeString(experiment.getTree())
            assert len(expTreeString) > 1
            assert experiment.getHalID() is not None
            assert experiment.getHalFastaID() is not None
            subHALPath = job.fileStore.readGlobalFile(experiment.getHalID())
            halFastaPath = job.fileStore.readGlobalFile(experiment.getHalFastaID())

            cmdline = "halAppendCactusSubtree \'{0}\' \'{1}\' \'{2}\' \'{3}\'".format(subHALPath, halFastaPath, expTreeString, HALPath)
            
            if len(outgroups) > 0:
                cmdline += " --outgroups {0}".format(",".join(outgroups))
            if cacheBytes is not None:
                cmdline += " --cacheBytes {0}".format(cacheBytes)
            if cacheMDC is not None:
                cmdline += " --cacheMDC {0}".format(cacheMDC)
            if cacheRDC is not None:
                cmdline += " --cacheRDC {0}".format(cacheRDC)
            if cacheW0 is not None:
                cmdline += " --cacheW0 {0}".format(cacheW0)
            if chunk is not None:
                cmdline += " --chunk {0}".format(chunk)
            if deflate is not None:
                cmdline += " --deflate {0}".format(deflate)
            if inMemory is True:
                cmdline += " --inMemory"

            
            print cmdline
            #appendTime = time.time()
            system(cmdline)
            #appendTime = time.time() - appendTime
            #totalAppendTime += appendTime
#            print "time of above command: {0:.2f}".format(appendTime)
 
    #totalTime = time.time() - totalTime
    #print "total time: {0:.2f}  total halAppendCactusSubtree time: {1:.2f}".format(totalTime, totalAppendTime)
    return job.fileStore.writeGlobalFile(HALPath)

def main():
    args = initParser()
    myProj = MultiCactusProject()
    myProj.readXML(args['cactus_project'])

    if not args['append']:
        # Overwrite existing hal
        print 'rm -f {0}'.format(args['HAL_file_path'])
        system('rm -f {0}'.format(args['HAL_file_path']))
    event = args['event']
    HALPath = args['HAL_file_path']
    with Toil(args) as toil:
        toil.start(Job.wrapJobFn(exportHal, myProj, HALPath, event=event))

                             
if __name__ == "__main__":
    main();
    raise SystemExit 
