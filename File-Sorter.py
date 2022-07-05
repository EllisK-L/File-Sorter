import os, datetime, pathlib, shutil

def Setup():
    input_dir = input("directory to sort")
    output_dir = input("output directory")
    return input_dir, output_dir    


def SortFiles(input_dir, output_dir):
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            file_path = os.path.join(subdir, file)

            print(file_path)
            print(os.path.getmtime(file_path))
            file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            print(file_date.year)

            move_dir = os.path.join(output_dir, str(file_date.year), str(file_date.strftime("%B")), str(file_date.day))
            move_file = os.path.join(move_dir, file)
            pathlib.Path(move_dir).mkdir(parents=True, exist_ok=True)
            shutil.copyfile(file_path, move_file)





if __name__ == '__main__':
    # input_dir, output_dir = Setup()
    SortFiles("input/", "output/")