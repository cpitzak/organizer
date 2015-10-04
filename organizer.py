import ast
import datetime
import glob
import os
import platform
import re
import shutil
import sys
import time
import traceback
from os.path import expanduser
from distutils.file_util import move_file

class Organizer:
    
    rules = None
    timeNow = datetime.datetime.now()
    home = expanduser("~")
    
    def read_rules(self, filename):
        try:
            rulesFile = open(filename, 'r').read()
            rulesFile = rulesFile.replace('<home>', self.home)
            rulesFile = rulesFile.replace('<month-year>', str(self.timeNow.month) + "-" + str(self.timeNow.year))
            rulesFile = rulesFile.replace('<year-month>', str(self.timeNow.year) + "-" + str(self.timeNow.month))
            if (platform.system() == 'Windows'):
                rulesFile = rulesFile.replace('\\', '\\\\')
                rulesFile = rulesFile.replace('/', '\\\\')
            self.rules = ast.literal_eval(rulesFile)
        except Exception:
            print(traceback.format_exc())
            return False
        return self.validate_rules()
    
    def validate_rules(self):
        return True
    
    def clean_up(self, src, days):
        now = time.time()
        cutoff = now - (days * 86400)
        for file in glob.iglob(src):
            try:
                if not os.path.exists(file):
                    print("src for move of " + src + " doesn't exist, skipped trying to move it")
                else:
                    fileStats = os.stat(file)
                    creationTime = fileStats.st_ctime
                    if creationTime < cutoff:
                        if os.path.isdir(file):
                            shutil.rmtree(file)
                        elif os.path.isfile(file):
                            os.remove(file)
                        else:
                            print("Unknown item, not a file or dir. Skipping delete of: " + file)
                        print("deleted:" + file)
            except Exception:
                print(traceback.format_exc())
                    
    def process_delete_rules(self):
        if not 'delete' in self.rules:
            print("no delete rule")
            return False
        for rule in self.rules['delete']:
            if '<extensions.' in rule['src']:
                extensionType = re.search(r'<extensions.(.*)>', rule['src'], re.M).group(1)
                for extension in self.rules['extensions'][extensionType]:
                    src = rule['src'].replace('<extensions.' + extensionType + '>', extension)
                    self.clean_up(src, rule['days'])
                    
    def proccess_move_rules(self):
        if not 'move' in self.rules:
            print("no move rule")
            return False
        for rule in self.rules['move']:
            if '<extensions.' in rule['src']:
                extensionType = re.search(r'<extensions.(.*)>', rule['src'], re.M).group(1)
                for extension in self.rules['extensions'][extensionType]:
                    src = rule['src'].replace('<extensions.' + extensionType + '>', extension)
                    self.move_files(src, rule['dst'], extension)
            else:
                self.move_files(rule['src'], rule['dst'], extension)
    
    def move_files(self, src, dst, extension):
        for file in glob.iglob(src):
            try:
                if not os.path.exists(file):
                    print("src for move of " + file + " doesn't exist, skipped trying to move it")
                else:
                    filename = os.path.basename(file)
                    moveResult = os.path.join(dst, filename)
                    if os.path.exists(moveResult):
                        print("Skipping move of %s to %s because same name file exists there" % (file, moveResult))
                    else:
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        shutil.move(file, dst)
                        print("moved: " + file + " to: " + dst)
            except Exception:
                print(traceback.format_exc())
    
def main():
    filename = None
    defaultFile = 'rules.txt'
    usage = """usage: python organizer.py [rules_file]
                    rules_file (optional) - the file with the rules. If not specified then will
                    attempt to be read %s at the same location as organizer.py 
            """ % defaultFile
    if len(sys.argv) == 1:
        if not os.path.isfile(defaultFile):
            print("Failed to read %s" % defaultFile)
            print(usage)
        else:
            filename = defaultFile
    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            print("Failed to read %s" % sys.argv[1])
        else:
            filename = sys.argv[1]
    else:
        print(usage)
        
    if filename:
        organizer = Organizer()
        if (organizer.read_rules(filename)):
            organizer.proccess_move_rules()
            organizer.process_delete_rules()
            print("completed")
        else:
            print("Malformed rules in %s, program exited." % filename)
    else:
        print("No file read, exited program")

if __name__ == "__main__":
    main()
