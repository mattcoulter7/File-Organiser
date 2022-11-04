import os
import platform
from datetime import datetime
import shutil

COPYMOVECOUNT = 0 # Number of files organised
DUPLICATECOUNT = 0 # Number of duplicate files found
NEWFOLDERCOUNT = 0 # Number of new folders created

def get_bool(message):
    '''
        determines true or false based off of input
    '''
    print(message + ' [y/n]')
    value = input()
    if value == 'y':
        return True
    elif value == 'n':
        return False
    return get_bool(message)


def get_dir(message):
    '''
        Gets input of directory
        only returns directory when the directory is found
    '''
    print(message)
    value = input()
    if os.path.isdir(value):
        return value
    print("Directory Not Found... Please Try Again...")
    return get_dir(message)

def get_action():
    '''
        Gets input of copy or move
        only returns value when input is copy or move
        non case-sensitive
    '''
    print('Do you want to move or copy the files into folders? [move/copy]')
    value = input()
    if value.lower() in ['copy','move']:
        return value.lower()
    print("Please Enter 'copy' or 'move'...")
    return get_action()

def sort_date(srcpath,destpath,action,subfolders):
    ''' 
        Sorts the provided directory into folders organised by date
        action determines whether the files will be moved or copied
    ''' 
    # Declare global for modification
    global COPYMOVECOUNT
    global DUPLICATECOUNT
    global NEWFOLDERCOUNT

    # For each file in directory
    for filename in os.listdir(srcpath):
        # Directory of file
        srcfilepath = os.path.join(srcpath,filename)

        # Files
        if os.path.isfile(srcfilepath):
            # Only applies to photos and videos
            if filename.lower().endswith(('.lrv','.aae','.3gp','.nef','.mov','.webm','.mp4','.m4p','.m4v','.avi','.wmv','.gif','.png', '.jpg','.jpeg', '.jpeg')):
                # Gets date of file as string
                filetimestamp = os.path.getmtime(srcfilepath)
                filedate = str(datetime.fromtimestamp(filetimestamp).strftime('%Y-%m-%d'))

                # Directory of folder that will be created
                destfolderpath = os.path.join(destpath,filedate)

                # Checks if folder already exists
                if not os.path.exists(destfolderpath):
                    # Makes a folder with date of creation as name
                    print('Adding a new folder at: ' + destfolderpath)
                    os.makedirs(destfolderpath) 
                    NEWFOLDERCOUNT += 1
        
                # Address that the copied file will become (used for existence check)
                destfilepath = os.path.join(destfolderpath,filename)

                # Existence check
                if not os.path.isfile(destfilepath):
                    # Copies file into folder (including metadata)
                    if action == 'copy':
                        print('\tCopying ' + filename + ' into ' + destfolderpath + '...')
                        shutil.copy2(srcfilepath,destfolderpath)
                    # Moves file into folder
                    elif action == 'move':
                        print('\tMoving ' + filename + ' into ' + destfolderpath + '...')
                        shutil.move(srcfilepath,destfolderpath)
                    COPYMOVECOUNT += 1
                # Removes file from source if it already exists        
                else: 
                    print('File already exists')
                    DUPLICATECOUNT += 1
                    if action == 'move': # only deletes from source for duplicate if action is move
                        print('\tDeleting' + filename + ' from source directory because it already exists...')
                        os.remove(srcfilepath)
                    
        # Folders will run the this sort if:
        # 1. It is a folder
        # 2. the user wants subfolders to be organised
        # 3. the folder path is not the dest path (avoid infinite loop)
        elif os.path.isdir(srcfilepath) and subfolders and srcfilepath != destpath:
            sort_date(srcfilepath,destpath,action,subfolders)   

def print_result():
    # Declare Global
    global COPYMOVECOUNT
    global DUPLICATECOUNT
    global NEWFOLDERCOUNT

    # Print Result
    print(str(COPYMOVECOUNT) + ' photos/videos have been organised...')
    print(str(NEWFOLDERCOUNT) + ' New days were created')
    print(str(DUPLICATECOUNT) + ' Duplicates photos/videos have been found')
    print("Organising Complete!")

    # Reset Global
    COPYMOVECOUNT = 0
    DUPLICATECOUNT = 0
    NEWFOLDERCOUNT = 0

def main():
    # gets directory to sort
    srcpath = get_dir('Please Enter a Directory to Organise: ')

    # gets output directory where files are copied/moved to
    destpath = get_dir('Please Enter a Output Directory')

    # Determines move or copy
    action = get_action()

    # Determines move or copy
    subfolders = get_bool('Would you like to include subfolders?')

    # Runs the sort function
    sort_date(srcpath,destpath,action,subfolders)
    print_result()
    # Prompt to organise another directory
    if get_bool('Would you like to sort another directory?'):
        main()

# Program execution begins here
if __name__ == '__main__':
    main()