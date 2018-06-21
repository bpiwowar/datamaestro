#!/usr/bin/env python3

import argparse
import sys
import logging
import os.path as op
import yaml
from functools import update_wrapper

from .xpm import ExperimaestroEncoder

from .context import Context
from .data import Dataset

import click

logging.basicConfig(level=logging.INFO)


def pass_cfg(f):
    """Pass configuration information"""
    @click.pass_context
    def new_func(ctx, *args, **kwargs):
        return ctx.invoke(f, ctx.obj, *args, **kwargs)
    return update_wrapper(new_func, f)

# --- Create the argument parser

@click.group()
@click.option("--quiet", is_flag=True, help="Be quiet")
@click.option("--debug", is_flag=True, help="Be even more verbose (implies traceback)")
@click.option("--traceback", is_flag=True, help="Display traceback if an exception occurs")
@click.option("--data", type=click.Path(exists=True), help="Directory containing datasets", default=Context.MAINDIR)
@click.pass_context
def cli(ctx, quiet, debug, traceback, data):
    if quiet:
        logging.getLogger().setLevel(logging.WARN)
    elif debug:
        logging.getLogger().setLevel(logging.DEBUG)


    ctx.obj = Context(data)

def main():
    cli(obj=None)

@cli.command(help="Prints the full information about a dataset")
@click.argument("dataset", type=str)
@pass_cfg
def info(cfg, dataset):
    dataset = Dataset.find(cfg, dataset)
    print(dataset.description())
    print(dataset.tags())



# --- Web site

@cli.group()
def site():
    pass

@site.command()
@pass_cfg
def generate(cfg):
    import datasets.commands.site as site
    site.generate(cfg)

@site.command()
@pass_cfg
def serve(cfg):
    import datasets.commands.site as site
    site.serve(cfg)


# --- prepare and download

@click.argument("dataset")
@cli.command()
@pass_cfg
def download(cfg, dataset):
    dataset = Dataset.find(cfg, dataset)
    success = dataset.download()
    if not success:
        logging.error("One or more errors occured while downloading the dataset")
        sys.exit(1)


@click.argument("datasetid")
@cli.command(help="Downloads a dataset (if freely available)")
@pass_cfg
def prepare(cfg, datasetid):
    dataset = cfg.dataset(datasetid)
    success = dataset.download()
    if not success:
        logging.error("One or more errors occured while downloading the dataset")
        sys.exit(1)

    s = dataset.prepare()
    try: 
        print(ExperimaestroEncoder().encode(s))
    except:
        logging.error("Error encoding to JSON: %s", s)
        sys.exit(1)
    
  


# --- Search

@click.argument("searchterms",  nargs=-1) #, description="Search terms (e.g. tag:XXX)")
@cli.command(help="Search for a dataset")
@pass_cfg
def search(cfg, searchterms):
    from .search import Condition, AndCondition

    condition = AndCondition()
    for searchterm in searchterms:
        condition.append(Condition.parse(searchterm))

    for dataset in cfg.datasets():
        if condition.match(dataset):
            print(dataset)


