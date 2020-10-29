from argparse import ArgumentParser
from pywaterml import __version__

def cli(args=None):
    p = ArgumentParser(
        description="The pywaterml is a package that lets you handle WaterML functions such as GetValues, GetSitesInfo, etc. In addition it lets offers extra functions such as mean interpolation for data with gaps",
        conflict_handler='resolve'
    )
    p.add_argument(
        '-V', '--version',
        action='version',
        help='Show the conda-prefix-replacement version number and exit.',
        version="pywaterml %s" % __version__,
    )

    args = p.parse_args(args)

    # do something with the args
    print("CLI template - fix me up!")

    # No return value means no error.
    # Return a value of 1 or higher to signify an error.
    # See https://docs.python.org/3/library/sys.html#sys.exit


if __name__ == '__main__':
    import sys
    cli(sys.argv[1:])
