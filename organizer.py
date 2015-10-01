import datetime
import glob
import os
import shutil
import time
import traceback
from os.path import expanduser

class Organizer:
    
    def clean_up(self, src, days):
        now = time.time()
        cutoff = now - (days * 86400)
        
        extensions = [".exe", ".zip", ".msi", ".torrent", ".jar", ".tar.gz", ".dmg"]
        
        files = os.listdir(src)
        for xfile in files:
            full_path = os.path.join(src, xfile)
            if os.path.isfile(full_path):
                t = os.stat(full_path)
                c = t.st_ctime
    
                # delete file if older than days
                if c < cutoff and any(x in xfile for x in extensions):
                    os.remove(full_path)
    
    def move_files(self, src, dst, extension):
        for file in glob.iglob(os.path.join(src, "*." + extension)):
            try:
                shutil.move(file, dst)
            except Exception:
                print(traceback.format_exc())
    
    def organize_pictures(self, dstDir, srcDir):
        if os.path.exists(dstDir) and os.path.exists(dstDir):
            now = datetime.datetime.now()
            newDstDir = os.path.join(dstDir, "desktop", str(now.year) + "-" + str(now.month))
            if not os.path.exists(newDstDir):
                os.makedirs(newDstDir)
            self.move_files(srcDir, newDstDir, "jpg")
            self.move_files(srcDir, newDstDir, "png")
            self.move_files(srcDir, newDstDir, "gif")
            self.move_files(srcDir, newDstDir, "tif")
        else:
            print("directories don't exist")
            
    def organize_documents(self, dstDir, srcDir):
        if os.path.exists(dstDir) and os.path.exists(dstDir):
            now = datetime.datetime.now()
            newDstDir = os.path.join(dstDir, "desktop", str(now.year) + "-" + str(now.month))
            if not os.path.exists(newDstDir):
                os.makedirs(newDstDir)
            self.move_files(srcDir, newDstDir, "txt")
            self.move_files(srcDir, newDstDir, "doc")
            self.move_files(srcDir, newDstDir, "docx")
            self.move_files(srcDir, newDstDir, "pdf")
            self.move_files(srcDir, newDstDir, "ppt")
            self.move_files(srcDir, newDstDir, "pptx")
            self.move_files(srcDir, newDstDir, "xls")
            self.move_files(srcDir, newDstDir, "xlsx")
        else:
            print("directories don't exist")
    
def main():
    organizer = Organizer()
    home = expanduser("~")
    picturesDir = os.path.join(home, "Pictures")
    documentsDir = os.path.join(home, "Documents")
    downloadsDir = os.path.join(home, "Downloads")
    desktopDir = os.path.join(home, "Desktop")
    organizer.organize_pictures(picturesDir, desktopDir)
    organizer.organize_documents(documentsDir, desktopDir)
    organizer.clean_up(downloadsDir, 7)

if __name__ == "__main__":
    main()
