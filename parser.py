import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-L', '--login', action="store_true", help='Login through your Google Account. Create a creds.json file in the project root directory with \'username\' and \'password\' keys.')
parser.add_argument('-F', '--function', help='Specify the function you want to perform')