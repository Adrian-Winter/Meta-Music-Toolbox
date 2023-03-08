#MIT License
#Copyright (c) 2023 Adrian Winter

import tkinter as tk
from tkinter import filedialog
import tunebatScraper as tbs
import trackMetaInfoConverter as tmic

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meta Music Toolbox")
        self.geometry("400x400")

        # Create checkboxes
        self.meta_check = tk.BooleanVar(value=False)
        self.meta_checkbox = tk.Checkbutton(self, text="Recheck Meta", variable=self.meta_check)
        self.meta_checkbox.pack()

        self.hypen_check = tk.BooleanVar(value=False)
        self.hypen_checkbox = tk.Checkbutton(self, text="Hyphen Separation", variable=self.hypen_check, command=self.update_sliders)
        self.hypen_checkbox.pack()

        # Create sliders
        self.artist_slider_var = tk.DoubleVar(value=0.4)
        self.artist_slider_label = tk.Label(self, text="Artist Name Thresh")
        self.artist_slider = tk.Scale(self, variable=self.artist_slider_var, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)

        self.track_slider_var = tk.DoubleVar(value=0.52)
        self.track_slider_label = tk.Label(self, text="Track Name Thresh")
        self.track_slider = tk.Scale(self, variable=self.track_slider_var, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)

        self.search_slider_var = tk.DoubleVar(value=0.65)
        self.search_slider_label = tk.Label(self, text="Search Thresh")
        self.search_slider = tk.Scale(self, variable=self.search_slider_var, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200)

        # Create button to select directory
        self.dirname = tk.StringVar()
        self.select_button = tk.Button(self, text="Select Directory", command=self.select_directory)
        self.select_button.pack()

        # Create directory display textbox
        self.directory_label = tk.Label(self, text="Selected Directory: ")
        self.directory_label.pack()
        self.directory_textbox = tk.Text(self, height=1, width=40)
        self.directory_textbox.pack()

        # Initialize directory name variable
        self.dirname = ""

        # Create buttons for meta/track conversion to start scraping
        self.tracktometa_button = tk.Button(self, text="Trackname to Meta", command=self.addMetaToTracksAccordingToName)
        self.tracktometa_button.pack(pady=10,side = tk.BOTTOM)

        self.metatotrack_button = tk.Button(self, text="Meta to Trackname", command=self.renameTracksinFolderAccordingToMeta)
        self.metatotrack_button.pack(pady=10,side = tk.BOTTOM)

        # Create button to start scraping
        self.scrape_button = tk.Button(self, text="Scrape Tunebat", command=self.start_scraping)
        self.scrape_button.pack(pady=10)

   
        # Initially hide the artist and track sliders
        self.search_slider_label.pack()
        self.search_slider.pack()
        self.artist_slider_label.pack_forget()
        self.artist_slider.pack_forget()
        self.track_slider_label.pack_forget()
        self.track_slider.pack_forget()

    def update_sliders(self):
        # If hyphen checkbox is checked, show the artist and track sliders, else hide them and show only the search slider
        if self.hypen_check.get():
            self.artist_slider_label.pack()
            self.artist_slider.pack()
            self.track_slider_label.pack()
            self.track_slider.pack()
            self.search_slider_label.pack_forget()
            self.search_slider.pack_forget()
        else:
            self.artist_slider_label.pack_forget()
            self.artist_slider.pack_forget()
            self.track_slider_label.pack_forget()
            self.track_slider.pack_forget()
            self.search_slider_label.pack()
            self.search_slider.pack()
    
    
    def select_directory(self):
        self.dirname = filedialog.askdirectory()
        self.directory_textbox.delete(1.0, tk.END)
        self.directory_textbox.insert(tk.END, self.dirname)

    def addMetaToTracksAccordingToName(self):
        directory = self.dirname
        tmic.addMetaToTracksAccordingToName(directory)

    def renameTracksinFolderAccordingToMeta(self):
        directory = self.dirname
        tmic.renameTracksinFolderAccordingToMeta(directory)

    def start_scraping(self):
        # Get the current values of the checkboxes and sliders
        meta = self.meta_check.get()
        hypen = self.hypen_check.get()
        artist_thresh = self.artist_slider_var.get()
        track_thresh = self.track_slider_var.get()
        search_thresh = self.search_slider_var.get()
        directory = self.dirname

        
        # TODO: starts scraping, pushed updates to console. 
        tbs.getMetaFromTunebat(directory,artist_thresh,track_thresh,search_thresh,meta,hypen)

        # Print the selected options and directory to the console
        print(f"Recheck Meta: {meta}")
        print(f"Hypen Separation: {hypen}")
        print(f"Artist Name Thresh: {artist_thresh}")
        print(f"Track Name Thresh: {track_thresh}")
        print(f"Search Thresh: {search_thresh}")
        print(f"Directory: {directory}")

app = App()
app.mainloop()

