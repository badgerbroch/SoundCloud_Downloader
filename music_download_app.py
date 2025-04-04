from pathlib import Path
from tkinter import RIGHT, TOP, Button, Frame, IntVar, Label, Tk, ttk
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import showwarning

from soundcloud_download import SoundCloudDownloader

TEXT_FONT = "Arial"
LARGE_TEXT_SIZE = 20
SMALL_TEXT_SIZE = 14

X_PADDING = 10
Y_PADDING = 10


class App(Tk):
    def __init__(self, my_title: str) -> None:
        super().__init__(my_title, my_title)
        self.geometry("500x700")
        self.config(background="black")
        self.title(my_title)
        # frontend
        self.header_frame = Frame(self, bg="black")
        self.title_label = Label(
            self.header_frame,
            text="SoundCloud Downloader",
            font=(TEXT_FONT, LARGE_TEXT_SIZE),
            background="black",
            fg="White",
        )
        self.title_label.pack(side=RIGHT, padx=X_PADDING, pady=Y_PADDING, expand=False)
        self.header_frame.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)

        self.body_frame = Frame(self, bg="black")

        self.select_file_label = Label(
            self.body_frame,
            text="Select File",
            font=(TEXT_FONT, LARGE_TEXT_SIZE),
            background="black",
            fg="white",
        )
        self.select_file_label.pack(
            side=TOP, padx=X_PADDING, pady=Y_PADDING, expand=False
        )

        self.browse_file_button = Button(
            self.body_frame,
            text="Browse csv File",
            font=(TEXT_FONT, LARGE_TEXT_SIZE),
            background="orange",
            command=self.select_csv_file,
        )
        self.browse_file_button.pack(
            side=TOP, padx=X_PADDING, pady=Y_PADDING, expand=False
        )

        self.select_output_folder_label = Label(
            self.body_frame,
            text="Select Output Folder",
            font=(TEXT_FONT, LARGE_TEXT_SIZE),
            background="black",
            fg="white",
        )
        self.select_output_folder_label.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)
        self.browse_folder_button = Button(
            self.body_frame,
            text="Choose Output Folder",
            font=(TEXT_FONT, LARGE_TEXT_SIZE),
            background="orange",
            command=self.select_output_folder,
        )
        self.browse_folder_button.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)

        self.body_frame.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)

        # class attributes
        self.current_csv_file = None
        self.output_folder = None

        self.csv_label = None
        self.output_folder_label = None
        self.completed_label = None
        self.download_button = None

    def select_csv_file(self):
        self.current_csv_file = askopenfilename(title="Select CSV File")
        if self.current_csv_file:
            if self.csv_label:
                self.csv_label.config(
                    text=f"{Path(self.current_csv_file).name} selected for Download"
                )
            else:
                self.csv_label = Label(
                    text=f"{Path(self.current_csv_file).name} selected for Download",
                    font=(TEXT_FONT, SMALL_TEXT_SIZE),
                    padx=X_PADDING,
                    pady=Y_PADDING,
                    background="black",
                    fg="white",
                )
                self.csv_label.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)
        if self.output_folder and self.current_csv_file:
            self.make_download_button()

    def select_output_folder(self) -> None:
        self.output_folder = askdirectory(title="Select Output Folder")
        if self.output_folder:
            if self.output_folder_label:
                self.output_folder_label.config(
                    text=f"{Path(self.output_folder).name} selected for mp3 downloads."
                )
            else:
                self.output_folder_label = Label(
                    text=f"{Path(self.output_folder).name} selected for mp3 downloads.",
                    font=(TEXT_FONT, SMALL_TEXT_SIZE),
                    padx=X_PADDING,
                    pady=Y_PADDING,
                    background="black",
                    fg="white",
                )
                self.output_folder_label.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)
        if self.output_folder and self.current_csv_file:
            self.make_download_button()

    def download_soundcloud_playlist(self) -> None:
        if not self.current_csv_file or not self.output_folder:
            showwarning("Select a csv file and an output folder directory")
        if self.completed_label:
            self.completed_label.pack_forget()
        self.soundcloud_downloader = SoundCloudDownloader(
            my_path_to_csv=self.current_csv_file,
            my_output_folder_path=self.output_folder,
        )
        song_list = self.soundcloud_downloader.get_song_paths()
        self.track_and_display_download_progress()
        for i, song in enumerate(song_list):
            if i > 0:
                self.soundcloud_downloader.download_song(song)
                self.update()
        self.soundcloud_downloader.fix_file_names()

        # self.soundcloud_downloader.download_songs_from_csv()

    def track_and_display_download_progress(self) -> None:
        if self.completed_label:
            self.completed_label.pack_forget()
        self.loading_label = Label(
            text=f"Downloading 1 of {self.soundcloud_downloader.total_songs}",
            font=(TEXT_FONT, SMALL_TEXT_SIZE),
            bg="black",
            fg="white",
        )
        self.loading_label.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)
        self.progress = IntVar()
        self.progress_bar = ttk.Progressbar(
            self, length=200, orient="horizontal", variable=self.progress
        )

        self.progress_bar.pack(side=TOP)
        self.check_download_progress()

    def check_download_progress(self) -> None:
        print(f"{self.soundcloud_downloader.total_songs}")
        print(f"{self.soundcloud_downloader.donwloaded_songs=}")
        if (
            self.soundcloud_downloader.total_songs
            > self.soundcloud_downloader.donwloaded_songs
        ):
            self.loading_label.config(
                text=f"Downloaded {self.soundcloud_downloader.donwloaded_songs} of {self.soundcloud_downloader.total_songs}"
            )
            step = int(
                (
                    self.soundcloud_downloader.donwloaded_songs
                    / self.soundcloud_downloader.total_songs
                )
                * 100
            )
            self.progress.set(step)
            self.update()
            self.after(250, self.check_download_progress)
        else:
            self.progress_bar.pack_forget()
            self.loading_label.pack_forget()
            self.completed_label = Label(
                self,
                text=f"Download Complete: {Path(self.current_csv_file).name} downloaded to {Path(self.output_folder).name}",
                background="black",
                fg="white",
            )
            self.completed_label.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)

    def make_download_button(self) -> None:
        if not self.download_button:
            self.download_button = Button(
                self,
                text="Download",
                font=(TEXT_FONT, LARGE_TEXT_SIZE),
                command=self.download_soundcloud_playlist,
            )
            self.download_button.pack(side=TOP, padx=X_PADDING, pady=Y_PADDING)


app = App(my_title="Soundcloud Downloader")
app.mainloop()
