#!/bin/bash

wget --header='Content-Type: text/plain' --post-file=mary.txt http://localhost:5121 -O - -nv
