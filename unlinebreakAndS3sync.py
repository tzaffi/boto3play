import json
import os

if __name__ == '__main__':
	import sys

	with open('config.json', 'r') as config_file:
		config = json.load(config_file)
		print(config)
	
#    try:
#        auto.run()
#    except KeyboardInterrupt:
#        # We're done. Bail out without dumping a traceback.
#        sys.exit(0)