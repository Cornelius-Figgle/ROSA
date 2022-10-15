import os
import pickle
import shutil
import sys

if hasattr(sys, '_MEIPASS'): #https://stackoverflow.com/a/66581062/19860022
	file_base_path = sys.argv[0] #https://stackoverflow.com/a/36343459/19860022
else:
	file_base_path = os.path.dirname(__file__)

#________________________________________________________________________________________________________________________________

def uac_procs(installConfigs, downloadedFiles) -> None:
	os.mkdir(os.path.join(installConfigs['programPath'], 'ROSA')) #admin
	os.mkdir(os.path.join(installConfigs['dataPath'], 'ROSA')) #admin

	shutil.move(downloadedFiles['bin'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['bin']))) #admin
	shutil.move(downloadedFiles['config'], os.path.join(installConfigs['dataPath'], 'ROSA', os.path.basename(downloadedFiles['config']))) #admin
	shutil.move(downloadedFiles['readme'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['readme']))) #admin

def main(config_pk, dwld_pk) -> None:
	print('starting pickle loads')

	with open(config_pk) as file: #os.path.join(file_base_path, 'installConfigs.pickle'), 'rb') as file:
		installConfigs = pickle.load(file)
	os.remove(os.path.join(file_base_path, 'installConfigs.pickle'))
	with open(dwld_pk) as file: #os.path.join(file_base_path, 'downloadedFiles.pickle'), 'rb') as file:
		downloadedFiles = pickle.load(file)
	os.remove(os.path.join(file_base_path, 'downloadedFiles.pickle'))

	print('finished pickle loads')

	for i in installConfigs:
		print(f'installConfigs[{i}] is {installConfigs[i]}')
	for i in downloadedFiles:
		print(f'downloadedFiles[{i}] is {downloadedFiles[i]}')

	uac_procs(installConfigs, downloadedFiles)

#________________________________________________________________________________________________________________________________

if __name__ == '__main__':
	if '_PYIBoot_SPLASH' in os.environ:# and importlib.util.find_spec('pyi_splash'):
		from pyi_splash import close, update_text  # type: ignore
		update_text('UI Loaded...')
		close()
	main(sys.argv[1], sys.argv[2])
