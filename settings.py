import os.path as op
DEBUG = True
DIRNAME = '/'.join(op.dirname(__file__).split('/')[:-1])
STATIC_PATH = op.join(DIRNAME, 'web')
TEMPLATE_PATH = op.join(DIRNAME, 'web')

import logging as log
import sys
#log linked to the standard error stream
log.basicConfig(level=log.DEBUG,
    format='%(asctime)s - %(levelname)-8s - %(message)s',
    datefmt='%d/%m/%Y %Hh%Mm%Ss')
console = log.StreamHandler(sys.stderr)
log.warning('DIRNAME: %s'%DIRNAME)

COOKIE_SECRET = 'L8LwECiNRxq2N0N2eGxx9MZlrpmuMEimlydNX/vt1LM='
