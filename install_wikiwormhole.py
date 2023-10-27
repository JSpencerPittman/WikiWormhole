import os
import venv
import subprocess

venv_name = 'env'
venv.create(venv_name, with_pip=True)

activate_script = os.path.join(venv_name, 'bin', 'activate')
custom_data_dir = os.path.abspath('data/w2v')

with open(activate_script, 'a') as file:
    file.write(f'\nexport GENSIM_DATA_DIR="{custom_data_dir}"\n')
