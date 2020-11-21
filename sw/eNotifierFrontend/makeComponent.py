import os
import shutil
import subprocess
from pathlib import Path
import shlex

from makeInstallScript import create_install_script
import json

def getFromJson(jsonFile, key):
  json_file = open(jsonFile, 'r')
  json_data = json.load(json_file)
  return json_data[key]

def parseVersion(rawVersion):
  point_position = rawVersion.find('.')
  major = rawVersion[:point_position]
  rawVersion = rawVersion[2:]
  point_position = rawVersion.find('.')
  minor = rawVersion[:point_position]
  parsedVersion = str(major) + '.' + str(minor)
  return parsedVersion

########## PACKAGE INFO ##########
name = getFromJson('package.json', 'name')
description='eNotifier Web Frontend'
version = parseVersion(getFromJson('package.json', 'version'))
author='iz2k'
author_email='ibon@zalbide.com'
url='https://www.zalbide.com'

# Clean previous outputs
try:
  shutil.rmtree(Path('dist'))
except:
  pass
os.mkdir(Path('dist'))

print('Starting Angular build..')
print(os.getcwd())
os.system('ng build --prod')
#subprocess.call(shlex.split('ng build --prod'), cwd=os.getcwd())
print('Build finished!')

# Create version.txt
print('Creating version file..')
version_file = open('dist/version.txt','w+')
version_file.write(version)
version_file.close()

# Create install.sh
print('Creating install.sh script..')
create_install_script(name)

# Zip dist folder
print('Creating component zip')
shutil.make_archive(Path(name + '_' + version), 'zip', 'dist')
os.rename(Path(name + '_' + version + '.zip'), Path('dist/' + name + '_' + version + '.zip'))

# Delete intermediate files
print('Cleaning up')
os.remove(Path('./dist/version.txt'))
os.remove(Path('./dist/install.sh'))
try:
  shutil.rmtree(Path('dist/public'))
except:
  pass
print('Done!')
