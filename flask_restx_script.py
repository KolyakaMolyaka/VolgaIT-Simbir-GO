"""
https://github.com/python-restx/flask-restx/issues/567
Исправление: https://github.com/python-restx/flask-restx/issues/567#issuecomment-1742097985
"""

from tempfile import mkstemp
from shutil import move
from os import remove, close

def replace(file_path, pattern, subst):
    # Create temp file
    fh, abs_path = mkstemp()
    replaced = True
    with open(abs_path, 'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                if not replaced:
                    new_file.write(line.replace(pattern, subst))
                    replaced = True
                else:
                    new_file.write(line)
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

replace('/usr/local/lib/python3.10/site-packages/flask_restx/api.py',
        'flask.scaffold', 
        'flask.sansio.scaffold')

print('flask-restx/api.py sansio bug fixed')