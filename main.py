from pathlib import Path
def creating():
    try:
        name=input("Please enter your file name ")
        path=Path(name)
        if not path.exists():
            with open(path,"x") as f:
                data=input("Enter your data")
                f.write(data)
                print("File created successfully....")
        else:
            print("File is already exists")
    except Exception as err:
        print(f"An error occured as {err}")

def reading():
    try:
        name=input("Enter yur file name")
        path=Path(name)
        if path.exists():
            with open(path,"r") as f:
                file_data=f.read()
                print(f"Your file contains {file_data}")
        else:
            print("No such file exists...")
    except Exception as err:
        print(f"An error occure as {err}")

def updating():
    try:
        name=input("Enter your file name ")
        path=Path(name)
        if path.exists:
            print("Operation:")
            print("1 for renaming the file")
            print("2 for appending the file")
            print("3 Overwriting the file")
            choice=int(input("Enter your choice"))
            if choice==1:
                newName=input("Enter a new name for your file ")
                newPath=Path(newName)
                if not newPath.exists():
                    path.rename(newPath)
                    print("Renamed successfully...")
                else:
                    print("File already exists...")
            if choice==2:
                with open(path,"a") as f:
                    data=input("What do you want to update ")
                    f.write("\n"+data)
                    print("Successfully updated")
            if choice==3:
                with open(path,"w") as f:
                    data=input("What do you want to overwrite: ")
                    f.write("\n"+data)
                    print("Successfully overwritten")
    except Exception as err:
        print(f"An error occured like {err}")

def deleting():
    try:
        name=input("Enter your file name: ")
        path=Path(name)
        if path.exists():
            path.unlink()
            print("File got deleted")
        else:
            print("No such file present")
    except Exception as err:
        print("An error occured like {err}")
print("1 for creating a file")
print("2 for reading a file")
print("3 for updating a file")
print("4 for creating a file")

a=int(input("Enter your choice: "))

if a==1:
    creating()
if a==2:
    reading()
if a==3:
    updating()
if a==4:
    deleting() 


