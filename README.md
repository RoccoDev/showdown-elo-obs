# Pokemon Showdown ELO plugin for OBS

## Installation
If you're on Windows you can follow [this video guide](https://www.youtube.com/watch?v=Jmgo9VBwNA8).

* First, download the plugin from [here](https://raw.githubusercontent.com/RoccoDev/showdown-elo-obs/master/showdown_elo.py).
* If you are on Linux or macOS, skip this step.
    * If you are on **Windows**, you have to install Python 3.6 first.
    * If your OBS is 64-bit, install [this](https://www.python.org/ftp/python/3.6.8/python-3.6.8-amd64.exe).
    * If your OBS is 32-bit, install [this](https://www.python.org/ftp/python/3.6.8/python-3.6.8.exe).
* Once you have downloaded the `showdown_elo.py` file, open OBS.
* Navigate to Tools > Scripts.
* If you're on **Windows**, do the following:
    * Open the "Python settings" tab.
    * Click "Browse..."
    * Type `%appdata%` in the address bar and press Enter.
    * You should be in the `Roaming` folder. Go up one level and open `Local`.
    * Navigate to `Programs\Python\Python36` and click "Select folder".
    * Now go back to the Scripts tab.
* Click the "+" button in the bottom left corner.
* Choose the `showdown_elo.py` file you've downloaded.
* Configure the plugin as you'd like.
    * Showdown username: the player to get the stats of.
    * Update interval: how often the statistics should update, in seconds (5 is recommended).
    * Text source: the OBS text source that the plugin will attempt to write statistics to.
        * You can add a text source to any scene, just like a normal video source.
        * If your text source isn't recognized by the plugin, restart OBS.
    * Format: the Showdown format identifier, for example `gen8ou`, `gen7randombattle`, `gen5uu` etc.
    * Text format: how the text should be displayed, see the section below.
* To apply the changes, click the refresh button next to the "+" and "-" buttons in the bottom left corner.

## Troubleshooting
* Text source isn't recognized in the settings: restart OBS.
* Text source isn't updating: hide it and show it (using the eye button).

## Text format
You can configure how the plugin displays the statistics.

By default, this is set to `{user}: {elo}`, but there are more options available. Here's a list:

To jump to the next line, you can use `\n` (newline).

#### user
The player's username.  
`{user}` = `Gen 8 Memes`

#### elo
The player's ELO, with two decimal digits.  
`{elo}` = `1000.00`

#### elo_int
The player's ELO, with no decimal digits.  
`{elo_int}` = `1000`

#### gxe
The player's GXE.  
`{gxe}` = `90.0%`

#### w
The player's victories.  
`{w}` = `290`

#### l (lowercase L)
The player's losses.  
`{l}` = `100`

#### t
The player's ties.  
`{t}` = `0`

#### g
The player's total number of games played.  
`{g}` = `390`

### Examples
* `{user}: {elo_int} ELO, {gxe} GXE` = `Gen 8 Memes: 1200 ELO, 61.4% GXE`
* `Suspect requirements\n {gxe}/80% GXE\n {g}/40 games` becomes:
```
Suspect requirements
61.4%/80% GXE
35/40 games
```

## Need help?
Reach out to me via email (hey(at)rocco.dev) or Discord (RoccoDev#2699).

## License
MIT
