import os.path, sys
import re
import subprocess
import zipfile

from setuptools import setup


BASEPATH = os.path.dirname(os.path.abspath(__file__))
JAR_FILE = 'scienceworld.jar'
JAR_PATH = os.path.join(BASEPATH, 'scienceworld', JAR_FILE)
# Extract ScienceWorld version from JAR file metadata
contents = zipfile.ZipFile(JAR_PATH).open('META-INF/MANIFEST.MF').read().decode('utf-8')
VERSION = re.search(r'\bSpecification-Version: (.*)\b', contents).group(1)

OBJECTS_LUT_FILE = "object_type_ids.tsv"
TASKS_JSON_FILE = "tasks.json"

if not os.path.isfile(JAR_PATH):
    print('ERROR: Unable to find required library:', JAR_PATH)
    sys.exit(1)

# Based on https://github.com/microsoft/DeepSpeed/blob/28dfca8a13313b570e1ad145cf14476d8d5d8e16/setup.py#L170-L184
# Write out version/git info
git_hash_cmd = "git rev-parse --short HEAD"
try:
    result = subprocess.check_output(git_hash_cmd, shell=True)
    git_hash = result.decode('utf-8').strip()
    VERSION += f'+{git_hash}'
except subprocess.CalledProcessError:
    pass

with open(os.path.join('scienceworld', 'version.py'), 'w') as f:
    f.write(f'__version__ = {VERSION!r}\n')

setup(name='scienceworld',
    version=VERSION,
    description='ScienceWorld: An interactive text environment to study AI agents on accomplishing tasks from the standardized elementary science curriculum.',
    author='Peter Jansen',
    packages=['scienceworld'],
    include_package_data=True,
    package_dir={'scienceworld': 'scienceworld'},
    package_data={'scienceworld': [JAR_FILE, OBJECTS_LUT_FILE, TASKS_JSON_FILE]},
    url="https://scienceworld.github.io",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires='>=3.7',
    install_requires=open('requirements.txt').readlines(),
    extras_require={
        'webserver': open('requirements.txt').readlines() + ['pywebio'],
    },
)
