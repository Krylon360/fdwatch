#!/usr/bin/python

# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8

"""
Copyright (c) 2014 Janne Blomqvist

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Plot the number of open file descriptors vs. time. Generate an input
file with the fdwatch "-p" option.

"""


import matplotlib.pyplot as plt
import sys
import numpy as np

d = np.loadtxt(sys.argv[1])
dt = d[:,0] - d[0, 0]
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(dt, d[:,1])
plt.xlabel('Time (s)')
plt.ylabel('Open file descriptors')
plt.show()
