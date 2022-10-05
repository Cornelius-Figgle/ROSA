import os
import pickle
import shutil

#________________________________________________________________________________________________________________________________

def uac_procs(installConfigs, downloadedFiles) -> None:
	os.mkdir(os.path.join(installConfigs['programPath'], 'ROSA')) #admin
	os.mkdir(os.path.join(installConfigs['dataPath'], 'ROSA')) #admin

	shutil.move(downloadedFiles['bin'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['bin']))) #admin
	shutil.move(downloadedFiles['config'], os.path.join(installConfigs['dataPath'], 'ROSA', os.path.basename(downloadedFiles['config']))) #admin
	shutil.move(downloadedFiles['readme'], os.path.join(installConfigs['progamPath'], 'ROSA', os.path.basename(downloadedFiles['readme']))) #admin

def main() -> None:
	with open(os.path.join(os.path.dirname(__file__), 'installConfigs.pickle'), 'rb') as file:
		installConfigs = pickle.load(file)
	os.remove(os.path.join(os.path.dirname(__file__), 'installConfigs.pickle'))
	with open(os.path.join(os.path.dirname(__file__), 'downloadedFiles.pickle'), 'rb') as file:
		downloadedFiles = pickle.load(file)
	os.remove(os.path.join(os.path.dirname(__file__), 'downloadedFiles.pickle'))

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
	main()
