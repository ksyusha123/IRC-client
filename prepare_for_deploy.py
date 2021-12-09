from yapf.yapflib.yapf_api import FormatFile
from zipfile import ZipFile
import glob
from pathlib import Path
import shutil


PATTERN = "*.py"


def get_ignored_objects(directory):
    if not Path(directory / ".gitignore").exists():
        return None
    ignored_files = set()
    ignored_files.add(Path(directory / ".git"))
    ignored_files.add(Path(directory / ".gitignore"))
    with open(Path(directory / ".gitignore")) as gitignore:
        for line in gitignore:
            line = line.strip()
            if not line.startswith("#"):
                for object_to_ignore in glob.glob(line):
                    obj_to_ignore_path = Path(directory / object_to_ignore)
                    ignored_files.add(obj_to_ignore_path)
                    if obj_to_ignore_path.is_dir():
                        for file in obj_to_ignore_path.iterdir():
                            ignored_files.add(file)
    return ignored_files


def delete_directory(directory):
    for obj in directory.iterdir():
        if obj.is_dir():
            delete_directory(obj)
        else:
            obj.unlink()
    directory.rmdir()


def make_zip_with_file_for_deploy(directory=Path('.'),
                                  archive_path=Path('.')):
    directory = Path(directory)
    ignored_objects = get_ignored_objects(directory)
    py_files = set(directory.glob(PATTERN))
    tmp_folder = Path(directory / "for_deploy")
    tmp_folder.mkdir()
    for obj in directory.iterdir():
        if obj in py_files:
            reformatted_code, encoding, changed = FormatFile(str(obj))
            with open(Path(tmp_folder / obj.name), 'w') as py_file:
                for line in reformatted_code.split('\n'):
                    py_file.write(line)
        elif obj != tmp_folder and obj not in ignored_objects:
            shutil.copyfile(obj, Path(tmp_folder / obj.name))
    with ZipFile(Path(archive_path / "archive.zip"), 'w') as archive:
        for obj in tmp_folder.iterdir():
            archive.write(obj)
    delete_directory(tmp_folder)


make_zip_with_file_for_deploy()
