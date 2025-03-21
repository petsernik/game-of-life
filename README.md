# Colored Conway's Game of Life
Cross-platform implementation of this game in Python in which you can
* create and run any game configuration
* move around the field
* start/pause the game
* save the current field as a snapshot
* create a custom brush pattern and draw with it (also you can save your patterns)
* create a brush pattern by PNG image
* change
  * color of brush (different colors are mixed during the game)
  * the scale
  * game speed
* rollback time  
* do something else

## Now about the controls
| control                           | action                                                                                      |
|-----------------------------------|---------------------------------------------------------------------------------------------|
| F1                                | get description of Game of Life and these controls  <br> (you can scroll it by mouse wheel) |  
| LMB                               | add/remove a living cell                                                                    |  
| LMB (holding)                     | draw a line of living ones                                                                  |  
| RMB (holding)                     | movement across the field                                                                   |
| Scrolling the mouse wheel         | increase/decrease the field                                                                 |  
| Space or button on the top left   | start/pause Conway's game                                                                   |  
| Left/right arrow                  | slow down/speed up the game twice                                                           |  
| P or MMB                          | switch pattern mode <br> (point/pattern/art mode)                                           |
| Upper/lower arrow                 | switch between patterns                                                                     |
| R                                 | rotate the pattern 90 degrees clockwise                                                     | 
| E or button on the top right      | toggle eraser mode on/off                                                                   |
| G                                 | toggle grid mode on/off                                                                     |
| T                                 | toggle transparent mode on/off                                                              |
| 1, 2, 3, 4, 5, 0                  | drawing colors <br> (0 is fake: i.e. does not participate in the game)                      |
| K / CTRL+K                        | clear living / fake cells                                                                   |
| I or button on the top right      | inventory with your patterns (the last one opened is used)                                  |
| CTRL+S or button on the top right | save the field and patterns                                                                 | 
| CTRL+Z                            | rollback to the last save                                                                   |
| V, B                              | time travel <br> (note: only current state can be saved)                                    |  
| H                                 | change the hiding mode of icons <br> (only in the field)                                    |  
| ESC                               | exit the current window <br> (in the field: exit the application)                           |
## Notes
Just saying that the \_\_parameters\_\_ file is a save file, it is created and then overwritten every time you save.  

You can add/remove PNG images from the gallery folder to update arts (if the width or height of the PNG 
is greater than ~50 pixels, the image will be reduced).

### Windows
You can download the executable file from Releases.

### All platforms
Download this repository (with `git clone` or directly from GitHub). Also, you need to install [Python](https://www.python.org/downloads/) and (optional) [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/). After that open terminal / cmd / PowerShell.

Create and activate virtual environment: 

* macOS / Linux:
```bash
python3 -m venv .venv
```

```bash
source .venv/bin/activate
```

* Windows:
```bash
python -m venv .venv
```

```bash
.venv\Scripts\activate.bat # for Windows from cmd
```

```bash
.venv\Scripts\activate.ps1 # for all platforms from PS
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
Many thanks to: 
* [Purepng](https://purepng.com/) and [iconduck](https://iconduck.com/licenses/cc0) for 
[CC0-licensed](https://creativecommons.org/publicdomain/zero/1.0/) PNGs.
* [Phosphor Icons](https://phosphoricons.com/) for [MIT-licensed](https://opensource.org/license/mit/) icons 
(in my repo it resources/eraser.png). 

