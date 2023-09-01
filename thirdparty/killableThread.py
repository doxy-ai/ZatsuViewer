#---------------------------------------------------------------------
# KThread.py: A killable Thread implementation.
# From: https://web.archive.org/web/20130503082442/http://mail.python.org/pipermail/python-list/2004-May/281943.html
#---------------------------------------------------------------------

import sys
import trace
import threading

class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill()
method."""
  def __init__(self, *args, **keywords):
    for key in keywords.keys():
        if(key == "target"):
            self.target = keywords["target"]
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run      # Force the Thread to install our trace.
    threading.Thread.start(self)

  def __run(self):
    """Hacked run function, which installs the trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        print("thread stopped")
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True