import os
import hashlib
import shutil
import time
import datetime

def main():
    # Getting the path of the source folder/ Checking if the path is a directory and exists
    PATH_SOURCE = input("Provide the complete path of your source file: ")
    if (not os.path.isdir(os.path.realpath(PATH_SOURCE))) or PATH_SOURCE=="" :
        print("Please, check that the path is a folder path or that the folder exists. Try again")
        main()
    # Getting the number of files in the source folder
    first_number_files_source = len(os.listdir(PATH_SOURCE))
    
    # Getting the path of the replica folder / Checking if the replica folder is different from the source folder
    PATH_REPLICA = input("Provide the path of another folder where do you want to save replica file: ")
    if (PATH_REPLICA==PATH_SOURCE) or PATH_REPLICA=="":
        print("Please, chosse a different folder for the replica. Try again")
        main()

    try:
        # Get the parent directory of the replica folder and creating a log file in the parent directory
        PARENT_DIR = os.path.dirname(PATH_REPLICA)
        LOG_PATH = os.path.join(PARENT_DIR, "log.txt")
        logCreation(LOG_PATH)
    except:
        print("Log File already exists.")
        informationForLog("Log file was tried to create once again",LOG_PATH)

    # Creating replica folder / Getting number of files ont it
    first_number_files_replica = 0
    if os.path.isdir(os.path.realpath(PATH_REPLICA))==False:
        creationReplicaFolder(PATH_REPLICA, LOG_PATH)
    else:
        first_number_files_replica = len(os.listdir(PATH_REPLICA))        

    # Getting the synchronization time in minutes
    try:
        SYNCHRO_TIME = int(input("Provide how regularly do you want to synchronize your replica file in minutes: "))
        SYNCHRO_TIME_SEC = SYNCHRO_TIME*60
    except:
        print("Pleased, check if your type an integer/ number")
        print("Type all the information again")
        main()

    informationForLog("Synchronization process has begun",LOG_PATH)
    print("If you want to stop the synchronization at any moment press the key combination [ctrl + c]")
    
    try:
        while(True): 
            # If the replica folder is empty, copy all files from the source folder to the replica folder
            if first_number_files_replica == 0:
                for file_source in os.listdir(PATH_SOURCE):
                    creatingCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH)
            else:
                # Compare if files are same/exist or not and updating/creating copy     
                for file_source in os.listdir(PATH_SOURCE):
                    name_in_replica= f"Back_up_{file_source}"
                    if name_in_replica in os.listdir(PATH_REPLICA):
                        src_path = os.path.join(PATH_SOURCE, file_source)
                        dst_path = os.path.join(PATH_REPLICA, f"Back_up_{file_source}")
                        areSameFiles = comparingFiles(src_path, dst_path)
                        if not areSameFiles:
                            creatingUpdatedCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH)
                    else:
                        creatingCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH)

            # Updating the number of files in the source and replica folders
            first_number_files_replica = len(os.listdir(PATH_REPLICA))
            first_number_files_source = len(os.listdir(PATH_SOURCE))

            # Checking if there are extra files in the replica folder and deleting them
            if first_number_files_replica > first_number_files_source:
                file_list_source = os.listdir(PATH_SOURCE)
                file_list_replica = [file.replace("Back_up_","") for file in os.listdir(PATH_REPLICA)]
                extra_files=["Back_up_"+file for file in file_list_replica if file not in file_list_source]
                for file in extra_files:
                    extra_files_path = os.path.join(PATH_REPLICA, file)
                    os.remove(extra_files_path)
                    original_name = file.replace("Back_up_","")
                    informationForLog(f"File {original_name} was not found in source folder. File {file} was deleted", LOG_PATH)
                    print(f"File {original_name} was not found in source folder. File {file} was deleted")

            # Wait the set time before synchronizing again
            time.sleep(SYNCHRO_TIME_SEC)
    except KeyboardInterrupt:
        informationForLog("\nThe file(s) synchronization has been stopped",LOG_PATH)
        print("The file(s) synchronization has been stopped \nHave a good day!")


def creationReplicaFolder(PATH_REPLICA, LOG_PATH):
    '''
    Creates the replica folder
    PATH_REPLICA: string, path of the replica folder
    LOG_PATH: string, path of the log file
    '''
    
    try:
        answer = input("The Back Up Folder does not exist. Do you want to create it? [y] for Yes, or [n] for No ")
        if answer == "y":
            os.makedirs(PATH_REPLICA)
            informationForLog(f"The back-up folder was created", LOG_PATH)
            print("The back up folder was created")
        else:
            print("Sorry we can not continue with the synchronization. Try again")
            deletingLogFile(LOG_PATH)
            main()
    except:
        print("Are you sure did you write a file path? Please try again")
        main()
    
def creatingCopyInReplica(PATH_SOURCE, file_source, PATH_REPLICA, LOG_PATH):
    '''
    Copies a file from the source folder to the replica folder and adds a "Back_up_" prefix
    PATH_SOURCE: string, path of the source folder
    file_source: string, name of the file to be copied
    PATH_REPLICA: string, path of the replica folder
    LOG_PATH: string, path of the log file
    '''
    
    src_path = os.path.join(PATH_SOURCE, file_source)
    dst_path = os.path.join(PATH_REPLICA, f"Back_up_{file_source}")
    shutil.copy(src_path, dst_path)
    informationForLog(f"Back up File of {file_source} was created on {PATH_REPLICA}", LOG_PATH)
    print(f"Back up File of {file_source} was created on {PATH_REPLICA}")

def creatingUpdatedCopyInReplica(PATH_SOURCE, file_source, PATH_REPLICA, LOG_PATH):
    '''
    Copies an updated version of a file from the source folder to the replica folder and adds a "Back_up_" prefix
    PATH_SOURCE: string, path of the source folder
    file_source: string, name of the file to be copied
    PATH_REPLICA: string, path of the replica folder
    LOG_PATH: string, path of the log file
    '''
    
    src_path = os.path.join(PATH_SOURCE, file_source)
    dst_path = os.path.join(PATH_REPLICA, f"Back_up_{file_source}")
    shutil.copy(src_path, dst_path)
    informationForLog(f"Back up File of {file_source} was updated on {PATH_REPLICA}", LOG_PATH)
    print(f"Back up File of {file_source} was updated on {PATH_REPLICA}")
    
def logCreation(LOG_PATH):
    '''
    Creates a log file at the specified path
    LOG_PATH: string, path to create the log file
    '''
    
    log = open(LOG_PATH, "x")
    informationForLog("Log File was created", LOG_PATH)
    log.close()
    print("Log File was created")
    
def informationForLog(message, LOG_PATH):
    '''
    Appends information to the log file at the specified path
    message: string, information to be logged
    LOG_PATH: string, path of the log file
    '''
    
    with open(LOG_PATH, "a") as log:
        now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"{message} on {now}")
        log.write("\n")
    print(f"{message} on {now}")

def comparingFiles(file1, file2):
    '''
    Compares if two files are the same by comparing their hash values
    file1: string, path of the first file
    file2: string, path of the second file
    return: bool, True if files are the same, False otherwise
    '''
    
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False

def deletingLogFile(LOG_PATH):
    '''
    Deletes the log file
    LOG_PATH: string, path of the log file
    '''
    
    try:
        os.remove(LOG_PATH)
        print("Log file successfully deleted.")
    except:
        print("Log file could not be deleted.")
    
if __name__ == "__main__":
    main()