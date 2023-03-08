# Meta-Music-Toolbox
## A collection of handy tools such as adding Key & BPM to your music library! 🎵

### EXAMPLE:
### Renaming tracks according to current meta and then web scraping the KEY and BPM from tubebat.com .🔥 

![alt text](https://github.com/Adrian-Winter/Meta-Music-Toolbox/blob/main/MusicToolBoxShowcase.gif)

## What can this application do? 👀
### This toolbox has currently the following functions:

* Web scraping __Key__ and __BPM__ from tunebat.com 
* Adding batch tags according to the filename (ID3v1, ID3v2.3, ID3v2.4)
* renaming the file according to the batch tag

## Why did I create this Toolbox? 🎹
I created this toolbox to help me sort my music library and add valuable information for DJing. I can imagine, most people are not interested in knowing the BPM and key of the track they are listening to, but for making smooth music mixes this is essential. Some music vendors such as beatport.com offer this metadata and some DJ software have algorithms to detect the key and BPM of a track. However in my case I didn’t want to rely on these services as I wanted to build my own DJ setup in M4L for Ableton (which I will upload soon...). ☺️


## What is web scraping? 🧐
Web scraping is the process of collecting data from websites automatically using software tools. It's commonly used for market research, content aggregation, lead generation, and data analysis. However, it can be a sensitive activity legally and ethically, so it's important to be careful when scraping websites. In this application web scraping is used to gather metadata such as Key and BPM from the database used for the website tunebat.com. 

![alt text](https://github.com/Adrian-Winter/Meta-Music-Toolbox/blob/main/tunebat%20database.png)

## Requirements 🔄
### In order to use this script you need:

* Google Chrome
* The addon ___I_dont_care_about_cookies___ (included in the repo) 
* Packages: Selenium, requests, music_tag


## How to use this application? ⚙️

1. Run the __metaMusicToolboxGUI.py__.
2. Select the folder with your tracks by clicking the __"Select Directory"__ Button.
3. If your files are in the format __artist - track.mp3__ click on the __Hyphen Separation__ checkbox.
4. Now you can click: 

    * __Scrape Tunebat__, which will rename your tracks to the format: __artist - trackname_BPM_Key.mp3__
    * __Meta to trackname__, which will read the current meta files of your tracks, and renaim the files to __artist - track.mp3__
    * __Trackname to meta__ , which write the current artist- and trackname to the meta file. 

Both the __Meta to trackname__ and __Trackname to Meta__ functions are implemented to prepare your library for the __Scrape Tunebat__ process. For example if you have a CD the usual filename is: __tracknumber - trackname.mp3__, but has the right meta. By applying __Meta to trackname__ you end up with a file named __artist - trackname.mp3__ which then can be used by the __Scrape Tunebat__ function.

### Parameters 

When you check the __recheck Meta__ checkbox, tracks that already have a key and BPM in their trackname will not be skipped, but overwritten by the tunebat database. 

If you check the __Hypen separation__ checkbox, it is assumed your filename has the format __artist - trackname.mp3__. If not, the whole current filename will used for the search on tunebat.com.

Using the __sliders__ you can decide how close the match of your filename and the database of tunebat.com needs to be in order to be used. When Checking the __hypen separation__ button, it is assumed your filename is in the format __artist - trackname.mp3__ and therefore you can set thresholds for the artist match and trackname match individually. For my library an __artist  name thresh = 0.4 and track name thresh = 0.52__ worked very well. 

If you don’t have your filenames in the format __artist - trackname.mp3__  you can simply uncheck the __Hypen separation__ checkbox and select a search accuracy of the whole filename compared to the artist+trackname of the tunebat.com database




## Feedback 
* Please feel free to let me know if you have trouble getting the results you are looking for. 
* Also what features could be added? 

### Hope this little app made your project a little bit easier! ☺️



