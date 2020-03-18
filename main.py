from yt_music import YtMusic
from parser import parser

# Parsing the program arguments
args = parser.parse_args()

ytm = YtMusic()

# Login if necessary
if(args.login): ytm.googleLogin()

# Command passed in '-F' or '--function'
command = args.function

# Executing Command
ytm.command_dict[command]()


