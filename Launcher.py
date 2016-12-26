from argparse import ArgumentParser, RawDescriptionHelpFormatter
import Husky

def PrintTerms():
    pass

def PrintSolvers():
    pass

HELP = {
    'help':'To print useful information about Husky'
    'test':'Run all tests'
}

def main():
    parser = ArgumentParser(description=__doc__,format_class=RawDescriptionHelpFormatter)
    parser.add_argument('--version',action='version',version='%(prog)s '+Husky.__version__)

    pass #ToDO

if __name__ == '__main__':
    main()