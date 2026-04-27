## For it to work you need to press play (▶️) and it will show you the menu and on the menu it will show you play, settings, leaderboard, how to play, and quit. To play press play. To find out how to play click how to play. to see your past high scores, press leaderboard. To turn of or on the music or reset your score, click on settings. to quit, press quit. 

## Setting Up Impossible Dash 

First, you create a virtual environment:

```
python3 -m venv .venv
```
This creates a .venv folder inside the project. That folder contains a separate Python environment for this project.

Next, you activate it.

On Windows PowerShell:
```
.venv\Scripts\Activate.ps1
```
If the prompt changes to include (.venv), that is evidence that the environment is active.

Then you upgrade pip:
```
python3 -m pip install --upgrade pip
```
This matters because pip is the tool that installs Python packages. Using python -m pip is clearer than just typing pip, because it makes sure the package installer belongs to the currently selected Python interpreter.

Example package install

If the project later needs a package such as requests, you would install it like this:
```
python3 -m pip install pygame3-ce