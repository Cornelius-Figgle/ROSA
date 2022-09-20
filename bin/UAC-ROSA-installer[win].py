import os
import shutil
from getopt import GetoptError, getopt
from msvcrt import getwch
from sys import argv

#________________________________________________________________________________________________________________________________

print(argv[1:])

#________________________________________________________________________________________________________________________________

def uac_procs(installConfigs, downloadedFiles) -> None:
    os.mkdir(os.path.join(installConfigs['programPath'], 'ROSA')) #admin
    os.mkdir(os.path.join(installConfigs['dataPath'], 'ROSA')) #admin
    os.mkdir(os.path.join(installConfigs['readPath'], 'ROSA')) #admin

    shutil.move(downloadedFiles['bin'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['bin']))) #admin
    shutil.move(downloadedFiles['config'], os.path.join(installConfigs['dataPath'], 'ROSA', os.path.basename(downloadedFiles['config'])))
    shutil.move(downloadedFiles['readme'], os.path.join(installConfigs['readPath'], 'ROSA', os.path.basename(downloadedFiles['readme']))) #admin
    if os.name == 'posix':
        shutil.move(downloadedFiles['png'], os.path.join(installConfigs['programPath'], 'ROSA', os.path.basename(downloadedFiles['png']))) #admin

def main(argv) -> None:
    try:
        opts, arg = getopt(argv, 'hc:d:',['config=', 'dwld='])
    except GetoptError:
        print('test.py -c <installConfigs> -d <downloadedFiles>')
        return None

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -c <installConfigs> -d <downloadedFiles>')
            return None
        elif opt in ('-c', '--config'):
            installConfigs = arg
        elif opt in ('-d', '--dwld'):
            downloadedFiles = arg
    print('argv[1] is', installConfigs)
    print('argv[2] is', downloadedFiles)

    #uac_procs(installConfigs, downloadedFiles)

#________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    if len(argv) != 1:
        main(argv[1:])
    else:
        print('test.py -c <installConfigs> -d <downloadedFiles>')
    getwch()
