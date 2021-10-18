# AudioToJummbox

Converts audio files into collections of notes and outputs them in [Jummbox](https://github.com/jummbus/jummbox) format.  

## Installation

It is recommended to use [Anaconda](https://www.anaconda.com/products/individual) for this process.  It will make the installation a lot easier.  

Step 1: Clone the repository with `git clone https://github.com/KeeyanGhoreshi/AudioToJummbox.git`

Step 2: Navigate to the root directory and run `python ./setup.py install`

You may need to install librosa using a package manager like pip, if you are not using anaconda you may need to install some other packages.  

## Usage

Navigate to the root directory of the project. You can run the app on the command line with 

`> audioToJummbox [args]`

The command takes the following command line arguments:

`infile` - **required** - The audio file to be processed and converted into jummbox notes.

`--base -b` - **not required** - The program only outputs the notes.  The rest of the song structure is defined by the "base" file, or a template jummbox json.  This file defines the instruments and other qualities.  This file defaults to `./resources/template.json`

You can change the base file if you want the program to output to have different instruments.  For example, if you would like all the instruments to have max filter cut, instead of min, you can change that in jummbox, output the json file, and replace the template file with your new one.

The following things are requirements that you cannot change:

    - There needs to be 24 pitch channels, 18 low pitch (1x frequency FM) and 6 high pitch (6x frequency FM)
    
    - There needs to be 8 mod channels
    
    - The rhythm  needs to be set to "freehand"

`--output -o` - **not required** - The output file.  Will default to `./resources/data.json`.  This is the file you import into jummbox.  When the program finishes running, this file will be updated with the notes.

`--tempo -t` - **not required** - This is the tempo that jummbox needs to be set to in order for the playback to sound correct.  If your jummbox song is set to 150 tempo, set this flag to 150.  This flag defaults to 200.  

`--smooth -s` - **not implemented yet**

Example command:

`> audioToJummbox ./sound/test.wav --tempo 200`

## Notes 

When converting audio, you will get the best results using clear, simple samples.  Noisy signals get amplified by the program and become difficult to understand.  When setting the tempo, you are also setting the size of each frame.  High tempos have lower frequency resolution, and might sound incorrect.  But they play more samples per second, so the sound is less compressed.  Low tempos have higher frequency resolution and are more accurate to the original signal, but are more compressed.  It's a tradeoff.  You may want to write a song at 200BPM, but have the audio converted at 100BPM.  You can halve the tempo of the song to 100BPM and make the notes half as long to simulate 200BPM in order to make the audio compatible.  

The filter cut of each instrument is at a minimum by defualt, to cut down on the "crackling" artifacts.  The audio sounds clearer with max filter cut, but it will introduce harsh crackling noises due to jummbox's limitations.

## Known Issues

- The program assumes a single channel of audio, it will fail if the audio is stereo and there are two channels.
- The base file included in the project only goes up to 8 patterns.  If you try to convert a long audio file, the program will fail, it will not add additional patterns for more notes.  You can easily adjust this by changing the base/template file out with one that has more patterns enabled per channel.   
- The audio will crackle a bit in Jummbox due to the large, rapid volume changes 
