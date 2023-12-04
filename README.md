# Colored Conway's Game of Life
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
* rollback time  
* do something else

## Now about the controls
| control                           | action                                                            |
|-----------------------------------|-------------------------------------------------------------------|
| LMB                               | add/remove a living cell                                          |  
| LMB (holding)                     | draw a line of living ones                                        |  
| RMB (holding)                     | movement across the field                                         |
| Scrolling the mouse wheel         | increase/decrease the field                                       |  
| Space or button on the top left   | start/pause Conway's game                                         |  
| Left/right arrow                  | slow down/speed up the game twice                                 |  
| P or MMB                          | switch pattern mode                                               |
| Upper/lower arrow                 | switch between patterns                                           |
| R                                 | rotate the pattern 90 degrees clockwise                           | 
| E or button on the top right      | toggle eraser mode on/off                                         |
| 1, 2, 3, 4, 5, 0                  | drawing colors (0 is fake: i.e. does not participate in the game) |
| K / CTRL+K                        | clear living / fake cells                                         |
| I or button on the top right      | inventory with your patterns (the last one opened is used)        |
| CTRL+S or button on the top right | save the field and patterns                                       | 
| CTRL+Z                            | rollback to the last save                                         |
| V, B                              | time travel (note: only current state can be saved)               |  
| H                                 | change the hiding mode of icons (only in the field)               |  
| ESC                               | exit the current window (in the field: exit the application)      |
## Notes
Just saying that the \_\_parameters\_\_ file is a save file, it is created and then overwritten every time you save.

### Windows
You can download the executable file from Releases.

### All platforms
You need to install [Python](https://www.python.org/downloads/). After that open terminal / cmd / PowerShell.

Create and activate virtual environment: 

* macOS / Linux:
```bash
python3 -m venv venv
```

```bash
source venv/bin/activate
```

* Windows:
```bash
python -m venv venv
```

```bash
venv\Scripts\activate.ps1 # for all platforms from PS
```

```bash
venv\Scripts\activate.bat # for Windows from cmd
```

Install necessary libraries:
```bash
pip install pygame screeninfo
```

Now you can run main.py and enjoy the game:
```bash
python main.py
```

If you want to build .exe yourself:
```bash
pip install pyinstaller
```

```bash
python -m PyInstaller main.spec
```

When you're done, you can deactivate the virtual environment:
```bash
deactivate
```

### Attributions
Many thanks to https://purepng.com/ and https://iconduck.com/licenses/cc0 for [CC0-licensed](https://creativecommons.org/publicdomain/zero/1.0/) PNGs (both) and [Phosphor Icons](https://phosphoricons.com/) for [MIT-licensed](https://opensource.org/license/mit/) icons (in my repo it resources/eraser.png). 

