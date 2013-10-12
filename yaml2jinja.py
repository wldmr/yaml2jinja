#!/bin/env python
# encoding: utf-8

import sys

import yaml
import jinja2


def get_arguments():
    import argparse  # Python 2.7 dependency

    class CommaSeparatedList(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            splitvals = [v.strip() for v in values.split(',')]
            setattr(namespace, self.dest, splitvals)

    parser = argparse.ArgumentParser()
    parser.add_argument("data",
        help=("The data in YAML format. "
              "Will be made available to the template "
              "through the 'data' variable."))
    parser.add_argument("template",
        help=("The template in Jinja2 syntax."))

    parser.add_argument('-t', '--try-keys',
        action=CommaSeparatedList,
        help="If a Jinja2 variable is a dict, try the keys given here, in order.")

    return parser.parse_args()


env = jinja2.Environment(
    loader=jinja2.PackageLoader('yaml2jinja', '.'),
    extensions=['jinja2.ext.with_']
)

def sort(value, key=None):
    return sorted(value, key=lambda v: v[key])
env.filters['sort'] = sort


if __name__ == '__main__':
    args = get_arguments()
    data = yaml.load(open(args.data))
    data = yaml.load(open(sys.argv[1]))
    template = env.get_template(sys.argv[2])
    template = env.get_template(args.template)
    output = template.render(data=data).encode("utf8")
    sys.stdout.write(output)

