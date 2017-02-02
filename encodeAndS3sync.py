import json
import os
import datetime as dt

def get_config():
	'''
	Load the configuration from ./config.json
	'''
	with open('config.json', 'r') as config_file:
		return json.load(config_file)

def get_new_files(config, max_age_in_hours=24):
	'''
	Get array of all files younger than max_age_in_hours, 
	unless max_age_in_hours is set to 0 - in which case all files
	are provided.
	'''
	now = dt.datetime.now()
	content_dir = config['content']
	if max_age_in_hours <= 0:
		cutoff = dt.datetime.min
	else:
		cutoff = now-dt.timedelta(hours=max_age_in_hours)
	def is_new_file(fname):
		path = os.path.join(content_dir, fname)
		st = os.stat(path)
		mtime = dt.datetime.fromtimestamp(st.st_mtime)
		return mtime > cutoff
		
	files = os.listdir(content_dir)
	files = [os.path.join(content_dir, fname) for fname in files if is_new_file(fname)]
	print("Found %d new files" % len(files))
	return files
			
if __name__ == '__main__':
	config = get_config()
	print(config)
	
	new_files = get_new_files(config, max_age_in_hours=24)
	print(new_files)
	
#    try:
#        auto.run()
#    except KeyboardInterrupt:
#        # We're done. Bail out without dumping a traceback.
#        sys.exit(0)