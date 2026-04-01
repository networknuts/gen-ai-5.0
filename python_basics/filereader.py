user_file = input("Enter the file path to read: ")

f = open(user_file,"r")
print("FILE OPENED SUCCESSFULLY!")
for line in f.readlines():
    print(line.strip())
print("FILE CONTENT PRINTED SUCCESSFULLY")

f.close()
print("FILE CLOSED SUCCESSFULLY!")