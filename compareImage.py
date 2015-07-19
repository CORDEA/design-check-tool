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

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2015-07-19"

from PIL import Image
import sys

def checkImage(srName, trName, loose=0):
    srData = Image.open(srName)
    trData = Image.open(trName)

    srPix = list(srData.getdata())
    trPix = list(trData.getdata())

    x, y = srData.size

    rsList = []
    for j in range(x * y):
        if srPix[j] != trPix[j]:
            out = True
            if loose != 0:
                for i in range(3):
                    dif = abs(trPix[j][i] - srPix[j][i])
                    if dif > loose:
                        out = False
            if out:
                tpl = list(srPix[j])
                tpl[2] = 255
                rsList.append(tuple(tpl))
            else:
                rsList.append(srPix[j])
        else:
            rsList.append(srPix[j])

    rs = Image.new("RGB", srData.size)
    rs.putdata(rsList)
    rs.save("aaa.png")

if __name__=='__main__':
    checkImage(sys.argv[1], sys.argv[2])
