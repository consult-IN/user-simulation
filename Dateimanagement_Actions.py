import os
import shutil
import time
from shutil import move
import configparser


def createDirectories():
# Erstellt Ordner, die für moveFiles.py benötigt werden

    # os.mkdir("softwares")
    root_path = ''
    directories = ['softwares', 'documents', 'images']  # put in names of directories you want to create

    for directory in directories:
        os.mkdir(os.path.join(root_path, directory))  # creates directories

    print('Successfully created directories')

    # subdirectory in previous directory
    # os.makedirs("software" + "/" + "")


def moveFiles():
# Verschiebt Dateien ihrer Dateienendung entsprechend in die verschiedenen Ordner

    config = configparser.ConfigParser()
    config.read('ConfigPathDriver.ini')

    user = os.getenv('USER')
    root_dir = '/Users/' + config['PATH']['User'] + '/' + config['PATH']['DirectoryMoveFiles'] + '/'.format(user)
    image_dir = '/Users/' + config['PATH']['User'] + '/' + config['PATH']['DirectoryMoveFiles'] + '/' + config['PATH'][
        'SubdirectoryMoveFiles1'] + '/'.format(user)
    documents_dir = '/Users/' + config['PATH']['User'] + '/' + config['PATH']['DirectoryMoveFiles'] + '/' + \
                    config['PATH']['SubdirectoryMoveFiles2'] + '/'.format(user)
    # others_dir = '/Users/'+config['PATH']['User']+'/'+config['PATH']['DirectoryMoveFiles']+'/'+config['PATH']
    # ['SubdirectoryMoveFiles3']+'/'.format(user)
    software_dir = '/Users/' + config['PATH']['User'] + '/' + config['PATH']['DirectoryMoveFiles'] + '/' + \
                   config['PATH']['SubdirectoryMoveFiles4'] + '/'.format(user)

    # tuples for category wise file types
    doc_types = ('.doc', '.docx', '.txt', '.pdf', '.xls', '.ppt', '.xlsx', '.pptx')
    img_types = ('.jpg', '.jpeg', '.png', '.svg', '.gif', '.tif', '.tiff')
    software_types = ('.exe', '.pkg', '.dmg')

    # listdir() method returns the list of the names of all the files & directories in the given path
    # isfile() method checks if the path provided is a file or not
    # return a list of all the required files

    def get_non_hidden_files_except_current_file(root_dir):
        return [f for f in os.listdir(root_dir) if
                os.path.isfile(f) and not f.startswith('.') and not f.__eq__(__file__)]

    # move_files() method is taking the list of files and moving them to their respective folders

    def move_files(files):
        for file in files:
            # file moved and overwritten if already exists
            if file.endswith(doc_types):
                move(file, '{}/{}'.format(documents_dir, file))
                #print('file {} moved to {}'.format(file, documents_dir))
            elif file.endswith(img_types):
                move(file, '{}/{}'.format(image_dir, file))
                #print('file {} moved to {}'.format(file, image_dir))
            elif file.endswith(software_types):
                move(file, '{}/{}'.format(software_dir, file))
                #print('file {} moved to {}'.format(file, others_dir))
            else:
                pass
            
    files = get_non_hidden_files_except_current_file(root_dir)

    move_files(files)
    time.sleep(6)
    
    # moveFiles.py has to be in directory path



def randomizer_Dateimanagement():
    a = randint(1, 2)
        
    if a == 1:
        moveFiles()
        
    if a == 2:
        createDirectories()
        
        
