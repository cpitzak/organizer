# Organizer
A utility I made to organizes my files and removes old files. I have this utility automatically run when the computer starts up.

Tested on Windows 7 and Mac OSX.

## Files
  * organizer.py - this is the main file that performs the organization.
  * rules.txt - this contain the rules for moving or deleting files.  keywords in the file: move, delete, \<extensions.\>, extensions, src, dst, \<home\>, \<year-month\>, \<month-year\>
  
```
	usage: python organizer.py [rules_file]
           
           rules_file - the file with the rules. If not specified then will
           attempt to be read rules.txt at the same location as organizer.py
```

## Keywords
  * \<home\> - will be turned into the location of the home directory of the user running this program
  * \<year-month\> or \<month-year\> - will be turned into the current month and year
  * src - location of source
  * dst - lcoation of destination
  * \<extensions.foo\> - will look for the "foo" array in the extensions map
  * extensions - a map that as values has arrays of extensions. You can make any array of extension you want and reference as \<extensions.myNewArray\>
  * delete - an array of maps to the src to delete after days old
  * days - number of days
  * move - an array of maps to the src and dst of what to move
