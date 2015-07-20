#!/usr/bin/env python
# encoding:utf-8
#
# Copyright [2015] [Yoshihiro Tanaka]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__Author__  =   "Yoshihiro Tanaka"
__date__    =   "2015-07-19"
__version__ =   "0.1 (Beta)"

from PIL import Image
import sys
from optparse import OptionParser

def optSettings():
    usage = ""
    version = __version__
    parser = OptionParser(usage=usage, version=version)

    parser.add_option(
            "-l", "--loose",
            action = "store",
            dest  = "loose",
            type = int,
            default = 0
            )

    parser.add_option(
            "-r", "--reversal",
            action = "store_false",
            dest = "reversal",
            )

    parser.add_option(
            "-c", "--color",
            action = "store",
            dest = "color",
            type = str,
            default = "r"
            )

    return parser.parse_args()

class CompareImages:
    def __init__(self, options, args):
        self._LOOSE     = options.loose
        self._REV       = options.reversal
        self._COLOR     = options.color
        if self._COLOR not in ['r', "red", 'g', "green", 'b', "blue"]:
            sys.stderr.write("[WARNING] " + self._COLOR + " does not match the format. Therefore, use the default value. format: r, red, g, green, b, blue\n")
            self._COLOR = 'r'

        self._SOURCE    = args[0]
        self._TARGET    = args[1]

    def checkImage(self, srName, trName):
        loose = self._LOOSE
        rev = self._REV
        color = self._COLOR

        srData = Image.open(srName)
        trData = Image.open(trName)

        srPix = list(srData.getdata())
        trPix = list(trData.getdata())

        trData = self.checkSize(srData.size, trData)

        x, y = srData.size

        rsList = []
        for j in range(x * y):
            if srPix[j] != trPix[j]:
                out = True
                if loose != 0:
                    for i in range(3):
                        dif = abs(trPix[j][i] - srPix[j][i])
                        if dif < loose:
                            out = False
                if out:
                    if rev:
                        rsList.append(tuple([(255 - r) for r in srPix[j]]))
                    else:
                        colorTpl = (255, 0, 0)
                        if color in ['g', "green"]:
                            colorTpl = (0, 255, 0)
                        elif color in ['b', "blue"]:
                            colorTpl = (0, 0, 255)
                        rsList.append(colorTpl)
                else:
                    rsList.append(srPix[j])
            else:
                rsList.append(srPix[j])

        rs = Image.new("RGB", srData.size)
        rs.putdata(rsList)
        rs.save("aaa.png")

    def checkSize(self, srSize, trData):
        srX, srY  = srSize
        trX, trY  = trData.size

        if (srX / float(srY)) != (trX / float(trY)):
            sys.exit("Aspect ratio does not match.")

        if srX != trX and srY != trY:
            trData = trData.resize(srData.size)

        return trData

if __name__=='__main__':
    options, args = optSettings()
    ci = CompareImages(options, args)
    ci.checkImage(sys.argv[1], sys.argv[2])
