import os
import hashlib
import time
#Name descompositino path source -> function
# mirar si el targe folder teine \ PATH_REPLICA

def main():
    # input necesary for the program
    PATH_SOURCE = input("Provide the real path and name of your source file: ")
    PATH_REPLICA = input("Provide the real path where do you want to save replica file: ")
    try:
        SYNCHRO_TIME = int(input("Provide how regularly do you want to synchronize your replica file in minutes: "))
    except:
        print("Pleased, check if your type an integer/ number")
        print("Type all the information again")
        main()
    
    LOG_PATH = PATH_REPLICA + "log.txt"
    logCreation(LOG_PATH)
    
    #Checking if the files exist or not
    if os.path.isfile(os.path.realpath(PATH_SOURCE)):
        # Checking if the target folder exists
        if os.path.isdir(os.path.realpath(PATH_REPLICA)):
            # Checking if a back up file exists
            NAME_FILE = PATH_SOURCE.split("/")
            PATH_BACK_UP_FILE = PATH_REPLICA +"backUp_"+ NAME_FILE[-1]
            if os.path.isfile(os.path.realpath(PATH_BACK_UP_FILE)):
                equal_data = compare2file(PATH_SOURCE, PATH_BACK_UP_FILE)
                print(equal_data)
            else:
                creationBackUpFile(PATH_BACK_UP_FILE, LOG_PATH)
        else:
            creationReplicaFolder(PATH_REPLICA)
    else:
        creationSourceFile(PATH_SOURCE)
    
def creationSourceFile(PATH_SOURCE):
        answer = input("The File does not exist. Do you want to create it? [y] for Yes, or [n] for No ")
        if answer == "y":
            NAME_FILE = PATH_SOURCE.split("/")
            print(f"the name of your file will be {NAME_FILE[-1]}")
            source_file = open(PATH_SOURCE, "x")
            source_file.close()
            print("The file was created")
        else:
            print("Sorry we can not continue with the synchronization")
            
def creationReplicaFolder(PATH_REPLICA):
    try:
        answer = input("The Folder does not exist. Do you want to create it? [y] for Yes, or [n] for No ")
        if answer == "y":
            NAME_FILE = PATH_REPLICA.split("/")
            directory = NAME_FILE[-1]
            PARENT_DIR = NAME_FILE[0:-1]
            parent_dir = "/".join(PARENT_DIR)
            os.chdir(parent_dir)
            os.mkdir(directory)
            print("The folder was created")
        else:
            print("Sorry we can not continue with the synchronization")
    except:
        print("Are you sure did you write a file path? Please try again")
        main()

def creationBackUpFile(PATH_BACK_UP_FILE, LOG_PATH):
    backup_file = open(PATH_BACK_UP_FILE, "x")
    backup_file.close()
    informationForLog("The backup file was created", LOG_PATH)
    print("The backup file was created")
    
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

def compare2file(file1, file2):
    # compare 2 files with hash
    with open(file1, 'rb') as f1:
        with open(file2, 'rb') as f2:
            if hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest():
                return True
            else:
                return False

if __name__ == "__main__":
    main()