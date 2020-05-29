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


class Organizer:
    rules = None
    timeNow = datetime.datetime.now()
    home = expanduser("~")

    def read_rules(self, filename):
        try:
            rules_file = open(filename, 'r').read()
            rules_file = rules_file.replace('<home>', self.home)
            rules_file = rules_file.replace('<month-year>', str(self.timeNow.month) + "-" + str(self.timeNow.year))
            rules_file = rules_file.replace('<year-month>', str(self.timeNow.year) + "-" + str(self.timeNow.month))
            if platform.system() == 'Windows':
                rules_file = rules_file.replace('\\', '\\\\')
                rules_file = rules_file.replace('/', '\\\\')
            self.rules = ast.literal_eval(rules_file)
        except Exception:
            print(traceback.format_exc())
            return False
        return True

    def clean_up(self, src, days):
        now = time.time()
        cutoff = now - (days * 86400)
        for file in glob.iglob(src):
            try:
                if not os.path.exists(file):
                    print("src for move of " + src + " doesn't exist, skipped trying to move it")
                else:
                    file_stats = os.stat(file)
                    creation_time = file_stats.st_ctime
                    if creation_time < cutoff:
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
        if 'delete' not in self.rules:
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
                    move_result = os.path.join(dst, filename)
                    if os.path.exists(move_result):
                        print("Skipping move of %s to %s because same name file exists there" % (file, move_result))
                    else:
                        if not os.path.exists(dst):
                            os.makedirs(dst)
                        shutil.move(file, dst)
                        print("moved: " + file + " to: " + dst)
            except Exception:
                print(traceback.format_exc())


def main():
    filename = None
    default_file = 'rules.json'
    usage = """usage: python organizer.py [rules_file]
                    rules_file (optional) - the file with the rules. If not specified then will
                    attempt to be read %s at the same location as organizer.py 
            """ % default_file
    if len(sys.argv) == 1:
        if not os.path.isfile(default_file):
            print("Failed to read %s" % default_file)
            print(usage)
        else:
            filename = default_file
    elif len(sys.argv) == 2:
        if not os.path.isfile(sys.argv[1]):
            print("Failed to read %s" % sys.argv[1])
        else:
            filename = sys.argv[1]
    else:
        print(usage)

    if filename:
        organizer = Organizer()
        if organizer.read_rules(filename):
            organizer.proccess_move_rules()
            organizer.process_delete_rules()
            print("completed")
        else:
            print("Malformed rules in %s, program exited." % filename)
    else:
        print("No file read, exited program")


if __name__ == "__main__":
    main()
