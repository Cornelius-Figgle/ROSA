import os

if os.name == 'nt':
	from pathlib import Path

	import pythoncom
	from win32com.client import Dispatch

def make_shortcut(source, dest_dir, dest_name=None, linux_file=False) -> None:
		'''
		Make shortcut of `source` path to file in `dest_dir` target folder
		If `dest_name` is None, will use `source`'s filename
		'''

		# process user input
		if dest_name is None:
			dest_name = Path(source).name
		dest_path = str(Path(dest_dir, dest_name))# + '.lnk' # `~/.local/share/applications/ROSA` on linux

		if not os.path.exists(dest_path):
			print(f'creating dirs "{dest_dir}"')
			#self.infoLabel.setText(f'creating dirs "{dest_dir}"')

			os.makedirs(dest_dir, exist_ok=True)

			print(f'creating shortcut at "{dest_path}"')
			#self.infoLabel.setText(f'creating shortcut at "{dest_path}"')
			
			if os.name == 'nt':
				dest_path = os.path.splitext(dest_path)[0] + '.lnk'
				# make shortcut
				shell = Dispatch('WScript.Shell')
				shortcut = shell.CreateShortCut(dest_path)
				shortcut.IconLocation = source
				shortcut.Targetpath = source
				shortcut.WorkingDirectory = dest_dir
				shortcut.save()
			elif os.name == 'posix':
				if linux_file:
					dest_path = dest_path + '.desktop' # `~/.local/share/applications/ROSA.desktop`

					shortcutContent = f'''
					[Desktop Entry]
					Name=ROSA
					Exec={os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(self.downloadedFiles['bin']))}
					Terminal=true
					Type=Application
					Icon={os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(self.downloadedFiles['png']))}
					'''
					with open(dest_path, 'w') as f:
						f.write(shortcutContent)
				else: 
					os.symlink(source, dest_path)
			# print status
			print(f'{source}\n-->\n{dest_path}')
			#self.infoLabel.setText(f'{source}\n-->\n{dest_path}')

			print(f'created shortcut at "{dest_path}"')
			#self.infoLabel.setText(f'created shortcut at "{dest_path}"')

if __name__ == '__main__': 
    make_shortcut('T:\\projects\\ROSA\\ROSA-installer.py', os.path.expandvars('%AppData%\\Microsoft\\Windows\\Start Menu\\Programs\\ROSA'))