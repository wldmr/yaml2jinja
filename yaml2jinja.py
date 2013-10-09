#!/bin/env python
# encoding: utf-8

import sys

import yaml
import jinja2

data = yaml.load(open(sys.argv[1]))
template = jinja2.Template(open(sys.argv[2]).read())

output = template.render(data=data).encode("utf8")
sys.stdout.write(output)
