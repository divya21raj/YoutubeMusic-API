from yt_music import YtMusic
from utils.parser import parser

# Parsing the program arguments
args = parser.parse_args()

ytm = YtMusic()

# Login if necessary
if(args.login): ytm.googleLogin()

# Command passed in '-F' or '--function'
command = args.function.strip()

# Executing Command
ytm.command_dict[command]()


