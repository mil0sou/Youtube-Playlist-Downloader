import tkinter as tk
import pytube
import time
import webbrowser
from tkinter import filedialog, messagebox, ttk
from pytube import Playlist
from pathlib import Path
import ssl

ssl._create_default_https_context = ssl._create_stdlib_context


def show_complete_message():
    messagebox.showinfo("Downloads Complete", "All downloads are complete.")
    root.destroy()


def browse_path():
    selected_path = filedialog.askdirectory()
    download_path_var.set(selected_path)


def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    formatted_time = ""
    if hours > 0:
        formatted_time += f"{hours:.0f} hour{'s' if hours > 1 else ''} "
    if minutes > 0 or hours > 0:
        formatted_time += f"{minutes:.0f} minute{'s' if minutes > 1 else ''} "
    formatted_time += f"{seconds:.0f} second{'s' if seconds > 1 else ''}"
    return formatted_time


root = tk.Tk()
root.title("YouTube Playlist Downloader by Milo")
# icon = tk.PhotoImage(file="D:\Code\WLdownloader\cat.png")
# root.iconphoto(False, icon)
root.geometry("600x330")

tk.Label(root, text="").pack()

playlist_label = tk.Label(root, text="Playlist URL:")
playlist_label.pack()
playlist_url_entry = tk.Entry(root, width=80)
playlist_url_entry.pack()

tk.Label(root, text="").pack()

download_path_label = tk.Label(root, text="Download Path:")
download_path_label.pack()
download_path_frame = tk.Frame(root)
download_path_frame.pack()

download_path_var = tk.StringVar()
download_path_entry = tk.Entry(
    download_path_frame, width=72, textvariable=download_path_var, state="readonly"
)
download_path_entry.pack(side="left")

browse_button = tk.Button(download_path_frame, text="Browse", command=browse_path)
browse_button.pack(side="left")

tk.Label(root, text="").pack()

resolution_label = tk.Label(root, text="Select Resolution:")
resolution_label.pack()
resolution_var = tk.StringVar(value="720p")
resolution_combo = ttk.Combobox(
    root,
    textvariable=resolution_var,
    values=["480p", "720p", "1080p"],
    state="readonly",
)
resolution_combo.pack()

tk.Label(root, text="").pack()


def start_download():
    start_time = time.time()
    inter_time = time.time()
    download_times = []
    playlist_url = playlist_url_entry.get()
    download_path = download_path_var.get()
    selected_resolution = resolution_var.get()
    playlist = Playlist(playlist_url)

    # download_path = "D:\Code\WLdownloader\Downloads"
    folder_name = playlist.title
    folder_path = Path(download_path) / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)

    download_path = f"{download_path}/{playlist.title}"

    print(f"\nDownloading playlist : {playlist.title} to {download_path}")

    numerovid = 1
    for video in playlist.videos:
        try:
            stream = video.streams.filter(
                file_extension="mp4", res=selected_resolution
            ).first()
            if stream is not None:
                percentagedown = numerovid / playlist.length * 100
                percentagedown2 = f"{percentagedown:.1f}"
                print(
                    f"\nDownloading: {video.title}... (video {numerovid} of {playlist.length} - {percentagedown2}%)"
                )
                stream.download(output_path=download_path)

                elapsed_time = time.time() - inter_time
                inter_time = time.time()
                print(
                    f"{video.title} downloaded successfully! Elapsed Time: {elapsed_time:.2f} seconds"
                )
                download_times.append(round(elapsed_time, 2))
                moy_temps = sum(download_times) / len(download_times)
                tempstotal = moy_temps * playlist.length
                tempsecoule = time.time() - start_time
                tempsrestant = tempstotal - tempsecoule

                print("Average download time :", round(moy_temps, 2), "s")
                print("Total estimated time :", format_time(tempstotal), "s")
                print("Total elapsed time :", round(tempsecoule, 2), "s")

                if float(percentagedown2) >= 99.9:
                    print("\nAll downloads are complete.\n")
                else:
                    print("Estimated remaining time :", format_time(tempsrestant))

            else:
                print(f"No suitable stream found for {video.title}")
        except pytube.exceptions.AgeRestrictedError:
            print(f"\n{video.title} is age-restricted. Skipping...")
            continue
        numerovid += 1


download_button = tk.Button(root, text="Start Download", command=start_download)
download_button.pack()

tk.Label(root, text="").pack()


hyperlink_label = ttk.Label(
    root,
    text="Credits : Milo",
    cursor="hand2",
    foreground="blue",
    font="Arial 10 underline",
)


def open_link(event):
    webbrowser.open("https://www.linkedin.com/in/milosou/", new=0, autoraise=True)


hyperlink_label.pack()
hyperlink_label.bind("<Button-1>", open_link)


root.mainloop()
