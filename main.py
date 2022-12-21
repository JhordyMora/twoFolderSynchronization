import os
import hashlib
import time
#Name descompositino path source -> function

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
        
    #Checking if the files exist or not
    if os.path.isfile(os.path.realpath(PATH_SOURCE)):
        # Checking if the target folder exists
        if os.path.isdir(os.path.realpath(PATH_REPLICA)):
            # Checking if a back up file exists
            NAME_FILE = PATH_SOURCE.split("/")
            PATH_BACK_UP_FILE = PATH_REPLICA +"backUp_"+ NAME_FILE[-1]
            if os.path.isfile(os.path.realpath(PATH_BACK_UP_FILE)):
                print("to -do ")
            else:
                creationBackUpFileAndLog(PATH_BACK_UP_FILE, PATH_REPLICA)
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

def creationBackUpFileAndLog(PATH_BACK_UP_FILE, PATH_REPLICA):
    backup_file = open(PATH_BACK_UP_FILE, "x")
    backup_file.close()
    print("The backup file was created")
    LOG_PATH = PATH_REPLICA + "log.txt"
    print(LOG_PATH)
    with open(LOG_PATH, "w") as log:
        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log.write(f"Log File was created on {now}")
        log.write("\n")
        log.write("Hola!")
    print("The log file was created")



if __name__ == "__main__":
    main()