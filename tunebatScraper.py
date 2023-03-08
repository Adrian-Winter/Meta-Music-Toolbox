#MIT License
#Copyright (c) 2023 Adrian Winter

import os, time, requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from difflib import SequenceMatcher

#Values that worked well for my music library 
artistNameThresh = 0.4
trackNameThresh = 0.52
searchTresh = 0.65

RECHECKMETA = False
HYPHENSEPERATION = False

#Sets window position for the chrome driver into the bottom right corner.
WindowPositionX =1000
WindowPositionY = 1000

#dirname is the name of the folder where the tunebatScraper.py is saved
dirname = os.path.dirname(__file__)

#change the cookie folder if you have the chrome extension somewhere else...
cookieFolder = os.path.dirname(__file__)

#replace this with the path of your song folder
dirname = os.path.join(dirname, "downloads")

class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def main():
    getMetaFromTunebat(dirname,artistNameThresh,trackNameThresh,searchTresh,RECHECKMETA,HYPHENSEPERATION)

def renameTrack(base_dir,filename,artist_name,song_name,bpm,key,ext):
    old_name = base_dir+"/"+filename
    new_name =""
  
    if bpm == "" and key  == "":
        new_name= base_dir+"/"+artist_name+" - "+song_name+"."+ext
    else:
        new_name= base_dir+"/"+artist_name+" - "+song_name+ " _"+bpm+"_"+key+"."+ext
    
    os.rename(old_name, new_name)

#Gets the FolderPath  as a string input, returns a list of all wav,m4a,mp3 files
def scan_dir(base_dir: str) -> list:
    l = []
    for filepath in os.listdir(base_dir):
        fn = filepath.split("/")[-1]
        if (fn.endswith(".mp3") or fn.endswith(".wav") or fn.endswith(".m4a")):
            l.append([fn, base_dir])
    return l

#compares strings, retuns the similarity ratio
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

#Gets the file path as input, splits it into artist, song_name and fileformat 
def parse_filename(fn: str,HYPHENSEPERATION) -> str:
    if HYPHENSEPERATION:
        ext = fn.split(".")[-1]
        temp = fn.rsplit(".", 1)[0].split(" - ", 1)
        artist = temp[0]
        song_name = temp[1]
        return artist, song_name, ext
    else:
        ext = fn.split(".")[-1]
        search = fn.rsplit(".", 1)[0]
        return search, ext


