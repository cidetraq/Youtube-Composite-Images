import image_packer
import combine
import download
import subprocess
import os

dimensions=(4000,4000)
d=download.getInfo()
image_packer.resize(d,dimensions)
#image_packer.run(dimensions)
#combine.equalSizedComposite()