import os, argparse, sys
from src.steak import Steak

title = '''
,d88~~\   d8   ,e,         888   _                 ,d88~~\   d8                       888   _   
8888    _d88__  "   e88~~\ 888 e~ ~  Y88b  /       8888    _d88__  e88~~8e    /~~~8e  888 e~ ~  
`Y88b    888   888 d888    888d8b     Y888/        `Y88b    888   d888  88b       88b 888d8b    
 `Y88b,  888   888 8888    888Y88b     Y8/          `Y88b,  888   8888__888  e88~-888 888Y88b   
   8888  888   888 Y888    888 Y88b     Y             8888  888   Y888    , C888  888 888 Y88b  
\__88P'  "88_/ 888  "88__/ 888  Y88b   /           \__88P'  "88_/  "88___/   "88_-888 888  Y88b 
                                     _/                                                         '''


def main():
  parser = argparse.ArgumentParser(description="None")
  parser.add_argument("-1", "--file1", action="store", help="The first input file", required=True)
  parser.add_argument("-2", "--file2", action="store", help="The second input file", required=True)
  parser.add_argument("-c", "--combine", action="store_true", help="Combine 2 files together and remove duplicate lines")
  parser.add_argument("-d", "--difference", action="store_true", help="Get the difference between 2 files")
  parser.add_argument("-o", "--output", action="store", help="Write the new output to a file")
  parser.add_argument("--ft", action="store", help="Write output to a specific file type. Options [txt, json]")
  parser.add_argument("-D", "--debug", action="store_true", help="Display all characters including unprintables")
  parser.add_argument("-s", "--subtract", action="store_true", help="Subtract lines from file2 using contents of file1")
  parser.add_argument("-r", "--ref", action="store", help="Show each reference for each line if any. File1 or 2 must be in json format")

  sys_args = sys.argv
  for i in sys_args:
    if "-h" in i or "--help" in i:
      print(f"\n\n{title}\n\n")
      break

  args = parser.parse_args()
  full_path = os.getcwd()
  sticky = Steak(args, full_path)
  out = []

  if args.file1 != None and args.file2 != None:
    
    if args.combine == True:
      out = sticky.get_combined_output()

    elif args.difference == True:
      out = sticky.get_difference()

    elif args.subtract == True:
      out = sticky.subtract_from()

    if args.ft != None:
      if args.ft == "json":
        out = Steak.get_json(out)

    if args.output != None and len(out) > 0:
      if args.ft == "txt":
        sticky.write_output(out)
      elif args.ft == "json":
        sticky.write_json(out)
      else:
        sticky.write_output(out)
    
    elif args.output == None:
      if args.ft == None or args.ft == "txt":
        for i in out:
          sticky.display_output(i)
      else:
        sticky.display_output(out)


if __name__ == "__main__":
  main()