#Uses selenium to open the search url and retrieve all text on the website. 
#The text is indexed so that it would only give the key and bpm of the audio file.
def getMetaFromTunebat(folderPath,artistNameThresh,trackNameThresh,searchTresh,RECHECKMETA,HYPHENSEPERATION) -> str:

    #Initializes the driver 
    url = f"https://tunebat.com/Search?q=".replace(" ", "%20")
    option_headless = webdriver.ChromeOptions()
    ex_dir = os.path.join(cookieFolder, 'I-still-don-t-care-about-cookies.crx')
    option_headless.add_extension(ex_dir)
    option_headless.add_argument("--disable-gpu")
    option_headless.add_argument('--log-level=1')
    option_headless.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=option_headless)
    driver.set_window_position(WindowPositionX,WindowPositionY)
    driver.get(url)
    
    #Connects the driver and removes ads that might interfere.
    try:
        print(f"Connecting -> {url}")
        WebDriverWait(driver, 30).until(EC.title_contains("Tunebat"))
        all_iframes = driver.find_elements(by=By.TAG_NAME, value="iframe")
        custom_ad_frames = driver.find_elements(by=By.CLASS_NAME, value="pa-unit-global")
        if len(all_iframes) > 0:
            driver.execute_script("""
                var elems = document.getElementsByTagName("iframe");
                for(var i = 0, max = elems.length; i < max; i++)
                     {
                         elems[i].hidden=true;
                     }
                                  """)
        if len(custom_ad_frames) > 0:
            driver.execute_script("""
                    var elems = document.getElementsByClassName("pa-unit-global");
                    for(var i = 0, max = elems.length; i < max; i++)
                         {
                             elems[i].hidden=true;
                         }
                                      """)
        print(f"Connected  -> {url}")
    except Exception as e:
        print(e)
        return None, None

    i = 0   #Number of skipped tracks
    j = 0   #Number of renaimed tracks
    h=0     #Number of doublechecked tracks
    tries = 1
    params_list = scan_dir(folderPath)

    for params in params_list:                  
        filename, base_dir = params

        #To doublecheck tracks that couldn´t  been found before. 
        if RECHECKMETA and filename.count("_") == 2:   
            try:
                #Removes the "NoKey, NoBPM from trackname"
                print("ReChecking: "+ filename)
                artist_name_old, song_name_old, ext = parse_filename(filename,HYPHENSEPERATION)
                song_name_old = song_name_old.split(" _")[0]
                song_name_old = song_name_old.rstrip()
                renameTrack(base_dir,filename,artist_name_old,song_name_old,"","",ext)
                filename = artist_name_old+" - "+song_name_old+"."+ext
                h+=1
                
            except:
                print("coulnt parse: "+filename)
                continue

        #skips Track if there is already meta or has been checked before
        if filename.count("_") == 2:            
            i+=1
            continue
    
        try:
           
            #fills the search  box on tunebat
            if HYPHENSEPERATION:
                artist_name_old, song_name_old, ext = parse_filename(filename,HYPHENSEPERATION)
                search = artist_name_old+" "+song_name_old
            else:
                search , ext= parse_filename(filename,HYPHENSEPERATION)
            
            search_input = driver.find_element(By.TAG_NAME, "input")
            search_input.send_keys(search)
            search_input.send_keys(Keys.RETURN)

            #Waits until search has loaded
            WebDriverWait(driver, 30).until(EC.title_contains(search))
            time.sleep(4)

            # Gets the harmonic info of the first item in the search result.
            content = driver.find_element(by=By.XPATH, value="/html/body").text
            harmonic_info = content.split("\n")[17:25]

            #Sets the bpm and key
            bpm = harmonic_info[6]
            key = harmonic_info[4]

            #Gets the online artist/Track name 
            track_name_online_new = harmonic_info[3]
            artist_name_online = harmonic_info[2]
    
            if HYPHENSEPERATION:
            #Checks if the online artist/track name are close enough to the search
                if similar(artist_name_old,artist_name_online) > artistNameThresh and similar(song_name_old,track_name_online_new) > trackNameThresh :

                    print(str(bcolors.OKGREEN)+artist_name_old+ " MATCHED! Artist Similarty is: "+str(similar(artist_name_old,artist_name_online))+" track Similarty is: "+str(similar(song_name_old,track_name_online_new))+str(bcolors.ENDC))
                    j+=1
                    renameTrack(base_dir,filename,artist_name_old,song_name_old,bpm,key,ext)

                else:
                    i+=1
                    bpm = "NoBpm"
                    key = "NoKey"
                    print(str(bcolors.FAIL)+artist_name_old+" SKIPPED! Artist Similarty is: "+str(similar(artist_name_old,artist_name_online))+" track Similarty is: "+str(similar(song_name_old,track_name_online_new))+str(bcolors.ENDC))
                    renameTrack(base_dir,filename,artist_name_old,song_name_old,bpm,key,ext)

            else: 
                onlineSearch = track_name_online_new +" " + artist_name_online
                if similar(search,onlineSearch) > searchTresh:
                    j+=1
                    print(str(bcolors.OKGREEN)+track_name_online_new+" MATCHED! Search Similarty is: "+str(similar(search,onlineSearch))+str(bcolors.ENDC))

                    artist_name_online = artist_name_online.replace(" - "," ")
                    artist_name_online = artist_name_online.replace("-"," ")
                    track_name_online_new = track_name_online_new.replace(" - "," ")
                    track_name_online_new = track_name_online_new.replace("-"," ")

                    renameTrack(base_dir,filename,artist_name_online,track_name_online_new,bpm,key,ext)
                else:
                    print(str(bcolors.FAIL)+track_name_online_new+ " SKIPPED! Search Similarty is: "+str(similar(search,onlineSearch))+str(bcolors.ENDC))
                    i+=1

        except IndexError:
            print("Make sure the trackname has the right format! : "+filename)
            i+=1
            continue
        except Exception as e :
            print(e)
            print("Exeption thrown for " +filename+"\n")
            continue
        
    print("Skipped :"+str(i)+" Tracks")
    print("Downloaded meta for :"+str(j)+" Tracks")

    driver.quit()

def press_enter_to_exit():
    input("\nPress enter to exit")
    exit()

if __name__ == "__main__":
    base_dir = "."
    main()