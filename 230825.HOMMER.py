#!/usr/bin/python3

import os

def HOMMER():
    command = f'findMotifsGenome.pl Result/02.Bed/Hyper.DMR.bed hg19 Result/03.HOMER/00.Hyper'
    os.system(command)

    command = f'findMotifsGenome.pl Result/02.Bed/Hypo.DMR.bed hg19 Result/03.HOMER/01.Hypo'
    os.system(command)

HOMMER()