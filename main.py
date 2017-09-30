import image_packer
import combine
import download
import subprocess
import os

dimensions=(1080,1080)
d=download.getInfo()
image_packer.resize(d,dimensions)
image_packer.run(dimensions)
#combine.equalSizedComposite()