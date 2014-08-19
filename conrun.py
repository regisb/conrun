#! /usr/bin/env python
import subprocess, time, argparse, os.path

def run_command(command):
  error = False
  try:
    # Launch command
    result = subprocess.Popen(command , shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result.wait()
  except KeyboardInterrupt:
    exit()
  except:
    error = True

  # Clear screen
  subprocess.Popen("clear").wait()

  # Print result
  (out, err) = result.communicate()
  print out
  print err
  print time.strftime("%c", time.localtime()),
  if error:
    print " --------------------------------- ERROR"
  else:
    print " +++++++++++++++++++++++++++++++++ OK"

def wait_for_file_change(file_path, last_modification):
  while True:
    t = None
    try:
      t = os.path.getmtime(file_path)
    except OSError:
      continue
    if t is not None and t != last_modification:
      return t

if __name__ == "__main__":

  # Argument parsing
  parser = argparse.ArgumentParser(description='Execute a command continuously. Type Ctrl-c to interrupt')
  parser.add_argument("-f", "--file", help="File to watch")
  parser.add_argument("command", help="The command to execute")
  args = parser.parse_args()

  # Should we watch file changes?
  last_modification = None
  file_path = None
  if args.file is not None:
    file_path = os.path.abspath(args.file)
    if not os.path.exists(file_path):
      raise Exception("File %s does not exist" % file_path)

  while True:
    if file_path is not None:
      last_modification = wait_for_file_change(file_path, last_modification)
    run_command(args.command)
    time.sleep(1)
