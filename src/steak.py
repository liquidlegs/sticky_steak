import json, enum

class FileTypes(enum.Enum):
  Nan = 0
  Txt = 1
  Json = 2


class Steak:

  def __init__(self, args, full_path: str):
    self.args = args                            # Program arguments.
    self.debug = args.debug                     # Display debug message when if true.
    self.full_path = full_path                  # The full path to the file.


  def get_file_type(filename: str) -> FileTypes:
    '''Determines the file type and returns the extension as an enum.'''
    
    out = FileTypes.Nan
    chk = filename.split(".")

    if len(chk) > 1:
      t = chk[1]
      
      if t == "txt":
        out = FileTypes.Txt
      elif t == "json":
        out = FileTypes.Json
    
    return out


  def get_difference(self) -> list:
    '''Function combines 2 files together to get the difference between them.'''
    
    f1_lines = []
    f2_lines = []
    difference = []
    
    # Opens both files, converts each character to lower case and splits the lines in multiple lists.
    with open(f"{self.full_path}\\{self.args.file1}") as f:
      f1_lines = f.read().lower().split("\n")

    with open(f"{self.full_path}\\{self.args.file2}") as f:
      f2_lines = f.read().lower().split("\n")    
    
    first_set = set(f1_lines)
    second_set = set(f2_lines)

    # Performs an xor operation to get the difference between the 2 sets.
    difference = first_set ^ second_set
    return list(difference)


  def get_combined_output(self) -> list:
    '''Function combines 2 files together and then removes duplicate lines.'''
    f1_lines = []
    f2_lines = []
    combine_output = []
    output = []
    
    file_path_1 = f"{self.full_path}\\{self.args.file1}"
    file_path_2 = f"{self.full_path}\\{self.args.file2}"
    ftype_1 = Steak.get_file_type(file_path_1)
    ftype_2 = Steak.get_file_type(file_path_2)

    # Opens both files, converts each character to lower case and splits the lines in multiple lists.
    if ftype_1 != FileTypes.Json:
      with open(file_path_1) as f:
        f1_lines = f.read().lower().split("\n")
    else:
      f1_lines = Steak.read_json(file_path_1)

    if ftype_2 != FileTypes.Json:
      with open(file_path_2) as f:
        f2_lines = f.read().lower().split("\n")
    else:
      f2_lines = Steak.read_json(file_path_2)

    combine_output.extend(f1_lines)
    combine_output.extend(f2_lines)

    # Combines the contents of each list and removes all duplicates.
    output = list(set(combine_output))
    
    return output


  def subtract_from(self) -> list:
    '''Function removes the contents of file2 that exists in file1'''
    f1_lines = []
    f2_lines = []
    subtracted_list = []

    # Opens both files, converts each character to lower case and splits the lines in multiple lists.
    with open(f"{self.full_path}\\{self.args.file1}") as f:
      f1_lines = f.read().lower().split("\n")

    with open(f"{self.full_path}\\{self.args.file2}") as f:
      f2_lines = f.read().lower().split("\n")

    first_set = set(f1_lines)
    second_set = set(f2_lines)

    # Subtracts all lines the first file from the second file, showing all unique lines between the 2 files.
    subtracted_list = (second_set - first_set)
    return list(subtracted_list)


  def write_output(self, content: list):
    '''Function write output to a file.'''

    output = self.args.output
    ext = self.args.ft
    lines = ""
    
    # Check if filename and ext are empty or not.
    if output == None:
      output = "output.txt"

    if ext == None:
      ext = "txt"

    if len(content) < 1:
      print(f"Nothing to write to file [{output}]")
      return

    # Code block adds a new line to the end of each line if not already present.
    for i in content:
      temp_ln = i
      if len(temp_ln) > 0 and temp_ln[len(temp_ln)-1] != "\n":
        temp_ln += "\n"

      lines += temp_ln
  
    # Writes content to a file.
    filepath = f"{self.full_path}\\{output}.{ext}"
    with open(filepath, "w") as f:
      n_bytes = f.write(lines)
      
      if n_bytes > 0:
        print(f"Successfully wrote {len(content)} lines ({n_bytes}) bytes to file '{filepath}'")


  def write_json(self, content: str):
    '''Writes content as a json file.'''

    output = self.args.output
    ext = self.args.ft

    if output == None:
      output = "output"

    if ext == None:
      ext = "json"

    filepath = f"{self.full_path}\\{output}.{ext}"
    with open(filepath, "w") as f:
      n_bytes = f.write(content)

      if n_bytes > 0:
        print(f"Successfully wrote {len(content)} bytes to {filepath}")


  def display_output(self, text: str):
    if self.debug == True:
      print(repr(text))
    else:
      print(text)

  
  def get_json(contents: list):
    '''Creates a json object out the contents of each file.'''
    
    output = {
      "data": []
    }

    for i in contents:
      output["data"].append({"ioc": i, "ref": []})

    output_json = json.dumps(output, indent=2)
    return output_json
  

  def check_json_error(data, key):
    out = None
    
    try:
      out = data[key]
      return out
    except KeyError:
      return out


  def read_json(filename: str):
    lines = []
    json_obj = None

    buffer = ""
    with open(filename, "r") as f:
      buffer = f.read()

    json_obj = json.loads(buffer)
    data = Steak.check_json_error(json_obj, "data")

    for i in data:
      ioc = Steak.check_json_error(i, "ioc")
      if ioc != None and ioc != "":
        lines.append(ioc)

    return lines