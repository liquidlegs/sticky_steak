import os, argparse, sys
from src.steak import Steak, ERR_FILE_PATH

title = '''
,d88~~\   d8   ,e,         888   _                 ,d88~~\   d8                       888   _   
8888    _d88__  "   e88~~\ 888 e~ ~  Y88b  /       8888    _d88__  e88~~8e    /~~~8e  888 e~ ~  
`Y88b    888   888 d888    888d8b     Y888/        `Y88b    888   d888  88b       88b 888d8b    
 `Y88b,  888   888 8888    888Y88b     Y8/          `Y88b,  888   8888__888  e88~-888 888Y88b   
   8888  888   888 Y888    888 Y88b     Y             8888  888   Y888    , C888  888 888 Y88b  
\__88P'  "88_/ 888  "88__/ 888  Y88b   /           \__88P'  "88_/  "88___/   "88_-888 888  Y88b 
                                     _/                                                         '''
def file_args(file_path: str, sticky: Steak):
  args = sticky.args
  
  if args.combine == True:
    print(f"{ERR_FILE_PATH} Cannot combine {args.file1} with nothing")

  elif args.subtract == True:
    print(f"{ERR_FILE_PATH} Cannot subtract the contents of {args.file1} with nothing")

  elif sticky.fmt == True:
    out = sticky.convert_json()

  if len(out) > 0:
    out = Steak.get_json(out)

  if args.output != None:
    if len(out) > 0:
      sticky.write_json(out)
  
  elif args.output == None:
    sticky.display_output(out)


def main():
  parser = argparse.ArgumentParser(description="None")
  parser.add_argument("-1", "--file1", action="store", help="The first input file", required=False)
  parser.add_argument("-2", "--file2", action="store", help="The second input file", required=False)
  parser.add_argument("-c", "--combine", action="store_true", help="Combine 2 files together and remove duplicate lines")
  parser.add_argument("-o", "--output", action="store", help="Write the new output to a file")
  parser.add_argument("--debug", action="store_true", help="Display debug information / messages")
  parser.add_argument("-p", "--pretty", action="store_true", help="Display the raw formatted json output")
  parser.add_argument("-s", "--subtract", action="store_true", help="Subtract lines from file2 using contents of file1")
  parser.add_argument("-r", "--ref", action="store_true", help="Does the same as --subtract, but only shows duplicate items")
  parser.add_argument("-t", "--ctime", action="store", help="Adds a custom date to an investigation for a particular ioc")
  parser.add_argument("-O", "--overwrite-date", action="store_true", help="Overwrites the date in an investigation with current date/time")
  parser.add_argument("-d", "--delim", action="store")
  parser.add_argument("-P", "--priority", action="store", help="Defines how often an ioc should be reinvestigated. Options: [p1, p2, p3, p4, p5]")

  sys_args = sys.argv
  for i in sys_args:
    if "-h" in i or "--help" in i:
      print(f"\n\n{title}\n\n")
      break

  args = parser.parse_args()
  full_path = os.getcwd()
  sticky = Steak(args, full_path)
  out = []

  if args.combine != True and args.subtract != True:
    sticky.fmt = True

  if args.file1 != None and args.file2 != None:
    
    if sticky.count_args() < 1:
      print("Error: File paths have been provided, but no options specified - No action taken.")

    if args.ref == True and args.subtract == False:
      args.subtract = True
      sticky.args.subtract = True

    if args.combine == True:
      out = sticky.get_combined_output()

    elif args.subtract == True:
      sticky.show_refs = args.ref
      out = sticky.subtract_from()

    if len(out) > 0:
      out = Steak.get_json(args, out)
    else: return

    if args.output != None:
      if len(out) > 0:
        sticky.write_json(out)
    
    elif args.output == None:
      sticky.display_output(out)

  elif args.file1 != None and args.file2 == None:
    file_args(args.file1, sticky)
  
  elif args.file1 == None and args.file2 != None:
    file_args(args.file2, sticky)

  else:
    print(f"Error: No file(s) specified - Use python {Steak.get_script_name(sys.argv[0])} -h for help")
    return


if __name__ == "__main__":
  main()