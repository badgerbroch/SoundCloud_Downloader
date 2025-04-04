from pathlib import Path
from subprocess import call as sub_call
from csv import reader
from os import PathLike, rename, listdir

SOUNDCLOUD_CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXX"
"""Get your soundcloud client id from cookies when inspecting soundcloud webpage when signed in."""


class SoundCloudDownloader:
    def __init__(
        self, my_path_to_csv: str | PathLike, my_output_folder_path: str | PathLike
    ) -> None:
        self.path_to_csv = Path(my_path_to_csv)
        self.output_folder = Path(my_output_folder_path)

        self.total_songs = 0
        self.donwloaded_songs = 0
        self.fixed_song_paths = 0

    def download_songs_from_csv(self) -> None:
        """Downloads songs listed on the csv passed when creating the SoundCloudDownloader Object."""
        self.donwloaded_songs = 0
        self.fixed_song_paths = 0
        songs = self.get_song_paths()
        self.total_songs = len(songs)
        self.download_songs(song_list=songs)
        self.fix_file_names()

    def get_song_paths(self) -> list:
        """Function to handle getting list of soundcloud paths into list called song_paths"""
        # open csv
        with open(self.path_to_csv, mode="r") as file:
            csv_file = list(reader(file))
        self.total_songs = len(csv_file) - 1
        return csv_file

    def download_songs(self, song_list: list[str]) -> None:
        """Function to call download for each song in the list and to save the same without number"""
        output_folder = self.output_folder.name
        for i, song in enumerate(song_list):
            if i > 0:
                commandp1 = f"yt-dlp soundcloud.com/{song[0]} --add-header "
                commandp2 = f'"Authorization: OAuth {SOUNDCLOUD_CLIENT_ID}"'
                commandp3 = f" --paths {output_folder} --format mp3 --audio-quality 0 --embed-thumbnail"
                command = commandp1 + commandp2 + commandp3
                sub_call(command, shell=True)
                self.donwloaded_songs += 1

    def download_song(self, song: str) -> None:
        commandp1 = f"yt-dlp soundcloud.com/{song[0]} --add-header "
        commandp2 = f'"Authorization: OAuth {SOUNDCLOUD_CLIENT_ID}"'
        commandp3 = f" --paths {self.output_folder.name} --format mp3 --audio-quality 0 --embed-thumbnail"
        command = commandp1 + commandp2 + commandp3
        sub_call(command, shell=True)
        self.donwloaded_songs += 1

    def fix_file_names(self) -> None:
        """Fixes names of files in the output folder after downloading."""
        for file in listdir(self.output_folder):
            name_list = file.split("[")
            new_name = name_list[0][0 : len(name_list[0]) - 1] + ".mp3"
            rename(Path(self.output_folder / file), Path(self.output_folder / new_name))
            self.fixed_song_paths += 1
