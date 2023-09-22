import os, argparse, sys

title = '''
,d88~~\   d8   ,e,         888   _                 ,d88~~\   d8                       888   _   
8888    _d88__  "   e88~~\ 888 e~ ~  Y88b  /       8888    _d88__  e88~~8e    /~~~8e  888 e~ ~  
`Y88b    888   888 d888    888d8b     Y888/        `Y88b    888   d888  88b       88b 888d8b    
 `Y88b,  888   888 8888    888Y88b     Y8/          `Y88b,  888   8888__888  e88~-888 888Y88b   
   8888  888   888 Y888    888 Y88b     Y             8888  888   Y888    , C888  888 888 Y88b  
\__88P'  "88_/ 888  "88__/ 888  Y88b   /           \__88P'  "88_/  "88___/   "88_-888 888  Y88b 
                                     _/                                                         '''

def get_difference(args, full_path: str) -> list:
  '''Function combines 2 files together to get the difference between them.'''
  
  f1_lines = []
  f2_lines = []
  difference = []
  
  with open(f"{full_path}\\{args.file1}") as f:
    f1_lines = f.read().split("\n")

  with open(f"{full_path}\\{args.file2}") as f:
    f2_lines = f.read().split("\n")    
  
  first_set = set(f1_lines)
  second_set = set(f2_lines)
  difference = first_set ^ second_set

  return list(difference)


def get_combined_output(args, full_path: str) -> list:
  '''Function combines 2 files together and then removes duplicate lines.'''
  f1_lines = []
  f2_lines = []
  combine_output = []
  output = []
  
  with open(f"{full_path}\\{args.file1}") as f:
    f1_lines = f.read().split("\n")

  with open(f"{full_path}\\{args.file2}") as f:
    f2_lines = f.read().split("\n")

  combine_output.extend(f1_lines)
  combine_output.extend(f2_lines)
  output = list(set(combine_output))
  
  return output


def subtract_from(args, full_path: str) -> list:
  '''Function removes the contents of file2 that exists in file1'''
  f1_lines = []
  f2_lines = []
  subtracted_list = []

  with open(f"{full_path}\\{args.file1}") as f:
    f1_lines = f.read().split("\n")

  with open(f"{full_path}\\{args.file2}") as f:
    f2_lines = f.read().split("\n")

  first_set = set(f1_lines)
  second_set = set(f2_lines)
  subtracted_list = (second_set - first_set)
  
  return list(subtracted_list)


def write_output(args, content: list, full_path: str):
  '''Function write script output to a file.'''

  output = args.output
  lines = ""
  
  if output == None:
    output = "output.txt"

  if len(content) < 1:
    print(f"Nothing to write to file [{output}]")
    return

  for i in content:
    temp_ln = i
    if len(temp_ln) > 0 and temp_ln[len(temp_ln)-1] != "\n":
      temp_ln += "\n"

    lines += temp_ln
  
  with open(f"{full_path}\\{output}", "w") as f:
    n_bytes = f.write(lines)
    
    if n_bytes > 0:
      print(f"Successfully wrote {len(content)} lines ({n_bytes}) bytes to file '{full_path}\\{output}'")


def display_output(args, text: str):
  if args.debug == True:
    print(repr(text))
  else:
    print(text)


def main():
  parser = argparse.ArgumentParser(description="None")
  parser.add_argument("-1", "--file1", action="store", help="The first input file", required=True)
  parser.add_argument("-2", "--file2", action="store", help="The second input file", required=True)
  parser.add_argument("-c", "--combine", action="store_true", help="Combine 2 files together and remove duplicate lines")
  parser.add_argument("-d", "--difference", action="store_true", help="Get the difference between 2 files")
  parser.add_argument("-o", "--output", action="store", help="Write the new output to a file")
  parser.add_argument("-D", "--debug", action="store_true", help="Display all characters including unprintables")
  parser.add_argument("-s", "--subtract", action="store_true", help="Subtract lines from file2 using contents of file1")

  sys_args = sys.argv
  for i in sys_args:
    if i == "-h" or "--help":
      print(f"\n\n{title}\n\n")
      break

  args = parser.parse_args()
  full_path = os.getcwd()
  out = []

  if args.file1 != None and args.file2 != None:
    if args.combine == True:
      out = get_combined_output(args, full_path)

    elif args.difference == True:
      out = get_difference(args, full_path)

    elif args.subtract == True:
      out = subtract_from(args, full_path)

    if args.output != None:
      if len(out) > 0:
        write_output(args, out, full_path)
    
    elif args.output == None:
      for i in out:
        display_output(args, i)


if __name__ == "__main__":
  main()