from yapf.yapflib.yapf_api import FormatFile
from zipfile import ZipFile
import os
from pathlib import Path
from os.path import basename


PATTERN = "*.py"


def make_folder_with_modified_py_files(directory=Path('.'),
                                       archive_path=Path('.')):
    directory = Path(directory)
    tmp_folder = Path(archive_path / 'tmp')
    Path.mkdir(tmp_folder)
    for file in directory.glob(PATTERN):
        reformatted_code, encoding, changed = FormatFile(str(file))
        with open(Path(tmp_folder / file.name), 'w') as f:
            for line in reformatted_code.split('\n'):
                f.write(line)


def make_archive_from_folder(folder=Path('tmp'), archive_path=Path('.')):
    with ZipFile(Path(archive_path / 'archive.zip'), 'w') as zip_obj:
        for py_file in folder.iterdir():
            zip_obj.write(py_file)

make_folder_with_modified_py_files()
make_archive_from_folder()
