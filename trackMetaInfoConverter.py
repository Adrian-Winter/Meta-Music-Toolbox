#MIT License
#Copyright (c) 2023 Adrian Winter

import tunebatScraper as tbs
import music_tag

def addMetaToTracksAccordingToName(folderPath):
    params_list = tbs.scan_dir(folderPath)
    i = 0
    j = 0 
    for params in params_list:               
        filename, base_dir = params
        old_name = base_dir+"/"+filename
        
        try:
            audiofile = music_tag.load_file(old_name)
            print(filename)
            artist_name_old, song_name_old, ext = tbs.parse_filename(filename,True)
            
            audiofile["artist"] = artist_name_old
            audiofile["title"] = song_name_old
            audiofile.save()
            i+=1
        except:
            print("couldnt add meta for: "+filename)
            j+=1
            continue
        
            
    print("Added Meta to  "+str(i) +" Tracks")
    print("skipped "+str(j) +" Tracks")

def renameTracksinFolderAccordingToMeta(folderPath):
    params_list = tbs.scan_dir(folderPath)
    i=0
    j=0
    for params in params_list:               
        filename, base_dir = params
        audiofile = None 
        try: 
            old_name = base_dir+"/"+filename
            audiofile = music_tag.load_file(old_name)
        except:
            j+=1
            continue
        try: 
            artist_name = str(audiofile['artist'])
            song_name = str(audiofile["title"])


           
            if artist_name == "" or song_name == "":
                j+=1 
                continue

            ext = filename.split(".")[-1]
            tbs.renameTrack(base_dir,filename,artist_name,song_name,"","",ext)
            i+=1

        except: 
            #print("Skipped: "+filename)
            j+=1
            continue

    print("Renaimed "+str(i) +" Tracks")
    print("skipped "+str(j) +" Tracks")