import os, datetime, pathlib, shutil, sys

def Setup():
    input_dir = input("directory to sort(input): ")
    output_dir = input("output directory: ")
    return input_dir, output_dir

def UserFileConflict(file):
    all_flag = ""
    single_flag = "n"

    print("Warrning: The file with the name: " + file + " already exsists")
    bad_input = True
    while bad_input:
        user_dec = input("replace? y: yes, n: no, k, keep both (add '_all' to apple to all)")
        if len(user_dec) >= 1:
            first_char = user_dec.lower()[0]
            if first_char == "y" or first_char == "n" or first_char == "k":
                single_flag = first_char
                bad_input = False
            if user_dec.lower()[1:] == "_all":
                all_flag = first_char
    return single_flag, all_flag
                    

def GetTotalFiles(dir):
    file_counter = 0
    for subdir, dirs, files in os.walk(dir):
        for file in files:
            file_counter+=1
    return file_counter


def SortFiles(input_dir, output_dir):
    all_flag = "" # if the file already exists

    print("indexing... " + input_dir)
    total_file_count = GetTotalFiles(input_dir)

    current_file_count = 0
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(subdir, file)
            file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            move_dir = os.path.join(output_dir, str(file_date.year), str(file_date.strftime("%B")), str(file_date.day))
            move_file = os.path.join(move_dir, file)

            pathlib.Path(move_dir).mkdir(parents=True, exist_ok=True)
            if os.path.exists(move_file):
                single_flag = ""
                if all_flag == "":
                    single_flag, all_flag = UserFileConflict(move_file)
                if all_flag == "y" or single_flag == "y":
                    print("replacing file: "+move_file)
                    shutil.copyfile(file_path, move_file)
                if all_flag == "k" or single_flag == "k":
                    file_exists = True
                    i = 0
                    while file_exists:
                        file_no_ext, file_ext = os.path.splitext(file)
                        file_no_ext += "("+str(i)+")"
                        new_file_name = os.path.join(move_dir, file_no_ext + file_ext)
                        if not os.path.exists(new_file_name):
                            file_exists = False
                        i+=1
                    print("adding new file: "+new_file_name)
                    shutil.copyfile(file_path, new_file_name)
                if all_flag == "n" or single_flag == "n":
                    print("skipping file: "+file_path)
            else:
                shutil.copyfile(file_path, move_file)

            current_file_count +=1
            print(str(current_file_count) + "/"+str(total_file_count))





if __name__ == '__main__':
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
        output_dir = sys.argv[2]
        # print("Warrning: You are about to move")
    else:
        input_dir, output_dir = Setup()
    # SortFiles("input/", "output/")
    SortFiles(input_dir, output_dir)