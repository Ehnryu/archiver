
import argparse
import time
import sys
import getopt
import subprocess
import os
import sys
from sys import platform
import json
import base64

def send_help():
    print('USAGE: build [options]')
    print('A custom archiver tool created by Ehnryu\n')
    print('Basic options:\n')
    print('--compress : compress an archive\n')



advanced = ["compress =","help","decompress =","encrypt = ","decrypt =","dc ="]



def encbase64(message):
  message_bytes = message.encode('ascii')
  base64_bytes = base64.b64encode(message_bytes)

  base64_message = base64_bytes.decode('ascii')
  return base64_message

def decbase64(base64_message):
  base64_bytes = base64_message.encode('ascii')
  message_bytes = base64.b64decode(base64_bytes)
  message = message_bytes.decode('ascii')
  return message

def filepaths(directory):
    """
    This function will generate the file names in a directory 
    tree by walking the tree either top-down or bottom-up. For each 
    directory in the tree rooted at directory top (including top itself), 
    it yields a 3-tuple (dirpath, dirnames, filenames).
    """
    file_paths = []  # List which will store all of the full filepaths.
    dirs = []

    # Walk the tree.
    for root, directories, files in os.walk(directory):
        for dir in directories:
          dirpath = os.path.join(root, dir)
          dirs.append(dirpath)
        for filename in files:
            # Join the two strings in order to form the full filepath.
            filepath = os.path.join(root, filename)
            file_paths.append(filepath)  # Add it to the list.

    return {"paths":file_paths,"dir":dirs}  # Self-explanatory.

def run(command):
    subprocess.check_output(command,shell=True)

def archiver():

    argv = sys.argv[1:]
    opts = []
    try:
      opts, args = getopt.getopt(argv, "c:hd:e:",advanced)

    except:
        print("ERROR: Invalid arguments provided.")
        send_help()

    for opt, arg in opts:
        if opt in ["-h","--help"]:
          send_help()
        if opt in ["--dc","--decrypt"]:
          file = arg
          jfile = file.replace(".erc",".json")
          name = file.replace(".erc","")
          key = arg[0]
        if opt in ["-e","--encrypt"]:
          file = arg
          jfile = file.replace(".arc",".json")
          name = file.replace(".arc","")
          key = arg[0]
          os.system(f"mv {os.getcwd()}/{file} {os.getcwd()}/{jfile}")
          with open(f"{os.getcwd()}/{jfile}") as x:
            j = json.load(x)
            j["./#key"] = key
          with open(f"{os.getcwd()}/{jfile}","w") as x:
            json.dump(j,x)
          with open(f"{os.getcwd()}/{jfile}") as x:
            content = x.read()
            content = encbase64(content)
            with open(f"{os.getcwd()}/{jfile}","w") as z:
              z.write(content)
          os.system(f"mv {os.getcwd()}/{jfile} {os.getcwd()}/{name}.erc")
        if opt in ["-d","--decompress"]:
          cfiles = []
          start = time.time()
          verbose = False
          if "-v" in args:
            verbose = True
            args.remove("-v")
          filex = 0
          file = arg
          try:
            output = args[0].replace(".arc","")
          except IndexError:
            output = "temp"
          e = file.replace(".arc",".json")
          os.system(f"mv {os.getcwd()}/{file} {os.getcwd()}/{e}")
          with open(f"{os.getcwd()}/{e}") as x:
            x = json.load(x)
          for item in x:
            cfiles.append(item)
            filex += 1
          if filex == 1:
            if verbose:
              print(f"Decompressing {cfiles[0]}")
            os.system(f"touch {os.getcwd()}/{cfiles[0]}")
            with open(f"{os.getcwd()}/{cfiles[0]}") as z:
              z.write(x[cfiles[0]])
            end = time.time()
            y = ""
            if verbose:
              y = f"in {end - start} second(s)"
            print(f"Decompressed {filex} file to {cfiles[0]} {y}")
          else:
            os.system(f"mkdir {os.getcwd()}/{output}")
            dirs = x["./#dir"]
            for item in dirs:
              os.system(f"mkdir {os.getcwd()}/{output}/{item}")
            for item in x:
              if item != "./#dir" and item != "./#pwd" and item != "./#key":


                pat = x[item]["path"]
                filename = item.replace("./","")
                pat = pat.replace("./","")
                if verbose:
                  print(f"Decompressing {output}/{pat}...")
                
                
                with open(f"{os.getcwd()}/{output}/{pat}","w") as z:
                  z.write(str(x[item]["content"]))
            end = time.time()
            y = ""
            if verbose:
              y = f"in {end - start} second(s)"
            print(f"Decompressed {filex} files to {output} {y}")
          os.system(f"mv {os.getcwd()}/{e} {os.getcwd()}/{file}")
        if opt in ["-c","--compress"]:
          start = time.time()
          verbose = False
          if "-v" in args:
            verbose = True
            args.remove("-v")
          filex = 0
          content = {}
          files = []
          f = True
          target = arg
          try:
            name = args[0]
          except IndexError:
            name = "temp"
          for file in os.listdir(os.getcwd()):
            if os.path.isfile(f"{os.getcwd()}/{file}"):
              if target == file:
                f = False
            files.append(file)
          if target not in files:
            return print("ERROR: file/directory non-existent")
          if f == True:
            paths = filepaths(f"{os.getcwd()}/{target}")
            dirs = paths["dir"]
            direx = [target]
            for item in dirs:
              item = item.replace(f"{os.getcwd()}/","")
              direx.append(item)
            paths = paths["paths"]
            for file in paths:
              with open(f"{file}") as x:
                file = file.replace(f"{os.getcwd()}/","./")
                

                contents = x.read()
                content[file] = {}
                content[file]["content"] = contents
                content["./#dir"] = direx
                content[file]["path"] = file.replace(f"{os.getcwd()}/","")
                if verbose:
                  print(f"Compressing {file}")
                x.close()
          if f == False:
            with open(f"{os.getcwd()}/{target}") as f:
              contents = f.read()
              content[file] = contents
              if verbose:
                print(f"Compressing {file}")
              f.close()
          for item in content:
            os.system(f"touch {os.getcwd()}/{name}.json")
            with open(f"{os.getcwd()}/{name}.json","w") as x:
              json.dump(content,x,ensure_ascii=False)
            os.system(f"mv {os.getcwd()}/{name}.json {os.getcwd()}/{name}.arc")
            filex += 1
          end = time.time()
          x = ""
          if verbose:
            x = f"in {end - start} second(s)"
          print(f"Finished compressing {filex} files to {name}.arc {x}")


archiver()

