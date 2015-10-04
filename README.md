# Organizer
A simple utility I made to organizes my files and removes old files. I have this utility automatically run when the computer starts up.

Tested on Windows 7 and Mac OSX.

## Files
  * organizer.py - this is the main file that performs the organization.
  * rules.txt - this contain the rules for moving or deleting files.  keywords in the file: move, delete, \<extensions.\>, extensions, src, dst, \<home\>, \<year-month\>, \<month-year\>
  
```
	usage: python organizer.py [rules_file]
                  rules_file (optional) - the file with the rules. If not specified then %s
                                          will attempt to be read at the same location as organizer.py
```