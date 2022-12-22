import os
import hashlib
import shutil
import time
#Name descompositino path source -> function
# mirar si el targe folder teine \ PATH_REPLICA

def main():
    # input necesary for the program
    PATH_SOURCE = input("Provide the complete path of your source file: ")
    if (not os.path.isdir(os.path.realpath(PATH_SOURCE))) or PATH_SOURCE=="" :
        print("Please, check that the path is a folder path or that the folder exists. Try again")
        main()
    first_number_files_source = len(os.listdir(PATH_SOURCE))
    # print(first_number_files_source)
        
    PATH_REPLICA = input("Provide the path of another folder where do you want to save replica file: ")
    if (PATH_REPLICA==PATH_SOURCE) or PATH_REPLICA=="":
        print("Please, chosse a different folder for the replica. Try again")
        main()
    
    try:
        PARENT_DIR = "/".join(PATH_REPLICA.split("/")[0:-1])
        LOG_PATH = PARENT_DIR + "/log.txt"
        logCreation(LOG_PATH)
    except:
        print("Log File already exists.")
        informationForLog("Log file was tried to create once again",LOG_PATH)
        
    first_number_files_replica = 0
    if os.path.isdir(os.path.realpath(PATH_REPLICA))==False:
        creationReplicaFolder(PATH_REPLICA, LOG_PATH)
    else:
        first_number_files_replica = len(os.listdir(PATH_REPLICA))
    # print(first_number_files_replica)
        
    
    try:
        SYNCHRO_TIME = int(input("Provide how regularly do you want to synchronize your replica file in minutes: "))
    except:
        print("Pleased, check if your type an integer/ number")
        print("Type all the information again")
        main()

    if first_number_files_replica == 0:
        for file_source in os.listdir(PATH_SOURCE):
            creatingCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH)
    else:       
        for file_source in os.listdir(PATH_SOURCE):
            # print(f"file_source: {file_source}")
            # print(f"list files replica folder: {os.listdir(PATH_REPLICA)}")
            name_in_replica= f"Back_up_{file_source}"
            # print(f"is in folder?: {name_in_replica in os.listdir(PATH_REPLICA)}")
            # for file_replica in os.listdir(PATH_REPLICA):
            #     print(f"file_replica: {file_replica}")
            if name_in_replica in os.listdir(PATH_REPLICA):
                src_path = PATH_SOURCE + "/" + file_source
                dst_path = PATH_REPLICA + "/Back_up_" + file_source
                areSameFiles = comparingFiles(src_path, dst_path)
                # print(f"areSameFiles: {areSameFiles}")
                if not areSameFiles:
                    # print("do function which copy the original file to the replica folder")
                    creatingUpdatedCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH)
            else:
                # creatingCopyInReplica()
                # print("create function which creates a copy of a file")
                creatingCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH)
                
    first_number_files_replica = len(os.listdir(PATH_REPLICA))
    first_number_files_source = len(os.listdir(PATH_SOURCE))
    
    
                
    if first_number_files_replica > first_number_files_source:
        file_list_source = os.listdir(PATH_SOURCE)
        file_list_replica = [file.replace("Back_up_","") for file in os.listdir(PATH_REPLICA)]
        # print(f"list file_source: {file_list_source}")  
        # print(f"list files replica folder: {file_list_replica}")
        # print("do function that deletes files von backup")
        extra_files=["Back_up_"+file for file in file_list_replica if file not in file_list_source]
        for file in extra_files:
            extra_files_path = PATH_REPLICA + "/" + file
            os.remove(extra_files_path)
            informationForLog(f"File {file} not found in source folder. File {file} was deleted", LOG_PATH)
            print("File {file} not found in source folder. File {file} was deleted")
        

def creationReplicaFolder(PATH_REPLICA, LOG_PATH):
    try:
        answer = input("The Back Up Folder does not exist. Do you want to create it? [y] for Yes, or [n] for No ")
        # print(answer)
        if answer == "y":
            NAME_FILE = PATH_REPLICA.split("/")
            directory = NAME_FILE[-1]
            PARENT_DIR = NAME_FILE[0:-1]
            parent_dir = "/".join(PARENT_DIR)
            os.chdir(parent_dir)
            os.mkdir(directory)
            informationForLog(f"The folder {directory} was created", LOG_PATH)
            print("The back up folder was created")
        else:
            print("Sorry we can not continue with the synchronization. Try again")
            deletingLogFile(LOG_PATH)
            main()
    except:
        print("Are you sure did you write a file path? Please try again")
        main()
    
def creatingCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH):
    src_path = PATH_SOURCE + "/" + file_source
    dst_path = PATH_REPLICA + "/Back_up_" + file_source
    shutil.copy(src_path, dst_path)
    informationForLog(f"Back up File of {file_source} was created on {PATH_REPLICA}", LOG_PATH)
    print(f"Back up File of {file_source} was created on {PATH_REPLICA}")

def creatingUpdatedCopyInReplica(PATH_SOURCE,file_source ,PATH_REPLICA, LOG_PATH):
    src_path = PATH_SOURCE + "/" + file_source
    dst_path = PATH_REPLICA + "/Back_up_" + file_source
    shutil.copy(src_path, dst_path)
    informationForLog(f"Back up File of {file_source} was updated on {PATH_REPLICA}", LOG_PATH)
    print(f"Back up File of {file_source} was updated on {PATH_REPLICA}")
    
def logCreation(LOG_PATH):
    log = open(LOG_PATH, "x")
    informationForLog("Log File was created", LOG_PATH)
    log.close()
    print("Log File was created")
    
def informationForLog(message, LOG_PATH):
    with open(LOG_PATH, "a") as log:
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log.write(f"{message} on {now}")
        log.write("\n")
    print(f"{message} on {now}")

def comparingFiles(file1, file2):
    # compare 2 files with hash
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False

def deletingLogFile(LOG_PATH):
    os.remove(LOG_PATH)
    
if __name__ == "__main__":
    main()