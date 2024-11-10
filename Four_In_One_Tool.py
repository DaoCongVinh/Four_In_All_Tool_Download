import tkinter as tk 
from tkinter import ttk, messagebox
from pytube import YouTube
import yt_dlp

class DownloaderApp:
    def __init__(self, root):
        root.title("Four in One Tool")
        root.geometry("1000x450")
        root.config(bg="#1a1a2e")

        self.platform = "YouTube"

        main_frame = tk.Frame(root, bg="#1a1a2e")
        main_frame.pack(side="top", fill="both", expand=True)
        main_frame.pack_propagate(False)

        left_frame = tk.Frame(main_frame, bg="#1a1a2e")
        left_frame.pack(side="left", padx=10, pady=10, fill="y")

        title_label = tk.Label(left_frame, text="FOUR IN ONE TOOL", font=("Lato", 24, "bold"), fg="white", bg="#1a1a2e")
        title_label.pack(pady=10)

        icon_frame = tk.Frame(left_frame, bg="#1a1a2e")
        icon_frame.pack(pady=5)

        facebook_icon = tk.PhotoImage(file="img/fb.png").subsample(6, 6)
        youtube_icon = tk.PhotoImage(file="img/ytb.png").subsample(6, 6)
        instagram_icon = tk.PhotoImage(file="img/insta.png").subsample(6, 6)
        tiktok_icon = tk.PhotoImage(file="img/tt.png").subsample(6, 6)

        for icon, platform in [(facebook_icon, "Facebook"), (youtube_icon, "YouTube"), (instagram_icon, "Instagram"), (tiktok_icon, "TikTok")]:
            btn = tk.Button(icon_frame, image=icon, command=lambda p=platform: self.select_platform(p), bg="#1a1a2e", relief="flat")
            btn.image = icon
            btn.pack(side="left", padx=10)

        link_frame = tk.Frame(left_frame, bg="#1a1a2e")
        link_frame.pack(pady=10)
        tk.Label(link_frame, text="Enter Video Link:", fg="white", bg="#1a1a2e", font=("Arial", 12, "bold")).pack(side="left", padx=5)
        
        self.link_entry = tk.Entry(link_frame, width=40, font=("Arial", 10))
        self.link_entry.pack(side="left", padx=5)

        options_frame = tk.Frame(left_frame, bg="#1a1a2e")
        options_frame.pack(pady=10)
        tk.Label(options_frame, text="Resolution:", fg="white", bg="#1a1a2e", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        
        self.resolution_var = ttk.Combobox(options_frame, values=["480p", "720p", "1080p"], state="readonly", width=10)
        self.resolution_var.current(2)
        self.resolution_var.grid(row=0, column=1, padx=5)

        tk.Label(options_frame, text="Format:", fg="white", bg="#1a1a2e", font=("Arial", 12, "bold")).grid(row=1, column=0, padx=5)
        
        self.format_var = ttk.Combobox(options_frame, values=["mp4", "mp3"], state="readonly", width=10)
        self.format_var.current(0)
        self.format_var.grid(row=1, column=1, padx=5)

        buttons_frame = tk.Frame(left_frame, bg="#1a1a2e")
        buttons_frame.pack(pady=15)
        
        start_btn = tk.Button(buttons_frame, text="Start", command=self.start_download, 
                              bg="#28a745", fg="white", font=("Arial", 12, "bold"), width=10)
        start_btn.pack(side="left", padx=10)
        
        pause_btn = tk.Button(buttons_frame, text="Pause", bg="#007bff", fg="white", 
                              font=("Arial", 12, "bold"), width=10)
        pause_btn.pack(side="left", padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Cancel", bg="#dc3545", fg="white", 
                               font=("Arial", 12, "bold"), width=10)
        cancel_btn.pack(side="left", padx=10)

        right_frame = tk.Frame(main_frame, bg="#1a1a2e", relief="sunken", bd=2)
        right_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

        tk.Label(right_frame, text="Download Progress", font=("Arial", 14, "bold"), fg="white", bg="#1a1a2e").pack(pady=5)

        self.progress_listbox = tk.Listbox(right_frame, bg="#000000", fg="white", font=("Arial", 10), width=70, height=20)
        self.progress_listbox.pack(padx=10, pady=10)

        footer_label = tk.Label(root, text="© Bản quyền thuộc về Đào Công Vinh", bg="#1a1a2e", fg="white", font=("Nexa Extra Ligth", 12, "italic"))
        footer_label.pack(side="bottom", fill="x", pady=5)

    def select_platform(self, platform):
        self.platform = platform
        messagebox.showinfo("Platform Selected", f"You selected {platform}")

    def start_download(self):
        link = self.link_entry.get()
        resolution = self.resolution_var.get()
        format_type = self.format_var.get()
        if not link:
            messagebox.showwarning("Input Error", "Please enter a video link.")
            return

        if self.platform == "YouTube":
            self.download_youtube(link, resolution)
        elif self.platform == "TikTok":
            self.download_tiktok_profile(link)
        else:
            self.download_other(link)

    def download_youtube(self, link, resolution):
        try:
            yt = YouTube(link)
            stream = yt.streams.filter(res=resolution, file_extension="mp4").first()
            if not stream:
                self.progress_listbox.insert(tk.END, f"{resolution} resolution not available.")
                return

            # file_size = stream.filesize / (1024 * 1024)
            # # self.progress_listbox.insert(tk.END, f"Downloading {link} ({file_size:.2f} MB)...")
            
            # stream.download(output_path="downloads")
            # # self.progress_listbox.insert(tk.END, f"Download complete: {link} ({file_size:.2f} MB).")
        
        except Exception as e:
            # self.progress_listbox.insert(tk.END, f"Failed to download {link} with pytube: {str(e)}")
            self.progress_listbox.insert(tk.END, "Attempting to download ...")
            self.download_youtube_with_yt_dlp(link)

    def download_youtube_with_yt_dlp(self, link):
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'quiet': True,
                'progress_hooks': [self.update_progress]
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            self.progress_listbox.insert(tk.END, "Download complete.")
        
        except Exception as e:
            self.progress_listbox.insert(tk.END, f"Failed to download {link} : {str(e)}")

    def download_tiktok_profile(self, profile_link):
        try:
            ydl_opts = {
                'format': 'best',
                'outtmpl': 'downloads/%(uploader)s/%(title)s.%(ext)s',
                'quiet': True,
                'progress_hooks': [self.update_progress]
            }
            self.progress_listbox.insert(tk.END, f"Scanning TikTok profile {profile_link} for videos...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([profile_link])

            self.progress_listbox.insert(tk.END, f"All videos downloaded from {profile_link}.")
        
        except Exception as e:
            self.progress_listbox.insert(tk.END, f"Failed to download from TikTok profile {profile_link}: {str(e)}")

    def download_other(self, link):
        self.progress_listbox.insert(tk.END, f"Feature for {self.platform} not implemented yet.")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            percentage = d['_percent_str']
            self.progress_listbox.insert(tk.END, f"Downloading: {percentage}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloaderApp(root)
    root.mainloop()
