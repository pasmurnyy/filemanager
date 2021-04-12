import os
import shutil
from pathlib import Path

PATH = "C:/Users/airsh/OneDrive/Desktop/test"
FileManager_PATH = Path(PATH).absolute()

class FileManager:
    def __init__(self, work_dir):
        self.WORK_DIR = Path(work_dir).absolute()
        try:
            os.chdir(self.WORK_DIR)
        except FileNotFoundError:
            print("File not found exception")
        self.curr_dir = Path(work_dir).absolute()
        self.last_dir = self.WORK_DIR.name


    def get_current_dir(self):
        return os.getcwd()

    def make_dir(self, path):
        try:
            if os.path.exists(path):
                print("Error. Please rename folder.")
            else:
                os.makedirs(str(path))
                print(f'Folder {path.split("/")[-1]} created')
        except FileNotFoundError:
            print("Error, try again")

    def del_dir(self, path):
        if os.path.isdir(path):
            shutil.rmtree(str(path), ignore_errors=True)
            print("Folder", path.split("/")[-1], "deleted")
        else:
            print("Error, try again")

    def ch_dir(self, path):
        try:
            if len(path) != 0:
                if path == "..":
                    if self.last_dir in str(self.curr_dir.parent):
                        os.chdir(self.curr_dir.parent)
                        self.curr_dir = self.WORK_DIR.joinpath(self.curr_dir.parent)
                        print("Current path:", self.curr_dir)
                    else:
                        print("Unable")
                else:
                    os.chdir(path)
                    self.curr_dir = self.WORK_DIR.joinpath(path)
                    print("Current path:", self.curr_dir)
        except FileNotFoundError:
            print("Error, try again")
        except OSError:
            print("Error, try again")

    def make_file(self, path):
        try:
            if os.path.exists(path):
                print("Change name.")
            else:
                open(path, "w", encoding="utf-8").close()
                print("Created")
        except FileNotFoundError:
            print("Error, try again")

    def write_file(self, path, inner):
        try:
            self.curr_dir.joinpath(path).write_text(inner)
            print(f"Data '{inner}' saved in {path}.")
        except FileNotFoundError:
            print("Error, try again")

    def read_file(self, path):
        try:
            if os.path.exists(path):
                print(str(self.curr_dir.joinpath(path).read_text()))
            else:
                print("Error, try again")
        except OSError:
            print("Error, try again")

    def del_file(self, path):
        try:
            if os.path.exists(path):
                os.remove(self.curr_dir.joinpath(path))
                print(f"File {path} is deleted.")
            else:
                print("Error, try again")
        except OSError:
            print("Error, try again")

    def copy_file(self, curr_path, new_path):
        try:
            if os.path.exists(curr_path):
                shutil.copy2(curr_path, new_path)
                print(f"Copied in {new_path}")
            else:
                print("Error, try again")
        except OSError:
            print("Error, try again")

    def move_file(self, curr_path, new_path):
        try:
            if os.path.exists(curr_path):
                os.replace(curr_path, new_path)
                print(f"File id moved from {curr_path} in {new_path}")
            else:
                print("Error, try again")
        except OSError:
            print("Error, try again")

    def rename_file(self, path, new_name):
        try:
            if os.path.exists(path):
                self.curr_dir.joinpath(path).rename(new_name)
                print(f"File is renamed {new_name}")
            else:
                print("Error, try again")
        except FileExistsError:
            print("Error, try again")

    def helper(self):

        print("make_dir {name}               Create directory {name}")
        print("del_dir {name}                Delete directory {name}")
        print("ch_dir {name}                 Change work directory")
        print("make_file {name}              Create empty file {name}")
        print("write_file {name} {data}      Write {data} to file {name}")
        print("read_file  {name}             Viewing the contents of a text file")
        print("del_file  {name}              Delete file {name}")
        print("copy_file {name} {new_dir}    Copy file from {name} to {new_dir}")
        print("move_file {dir} {new_dir}     Move file from {name} to {new_name}")
        print("rename_file {name} {new_name} Rename file from {name} to {new_name}")
        print("current                       Show work dir")
        print("help                          For help")
        print("Exit                          Exit from program")

FM = FileManager(FileManager_PATH)
print("Current path: ", FM.get_current_dir())


while True:
    command = input(">>> ")
    if command.split(' ')[0] == "make_dir":
        new_dir = command.split(' ')[1]
        FM.make_dir(new_dir)

    elif command.split(' ')[0] == "del_dir":
        dirname = command.split(' ')[1]
        FM.del_dir(dirname)


    elif command.split(' ')[0] == "make_file":
        filename = command.split(' ')[1]
        FM.make_file(filename)

    elif command.split(' ')[0] == "write_file":
        filename = command.split(' ')[1]
        text = ' '.join(command.split(' ')[2:])
        FM.write_file(filename, text)

    elif command.split(' ')[0] == "read_file":
        filename = command.split(' ')[1]
        FM.read_file(filename)

    elif command.split(' ')[0] == "del_file":
        filename = command.split(' ')[1]
        FM.del_file(filename)

    elif command.split(' ')[0] == "copy_file":
        currpath = command.split(' ')[1]
        newpath = command.split(' ')[2]
        FM.copy_file(currpath, newpath)

    elif command.split(' ')[0] == "move_file":
        currpath = command.split(' ')[1]
        newpath = command.split(' ')[2]
        FM.move_file(currpath, newpath)

    elif command.split(' ')[0] == "rename_file":
        filepath = command.split(' ')[1]
        newname = command.split(' ')[2]
        FM.rename_file(filepath, newname)

    elif command.split(' ')[0] == "current":
        print("Current path:", FM.get_current_dir())

    elif command == "tree_list":
        print("Сontents of the current folder: ")
        FM.tree_list()

    elif command == "help":
        FM.helper()

    elif command == "Exit":
        print("Bye")
        break
    else:
        print("Wrong command. Print Help for help")
