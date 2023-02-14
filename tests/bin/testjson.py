import os
import pickle

installConfigs = {
  'brand': 'Ford',
  'model': 'Mustang',
  'year': 1964
}

downloadedFiles = {
  'brand': 'Ford',
  'model': 'Mustang',
  'year': 1964
}

#json_Configs = '\'' + json_Configs + '\''
#json_Dwlds = '\'' + json_Dwlds + '\''

if os.name == 'nt': 
	with open(os.path.join(os.path.dirname(__file__), 'installConfigs.pickle'), 'wb') as file:
		pk1 = pickle.dump(installConfigs, file)
	with open(os.path.join(os.path.dirname(__file__), 'downloadedFiles.pickle'), 'wb') as file:
		pk2 = pickle.dump(downloadedFiles, file)
	os.system(f'{downloadedFiles["adm"]} {pk1} {pk2}')
