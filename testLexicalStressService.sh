#!/bin/bash

wget --header='Content-Type: text/plain' --post-file=mary.txt http://198.211.105.27:5121 -O - -nv
