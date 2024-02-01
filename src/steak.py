import json, enum, os
from copy import deepcopy
from platform import system
from datetime import date, timedelta
from src.colourterm import ColourTerm as C
C.enable_colour_terminal()

ERR_FILE_PATH = "Error: Only one file path has been provided."
SPL_LN_DELIM = ":"


class FileTypes(enum.Enum):
  Nan = 0
  Txt = 1
  Json = 2


class Steak():

  def __init__(self, args, full_path: str, fmt=False, show_refs=False):
    self.args = args                                # Program arguments.
    self.debug = args.debug                         # Display debug message when if true.
    self.pretty = args.pretty                       # Displays output as well formatted json.
    self.fmt = fmt                                  # Allows file contents to be printed if combine and subtract flags are == None
    self.show_refs = show_refs                      # Shows all items with associated refs.
    self.full_path = full_path                      # The full path to the file.
    self.spl_delim = args.delim                     # Controls how refs are added.
    self.config = None                              # Holds the config file.
    self.enable_colour = C.enable_colour_terminal() # Enables coloured text.

    if self.spl_delim == None:
      self.spl_delim = SPL_LN_DELIM

    self.dprint("Searching for config file")

    if self.config_exists() == True:
      self.dprint("Config file exists")
      self.config = self.load_config_file()

      if self.config != None:
        self.dprint("Successfully loaded config file")
    else:
      self.config = Steak.generate_config_string()
      self.dprint("Generating config string")


  def dprint(self, text: str):
    if self.debug == True:
      if self.enable_colour == True:
        print(f"{C.f_red('Debug')} {C.fd_cyan('=>')} {C.fd_yellow(text)}")
      else:
        print(f"Debug => {text}")


  def err(self, text: str):
    if self.enable_colour == True:
      print(f"{C.f_red('Error')}: {text}")
    else:
      print(f"Error: {text}")


  def get_delim():
    delim = "/"

    if system().lower() == "windows":
      delim = "\\"

    return delim


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
    '''Function prevents the user from specifying files via the commandline and not perfomring an action with any of the data.'''

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

    if self.args.overwrite_date == True:
      counter += 1

    if self.args.ctime != None:
      counter += 1

    if self.spl_delim != None:
      counter += 1

    if self.args.priority != None:
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
        f1_lines = Steak.double_split_lines(f.read().lower().split("\n"), self.spl_delim)
    else:
      f1_lines = Steak.read_json(file_path_1)

    if ftype_2 != FileTypes.Json:
      with open(file_path_2) as f:
        f2_lines = Steak.double_split_lines(f.read().lower().split("\n"), self.spl_delim)
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
        lines = Steak.double_split_lines(f.read().lower().split("\n"), self.spl_delim)
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

    # Adds addtional fields that comes after iocs and refs
    d_combined_content = Steak.add_addtional_fields(combined_lines, combined_content)

    combined_content = d_combined_content
    return combined_content


  def add_addtional_fields(combined_lines: list, combined_content: list):
    c_combined_content = []
    d_combined_content = []
    
    for idx in combined_content:

      for i in combined_lines:

        if i[0] == idx[0]:

          if len(i) < 3:
            new_item = idx
            new_item.append(None)
            new_item.append(None)
            new_item.append(None)
            c_combined_content.append(new_item)
            break
          
          elif len(i) < 5 and len(i) > 2:
            new_item = idx
            new_item.append(i[2])
            new_item.append(i[3])
            new_item.append(None)
            c_combined_content.append(new_item)
            break

          elif len(i) == 5:
            new_item = idx
            new_item.append(i[2])
            new_item.append(i[3])
            new_item.append(i[4])
            c_combined_content.append(new_item)
            break

    for i in c_combined_content:
      d_combined_content.append(i[:5])

    return d_combined_content


  def get_duplicates(master_list: list, dup_list: list):
    output = []

    for i in master_list:

      for idx in range(len(dup_list)):
        if i[0] == dup_list[idx][0] and i[1] != [] and i[1] != [""]:
          output.append(i)
          break

    output = Steak.separate_items_and_ref(output)
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

    d_dupes = []
    dupes = Steak.get_duplicates(duplicate_list, c_f2_lines)  

    for i in pair[0]:
      for idx in dupes:
        
        if i[0] == idx[0]:
          if i[1] != []:
            new_item = []
            new_item.append(idx[0])
            new_item.append(idx[1])
            new_item.append(i[2])
            new_item.append(i[3])
            new_item.append(i[4])
            d_dupes.append(new_item)


    if self.show_refs == True:
      return d_dupes

    output = []
    for i in subtracted_list:
      output.append([i, [], None, None, None])

    return output


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

    if self.pretty == True:
      print(text)
    
    else:
      json_data = ""

      try:
        json_data = json.loads(text)
      except json.JSONDecodeError:
        self.err("Unable to display output - JsonDecodeError")
      
      data = Steak.check_json_error(json_data, "data")
      
      for i in data:
        item = Steak.check_json_error(i, "ioc")
        ref = Steak.check_json_error(i, "ref")

        if len(ref) == 0 or self.args.combine == True:
          print(f"{item}")
        
        elif len(ref) > 0 and self.show_refs == True:
          lseen = Steak.check_json_error(i, "last_seen")
          sev = Steak.check_json_error(i, "priority")

          if sev != None:
            sev = sev.lower()
            target = Steak.check_json_error(self.config, sev)
            seen = self.convert_string_to_date(lseen)
            today = date.today()
            result = today - seen

            if result.days > target:
              rsev = sev.upper()

              if rsev == "P1":
                rsev = C.b_red(C.f_white(rsev))
              elif rsev == "P2":
                rsev = C.f_red(rsev)
              elif rsev == "P3":
                rsev = C.f_yellow(rsev)
              elif rsev == "P4":
                rsev = C.f_green(rsev)
              elif rsev == "P5":
                rsev = C.f_blue(rsev)

              print(
                f"[{' '*3}{rsev}{' '*3}] {item} -- {ref} | {sev})"
              )    
            else:
              print(f"{item} -- {ref}")
          
          else:
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
      refs[i] = Steak.split_refs(c_refs[i])

    # Code block will create a double indexed list from items and refs
    output = []
    for i in range(len(items)):
      output.append([items[i], refs[i]])

    return output


  def split_refs(refs: list):
    output = []

    if len(refs) == 0:
      return refs

    for i in refs:
      element = i.split(",")
      output.extend(element)

    output = list(set(output))
    return output


  def double_split_lines(content: list, delim: str):
    output = []

    for i in content:
      line_chunks = i.split(delim)

      if len(line_chunks) > 1:
        item = line_chunks[0]
        ref = line_chunks[1]
      else:
        item = line_chunks[0]
        ref = []

      output.append([item, ref])

    return output


  def get_json(self, args, contents: list):
    '''Creates a json object out the contents of each file.'''

    output = {
      "data": []
    }

    first_seen = None             # Defines the first and last time that an ioc was investigated.
    last_seen = None
    sev = ""

    for i in contents:
      # Sets tje prioirty to the value as specified by the user.
      if args.priority != None:
        sev = args.priority.upper()
      else:
        sev = None
      
      self.dprint(i)

      # The first seen value should only be created when the first_seen value is null.
      if i[2] == None:
        first_seen = str(date.today())
      else:
        first_seen = i[2]

      # Creates the last seen field and sets it to the current date.
      if i[3] == None:
        last_seen = str(date.today())
      
      # Overwrites the last_date to the current date if the flag is set to true.
      if args.overwrite_date == True:
        last_seen = str(date.today())
      
      # Overwrites the last_date with a custom date entered via the commandline.
      elif args.ctime != None:
        last_seen = self.convert_string_to_date(args.ctime)
        
        if last_seen != None:
          last_seen = str(last_seen)
        else:
          last_seen = i[3]
      
      else:
        if i[3] != None:
          last_seen = i[3]

      # Sets the priority to P5 as the default or whatever is stored in the file.
      if i[4] == None:
        if sev == None:
          sev = "P5"
        
        # Santize input that the user has provided.
        elif sev != None:
          if sev != "P1" and sev != "P2" and sev != "P3" and sev != "P4" and sev != "P5":
            sev = "P5"

      elif i[4] != None:
        sev = i[4]

      self.dprint(sev)
      output["data"].append(
        {
          "ioc": i[0],
          "ref": i[1],
          "first_seen": first_seen,
          "last_seen": last_seen,
          "priority": sev
        }
      )

    output_json = json.dumps(output, indent=2)
    return output_json
  

  def check_json_error(data, key):
    '''Catches all json key errors in a separate function to prevent the program crashing in the middle of a loop.'''

    out = None
    
    try:
      out = data[key]
      return out
    except KeyError:
      return out


  def read_json(filename: str):
    '''Reads in the json file as a python list.'''
    
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
      first_seen = Steak.check_json_error(i, "first_seen")
      last_seen = Steak.check_json_error(i, "last_seen")
      sev = Steak.check_json_error(i, "priority")

      if ioc != None and ioc != "":
        lines.append([ioc, ref, first_seen, last_seen, sev])

    return lines
  

  def convert_string_to_date(self, custom_date: str) -> date:
    '''Converts a date as a string to a datetime object.'''
    
    dt = []
    delim = ""

    if "-" in custom_date:
      delim = "-"
    elif "/" in custom_date:
      delim = "/"

    if delim == "":
      self.err("date is in unknown format. Please use dd/mm/yyyy or dd-mm-yyyy")
      return
    
    cdate = custom_date.split(delim)
    for i in cdate:
      dt.append(int(i))

    if len(dt) < 1:
      self.err(f"unable to convert {custom_date} to datetime format")
      return
    
    out = date(dt[0], dt[1], dt[2])
    return out


  def auto_generate_config():
    '''Function writes the default config file to the root of the project directory.'''

    output = {
      "p5": 365,
      "p4": 180,
      "p3": 120,
      "p2": 40,
      "p1": 7
    }

    content = json.dumps(output, indent=2)
    with open("config.json", "w") as f:
      f.write(content)

  
  def generate_config_string() -> dict:
    output = {
      "p5": 365,
      "p4": 180,
      "p3": 120,
      "p2": 40,
      "p1": 7
    }

    return output


  def load_config_file(self) -> dict:
    path = f"{self.full_path}{Steak.get_delim()}config.json"
    buffer = ""
    output = ""

    with open(path, "r") as f:
      buffer = f.read()

    try:
      output = json.loads(buffer)
    except Exception as e:
      self.err("failed to load config file")
    
    return output


  def config_exists(self) -> bool:
    '''Function checks if the file config file exists and returns a boolean if so.'''
    
    delim = "/"

    if system().lower() == "windows":
      delim = "\\"

    # Code block checks if the config file exists and if so returns True.
    # However if not the case, the config will be generated and checked again.
    full_path = os.getcwd() + delim + "config.json"
    if os.path.exists(full_path) == True:
      return True
    else:
      self.dprint("Generating default config file")
      Steak.auto_generate_config()

    # If the config still does exist after being generated, there is likely a 
    # permission issue preventing the file from written to the disk.
    if os.path.exists(full_path) == True:
      return True
    else:
      return False