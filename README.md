# AudioToJummbox

Converts audio files into collections of notes and outputs them in Jummbox format.  

## Installation

It is recommended to use [Anaconda](https://www.anaconda.com/products/individual) for this process.  It will make the installation a lot easier.  

Step 1: Clone the repository with `git clone https://github.com/KeeyanGhoreshi/AudioToJummbox.git`

Step 2: Navigate to the `AudioToJummbox` directory and run `python ./setup.py install`

You may need to install librosa using a package manager like pip, if you are not using anaconda you may need to install some other packages.  

## Usage

You can run the app on the command line with `audioToJummbox [args]`

The command takes the following command line arguments:

`infile` - required - The audio file to be processed and converted into jummbox notes.

`--base -b` - not required - The program only outputs the notes.  The rest of the song structure is defined by the "base" file, or a template jummbox json.  This file defines the instruments and other qualities.  This file defaults to `./resources/template.json`

You can change the base file if you want the program to output to have different instruments.  For example, if you would like all the instruments to have max filter cut, instead of min, you can change that in jummbox, output the json file, and replace the template file with your new one.

The following things are requirements that you cannot change:
    - There needs to be 24 pitch channels
    - There needs to be 8 mod channels
    - The rhythm  needs to be set to "freehand"

`--output -o` - not required - The output file.  Will default to `./resources/data.json`.  This is the file you import into jummbox.  When the program finishes running, this file will be updated with the notes.

`--tempo -t` - not required - This is the tempo that jummbox needs to be set to in order for the playback to sound correct.  If your jummbox song is set to 150 tempo, set this flag to 150.  This flag defaults to 200.  

`--smooth -s` - not implemented yet

Example command:
`audioToJummbox ./sound/test.wav --tempo 200`