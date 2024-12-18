import igv_remote
import os
#--------------------------------------------------------------------------------------#
ir = igv_remote.IGV_remote()

ir.connect()

ir.load('/media/node02-HDD01/00.BPDCN/bpdcn_chh_001/03.Align/bpdcn_chh_001.bam')

ir.goto('chr17', 7568000, 7569000)

ir.set_saveopts(img_dir = "/media/node02-HDD01/00.BPDCN/", img_basename = "BPDCN1.png" ) # must be set!

ir.snapshot()

ir.close()
