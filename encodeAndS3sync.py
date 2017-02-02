import json
import os
import ntpath
import datetime as dt
import pprint

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
	Note, directories and files with the wrong extension type are ignored.
	'''
	now = dt.datetime.now()
	content_dir = config['content']
	ext = config['content_ext']
	if max_age_in_hours <= 0:
		cutoff = dt.datetime.min
	else:
		cutoff = now-dt.timedelta(hours=max_age_in_hours)
	def is_new_file(fname):
		path = os.path.join(content_dir, fname)
		st = os.stat(path)
		mtime = dt.datetime.fromtimestamp(st.st_mtime)
		return mtime > cutoff and os.path.isfile(path) and path.endswith('.'+ext)
		
	files = os.listdir(content_dir)
	files = [os.path.join(content_dir, fname) for fname in files if is_new_file(fname)]
	print("Found %d new files" % len(files))
	return files

def get_encoding_filemap(config, files):
	'''
	Get a dictionary of pointing from files to encode, to 
	where these should be saved
	'''
	encoded_dir = config['encoded']
	ext = '.' + config['encoded_ext']
	result = {}
	for ifname in files:
		path, fname = ntpath.split(ifname)
		ofname = os.path.join(encoded_dir, fname.split('.')[0] + ext)
		result[ifname] = ofname
	return result
	
def encode_files(config, filesmap):
	'''
	Save each file with line breaks replaced by spaces
	'''
	pass
	
if __name__ == '__main__':
	pp = pprint.PrettyPrinter(indent=4)
	config = get_config()
	print("\nconfig:")
	pp.pprint(config)
	
	new_files = get_new_files(config, max_age_in_hours=24)
	print("\nnew files:")
	pp.pprint(new_files)
	
	encoding_filemap = get_encoding_filemap(config, new_files)
	print("\nfile encoding map:")
	pp.pprint(encoding_filemap)
	
#    try:
#        auto.run()
#    except KeyboardInterrupt:
#        # We're done. Bail out without dumping a traceback.
#        sys.exit(0)