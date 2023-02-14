import os
import shutil

from requests import get


def download_file(url) -> str:
		local_dirname = os.path.join(os.path.dirname(__file__), 'temp_dwld')
		local_filename = os.path.join(local_dirname, url.split('/')[-1])

		print(f'creating dirs "{local_dirname}"')
		#self.infoLabel.setText(f'creating dirs "{local_dirname}"')

		os.makedirs(local_dirname, exist_ok=True)

		print(f'starting download for "{local_filename}"')
		#self.infoLabel.setText(f'starting download for "{local_filename}"')

		with get(url, stream=True) as r:
			with open(local_filename, 'w') as f:
				f.write(r.text)

		print(f'finished download for "{local_filename}"')
		#self.infoLabel.setText(f'finished download for "{local_filename}"')

		return local_filename


if __name__ == '__main__':
	print(download_file('https://raw.githubusercontent.com/Cornelius-Figgle/ROSA/main/bin/UAC-ROSA-installer%5Bwin%5D.py'))