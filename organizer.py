import ast
import datetime
import glob
import os
import re
import shutil
import time
import traceback
from os.path import expanduser
from __builtin__ import True
from distutils.file_util import move_file

class Organizer:
    
    rules = None
    time_now = datetime.datetime.now()
    home = expanduser("~")
    
    def read_rules(self):
        try:
            rules_file = open('rules.txt', 'r').read()
            rules_file = rules_file.replace('<home>', self.home)
            rules_file = rules_file.replace('<month-year>', str(self.time_now.month) + "-" + str(self.time_now.year))
            rules_file = rules_file.replace('<year-month>', str(self.time_now.year) + "-" + str(self.time_now.month))
            self.rules = ast.literal_eval(rules_file)
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
                extension_type = re.search(r'<extensions.(.*)>', rule['src'], re.M).group(1)
                for extension in self.rules['extensions'][extension_type]:
                    src = rule['src'].replace('<extensions.' + extension_type + '>', extension)
                    self.clean_up(src, rule['days'])
                    
    def proccess_move_rules(self):
        if not 'move' in self.rules:
            print("no move rule")
            return False
        for rule in self.rules['move']:
            if '<extensions.' in rule['src']:
                extension_type = re.search(r'<extensions.(.*)>', rule['src'], re.M).group(1)
                for extension in self.rules['extensions'][extension_type]:
                    src = rule['src'].replace('<extensions.' + extension_type + '>', extension)
                    if not os.path.exists(rule['dst']):
                        os.makedirs(rule['dst'])
                    self.move_files(src, rule['dst'], extension)
    
    def move_files(self, src, dst, extension):
        for file in glob.iglob(src):
            try:
                if not os.path.exists(file):
                    print("src for move of " + src + " doesn't exist, skipped trying to move it")
                else:
                    shutil.move(file, dst)
                    print("moved:" + file + ", to: " + dst)
            except Exception:
                print(traceback.format_exc())
    
def main():
    organizer = Organizer()
    if (organizer.read_rules()):
        organizer.proccess_move_rules()
        organizer.process_delete_rules()
    else:
        print("Failed to read rules.txt, program exited.")

if __name__ == "__main__":
    main()
