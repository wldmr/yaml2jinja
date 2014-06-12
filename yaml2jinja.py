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

    parser.add_argument('-v', '--variants',
        action=CommaSeparatedList,
        help=("If a template variable or expression is a dict, "
              "try the keys given here, in the given order. "
              "If it is a tuple of the form ('v1:Hello', 'v2:Hallo'), "
              "then convert it to a dict {'v1': 'Hello', 'v2': Hallo'} first."))

    return parser.parse_args()


env = jinja2.Environment(
    loader=jinja2.FileSystemLoader('.'),
    extensions=['jinja2.ext.with_'],
    block_start_string='{%',
    block_end_string='%}',
    variable_start_string='{{',
    variable_end_string='}}',
    comment_start_string='{#',
    comment_end_string='#}',
    line_statement_prefix='::',
    line_comment_prefix='##',
    trim_blocks=True,
    lstrip_blocks=True,
)


def select_variant(keys):
    if not keys:
        return lambda expr: expr

    def func(expr):
        if isinstance(expr, tuple):
            pairs = (item.split(":", 1) for item in expr)
            expr = dict(pairs)

        if isinstance(expr, dict):
            for key in keys:
                if key in expr:
                    return expr[key]

        return expr

    return func
if __name__ == '__main__':
    args = get_arguments()
    data = yaml.load(open(args.data))
    env.globals['variants'] = args.variants
    env.finalize = select_variant(args.variants)
    env.filters['select_variant'] = env.finalize
    template = env.get_template(args.template)
    output = template.render(data=data).encode("utf8")
    sys.stdout.write(output)

