import json, enum
from copy import deepcopy
from platform import system

ERR_FILE_PATH = "Error: Only one file path has been provided."

class FileTypes(enum.Enum):
  Nan = 0
  Txt = 1
  Json = 2


class Steak:

  def __init__(self, args, full_path: str, fmt=False, show_refs=False):
    self.args = args                            # Program arguments.
    self.debug = args.debug                     # Display debug message when if true.
    self.pretty = args.pretty
    self.fmt = fmt                              # 
    self.show_refs = show_refs                  # Shows all items with associated refs
    self.full_path = full_path                  # The full path to the file.


  def get_script_name(file_path: str):
    delim = "/"
    
    if system().lower() == "windows":
      delim = "\\"

    split_path = file_path.split(delim)
    output = ""
    
    if len(split_path) > 1:
      output = split_path[len(split_path)-1]
    else:
      output = split_path
    
    return output


  def count_args(self):
    counter = 0

    if self.args.combine == True:
      counter += 1
    
    if self.args.subtract == True:
      counter += 1

    if self.args.pretty == True:
      counter += 1

    if self.args.ref == True:
      counter += 1

    if self.args.output != None:
      counter += 1
    
    return counter


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


  def parse_files(self):
    file_path_1 = f"{self.full_path}\\{self.args.file1}"
    file_path_2 = f"{self.full_path}\\{self.args.file2}"
    ftype_1 = Steak.get_file_type(file_path_1)
    ftype_2 = Steak.get_file_type(file_path_2)

    # Opens both files, converts each character to lower case and splits the lines in multiple lists.
    if ftype_1 != FileTypes.Json:
      with open(file_path_1) as f:
        f1_lines = Steak.double_split_lines(f.read().lower().split("\n"))
    else:
      f1_lines = Steak.read_json(file_path_1)

    if ftype_2 != FileTypes.Json:
      with open(file_path_2) as f:
        f2_lines = Steak.double_split_lines(f.read().lower().split("\n"))
    else:
      f2_lines = Steak.read_json(file_path_2)


    return [f1_lines, f2_lines]


  def convert_json(self) -> list:
    '''Function converts text file into the json format'''
    lines = []
    file_path = ""

    if self.args.file1 != None:
      file_path = f"{self.full_path}\\{self.args.file1}"
    elif self.args.file2 != None:
      file_path = f"{self.full_path}\\{self.args.file2}"
    
    f_type = Steak.get_file_type(file_path)

    if f_type != FileTypes.Json:
      with open(file_path) as f:
        lines = Steak.double_split_lines(f.read().lower().split("\n"))
    else:
      lines = Steak.read_json(file_path)

    json_content = Steak.separate_items_and_ref(lines)
    return json_content


  def get_combined_output(self) -> list:
    '''Function combines 2 files together and then removes duplicate lines.'''
    combined_lines = []
    
    pair = self.parse_files()
    f1_lines = pair[0]
    f2_lines = pair[1]

    for i in f1_lines:
      combined_lines.append(i)

    for i in f2_lines:
      combined_lines.append(i)

    # Combines the contents of each list and removes all duplicates.
    combined_content = Steak.separate_items_and_ref(combined_lines)
    return combined_content


  def get_duplicates(master_list: list, dup_list: list):
    output = []

    for i in master_list:

      for idx in range(len(dup_list)):
        if i[0] == dup_list[idx][0] and i[1] != [] and i[1] != [""]:
          output.append(i)
          break


    return output


  def subtract_from(self) -> list:
    '''Function removes the contents of file2 that exists in file1'''
    f1_items = []
    f2_items = []
    subtracted_list = []
    duplicate_list = []

    pair = self.parse_files()
    f1_lines = Steak.separate_items_and_ref(pair[0])
    f2_lines = Steak.separate_items_and_ref(pair[1])

    c_f1_lines = deepcopy(f1_lines)
    c_f2_lines = deepcopy(f2_lines)

    for i in c_f1_lines:
      f1_items.append(i[0])
      duplicate_list.append(i)

    for i in c_f2_lines:
      f2_items.append(i[0])
      duplicate_list.append(i)

    # Subtracts all lines the first file from the second file, showing all unique lines between the 2 files.
    first_set = set(f1_items)
    second_set = set(f2_items)
    subtracted_list = (second_set - first_set)
    subtracted_list = list(set(subtracted_list))

    dupes = Steak.get_duplicates(duplicate_list, c_f2_lines)
    if self.show_refs == True:
      return dupes

    output = []
    for i in subtracted_list:
      output.append([i, []])

    return output


  # def write_output(self, content: list):
  #   '''Function write output to a file.'''

  #   output = self.args.output
  #   ext = self.args.ft
  #   lines = ""
    
  #   # Check if filename and ext are empty or not.
  #   if output == None:
  #     output = "output.txt"

  #   if ext == None:
  #     ext = "txt"

  #   if len(content) < 1:
  #     print(f"Nothing to write to file [{output}]")
  #     return

  #   # Code block adds a new line to the end of each line if not already present.
  #   for i in content:
  #     temp_ln = i
  #     if len(temp_ln) > 0 and temp_ln[len(temp_ln)-1] != "\n":
  #       temp_ln += "\n"

  #     lines += temp_ln
  
  #   # Writes content to a file.
  #   filepath = f"{self.full_path}\\{output}.{ext}"
  #   with open(filepath, "w") as f:
  #     n_bytes = f.write(lines)
      
  #     if n_bytes > 0:
  #       print(f"Successfully wrote {len(content)} lines ({n_bytes}) bytes to file '{filepath}'")


  def write_json(self, content: str):
    '''Writes content as a json file.'''

    output = self.args.output

    if output == None:
      output = "output"

    filepath = f"{self.full_path}\\{output}"
    if filepath.endswith(".json") == False:
      filepath += ".json"

    with open(filepath, "w") as f:
      n_bytes = f.write(content)

      if n_bytes > 0:
        print(f"Successfully wrote {len(content)} bytes to {filepath}")


  def display_output(self, text: str):
    if self.debug == True:
      print(repr(text))

    elif self.pretty == True:
      print(text)
    
    else:
      json_data = ""

      try:
        json_data = json.loads(text)
      except json.JSONDecodeError:
        print("Unable to display output - JsonDecodeError")
      
      data = Steak.check_json_error(json_data, "data")
      
      for i in data:
        item = Steak.check_json_error(i, "ioc")
        ref = Steak.check_json_error(i, "ref")

        if len(ref) == 0:
          print(f"{item}")
        elif len(ref) > 0:
          print(f"{item} -- {ref}")


  def separate_items_and_ref(content: list):
    '''Function remove all duplicate elements from items and refs.
    It also creates a new list from the content list to correctly align each item element with the corresponding ref element.
    Returns a double indexed array [[item, ref]]'''

    items = []
    refs = []

    # loop creates two lists that will be of equal lengths to the content list.
    for i in content:
      items.append(i[0])
      refs.append([])

    # All duplicates are removed from items and a deep copy is created to prevent modifying the content list.
    items = list(set(items))
    new_content = deepcopy(content)

    # Code block modifies the items in new_content and turns all strings into lists
    for i in range(len(new_content)):
      if type(new_content[i][1]) == str:
        new_content[i][1] = [new_content[i][1]]
      
    # Code block sorts the information in refs by inserting the correct ref_element at the same index values as in new content.
    for i in new_content:
      ref_item = None
      in_counter = 0

      # The order of the items list will be jumbled when the duplicate elements are removed.
      # Code will iterate over items and compare the element that is stored in i.
      # Once found, the corresponding ref value that is paired with each item will be assigned to the variable ref_item.
      for idx in items:
        if i[0] == idx:
          ref_item = i[1]
          break

        # Once the we break out of the loop, in_counter will be store the position the ref_element should be inserted.
        in_counter += 1
    
      # Refs will be stored in the same order as the items list.
      refs[in_counter].extend(ref_item)
        
    # This code block will remove all duplicate ref_elements stored in each ref.
    c_refs = deepcopy(refs)
    for i in range(len(c_refs)):
      refs[i] = list(set(c_refs[i]))

    # Code block will create a double indexed list from items and refs
    output = []
    for i in range(len(items)):
      output.append([items[i], refs[i]])

    return output


  def double_split_lines(content: list):
    output = []

    for i in content:
      line_chunks = i.split(":")

      if len(line_chunks) > 1:
        item = line_chunks[0]
        ref = line_chunks[1]
      else:
        item = line_chunks[0]
        ref = []

      output.append([item, ref])

    return output


  # def remove_empties(refs: list):
  #   output = deepcopy(refs)

  #   if len(output) == 1:
  #     if output[0] == "[]":
  #       output.clear()
    
  #   return output


  def get_json(contents: list):
    '''Creates a json object out the contents of each file.'''

    output = {
      "data": []
    }

    for i in contents:
      # clean_ref = Steak.remove_empties(i[1])
      output["data"].append({"ioc": i[0], "ref": i[1]})

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
      ref = Steak.check_json_error(i, "ref")

      if ioc != None and ioc != "":
        lines.append([ioc, ref])

    return lines