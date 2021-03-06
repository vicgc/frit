#!/usr/bin/python
"""
mmls support. A good way to find unused sectors.
"""

import subprocess
import os
import os.path
import fritutils.termout
import fritutils.fritlog
from fritutils.fritglobals import *

logger = fritutils.fritlog.loggers['sectorsLog']

def ddump(container,start,end,destination):
    """
    This function is used by Evidences objects to dump specified sectors of a raw file
    """
    if os.path.exists(container):
        ifoption = 'if=' + container
        ofoption = 'of=' + destination
        convoption = 'conv=sync,noerror'
        seekoption = 'seek=' + str(start)
        countoption = 'count=' + str(end-start)
        dd = subprocess.Popen([DD, ifoption, ofoption, seekoption, countoption, convoption], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        dd.wait()

def affcat(container,start,end,destination):
    """
    This function is used by AFF Evidences objects to dump specified sectors of a raw file
    """
    if os.path.exists(container):
        outfile = open(destination,'w')
        c = (end-start) * 512
        s = start * 512
        roption = str(s) + ':' + str(c)
        affcat = subprocess.Popen([AFFCAT, '-r', roption, container], stdout=outfile, stderr=subprocess.PIPE)
        affcat.wait()
        outfile.close()

def ewfexport(container,start,end,destination):
    """
    This function is used by EWF evidences objects to dump specified sectors of a raw file.
    """
    if os.path.exists(container):
        nbytes = str((end-start) * 512)
        offset = str(start * 512)
        ewfexport = subprocess.Popen([EWFEXPORT, '-u', '-q', '-B', nbytes, '-f','raw', '-o', offset, '-t', destination, container], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ewfexport.wait()
        # renaming destination because ewfexport automatically append a ".raw" extension to the file.
        ewfname = destination + '.raw'
        if os.path.exists(ewfname):
            logger.info('Renaming "%s" in "%s"' % (ewfname,destination))
            os.rename(ewfname,destination)
        else:
            logger.warning('File "%s" not found, cannot rename it' % ewfname)

