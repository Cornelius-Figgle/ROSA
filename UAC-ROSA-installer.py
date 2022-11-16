#pyinstaller --distpath "t:\projects\rosa\bin\bin" --workpath "t:\projects\rosa\bin\build" -F -n ROSA-installer_uac --paths "T:\projects\ROSA\rosa-env\Lib\site-packages" --uac-admin --hidden-import pyi_splash --splash "T:\projects\ROSA\ico\hotpot-ai.png" -i "T:\projects\ROSA\ico\hotpot-ai.ico" "T:\projects\ROSA\UAC-ROSA-installer.py"

#https://github.com/Cornelius-Figgle/ROSA/
#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX HARRISON, AS OF 2022
It may work separately and independently of the main repo, it may not. Who knows

Code (c) Max Harrison 2022
Ideas (c) Callum Blumfield 2022
Ideas (c) Max Harrison 2022
Vocals (c) Evie Peacock 2022

Thanks also to Alex, Ashe & Jake for support throughout (sorry for the spam)
Extra thanks to all the internet peoples that helped with this as well 
'''

import os
import pickle
import shutil
import sys

if hasattr(sys, '_MEIPASS'): #https://stackoverflow.com/a/66581062/19860022
	file_base_path = sys.argv[0] #https://stackoverflow.com/a/36343459/19860022
else:
	file_base_path = os.path.dirname(__file__)

#________________________________________________________________________________________________________________________________

def uac_procs(installConfigs: dict, downloadedFiles: dict) -> None:
	os.mkdir(os.path.join(installConfigs['programPath'], 'ROSA')) #admin
	#os.mkdir(os.path.join(installConfigs['dataPath'], 'ROSA')) #admin

	shutil.move(downloadedFiles['bin'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['bin']))) #admin
	shutil.move(downloadedFiles['config'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['config']))) #admin
	shutil.move(downloadedFiles['readme'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['readme']))) #admin

def main(config_pk: str, dwld_pk: str) -> None:
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

	print('starting UAC script')
	main(sys.argv[1], sys.argv[2])
