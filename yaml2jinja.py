#!/bin/env python
# encoding: utf-8

import sys

import yaml
import jinja2


env = jinja2.Environment(
    loader=jinja2.PackageLoader('yaml2jinja', '.'),
    extensions=['jinja2.ext.with_']
)

def sort(value, key=None):
    return sorted(value, key=lambda v: v[key])
env.filters['sort'] = sort


if __name__ == '__main__':
    data = yaml.load(open(sys.argv[1]))
    template = env.get_template(sys.argv[2])
    output = template.render(data=data).encode("utf8")
    sys.stdout.write(output)

