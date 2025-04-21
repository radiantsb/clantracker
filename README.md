to setup clan tracker:
edit line 6 by putting your clan name in the quotation marks
edit line 7 by putting your roblox userid (not username) after 'userid =' (but before the #)
optionally edit line 8, if set to true it will create 2 text files that track your score and the clan score over time

if you want a .exe file:
make sure you have python installed
open a command prompt window and run: pip install pyinstaller
copy the file path of the .py file you edited
open command prompt and run: pyinstaller "path of file" --noconsole --onefile
exe file will be saved to c://users/you/dist
