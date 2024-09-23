# Conway's Game of Life
Cross-platform implementation of this game in Python in which you can
* create and run any game configuration
* move around the field
* start/pause the game
* save the current field as a snapshot
* create a custom brush pattern and draw with it (also you can save your patterns)
* change
  * color of brush (different colors are mixed during the game)
  * the scale
  * game speed
* roll back time  
* do something else

## Now about the controls
| control | action |
| --- | --- |
| LMB | add/remove a living cell |  
| LMB (holding) | draw a line of living ones |  
| RMB (holding) | movement across the field |
| Scrolling the mouse wheel | increase/decrease the field |  
| Spacebar | start/pause Conway's game |  
| Left/right arrow | slow down/speed up the game twice |  
| P or MMB | toggle pattern mode on/off |
| Upper/lower arrow | switch between patterns |
| R | rotate the pattern 90 degrees clockwise | 
| E or button on the top right | toggle eraser mode on/off |  
| G | toggle grid mode on/off | 
| 1, 2, 3, 4, 5, 0 | drawing colors (0 is false: i.e. does not participate in the game) |
| K , CTRL+K | clear living / false cells |
| I or button on the top right | inventory with your patterns (the last one opened is used) |
| CTRL+S or button on the top right | save the field and patterns | 
| CTRL+Z | roll back to the last save |
| V, B | time travel (note: it's not saved) |  
| H | change the hiding mode of icons (in the field) |  
| ESC | exit the current window (in the field: exit the application) |
### Notes
Windows: you can download the executable file from Releases.

All platforms:  
Install the necessary libraries by this commands:
```bash
pip3 install pygame
```
```bash
pip3 install pypiwin32  #only for Windows
```
After this you can run main.py and enjoy the game:
```bash
python3 main.py
```

Also you can create the executable file by following commands:
```bash
pip3 install pyinstaller==4.10
```
```bash
python3 -m PyInstaller -F main.spec
```


Just saying that the \_\_parameters\_\_ file is a save file, it is created and then overwritten every time you save.
