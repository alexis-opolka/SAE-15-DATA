from os import system
from pathlib import Path, PurePath


def listToStr(list_line: list):
    rendered = ""
    for i in range(0, len(list_line)):
        if i < len(list_line)-1:
            rendered = rendered + list_line[i] + ","
        else:
            rendered = rendered + list_line[i] + "\n"
    return rendered

the_path = Path("./in/stats/csv/")
csv_files = []

### Get all the CSV files in the directory
### while assuring ourselves that they're really files
for element in the_path.iterdir(): # Path.iterdir() in order to iterate inside the directory
    if Path.is_file(element):
        if element.name[:2] == "FR":
            csv_files.append(element)

for file in csv_files:
    final_file = []
    filename = file.name.strip().split("\\")[-1];
    filename = filename.replace(".CSV", "")
    print("Opening", filename)
    with open(file, "rt", encoding="utf-8") as fin:
        fin = fin.readlines()
        for line in fin:
            line = line.strip().split(',')
            if len(line) < 6:
                if len(line) == 1:
                    line = ["" for i in range(0, 6)]
                line.insert(2, f"{line[1]}") 
            final_file.append("".join(listToStr(line)))
    with open(f"out/csv/{filename}.csv", "wt", encoding="utf-8") as fout:
        fout.write("".join(final_file) + "\n")
    print(f"{filename} completed")
