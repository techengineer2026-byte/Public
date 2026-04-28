import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import json
import requests
from io import BytesIO
from PIL import Image, ImageTk
import yt_dlp


# ═══════════════════════ CONFIG ═══════════════════════
CLIPS_JSON_PATH = r"E:\PPP\Public\data\clips.json"
# ═════════════════════════════════════════════════════


class YouTubeChannelDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("📺 YouTube Channel Downloader")
        self.root.geometry("950x720")
        self.root.minsize(800, 550)
        self.root.configure(bg="#1a1a2e")

        self.videos = []
        self.check_vars = []
        self.thumbnail_refs = []

        self._setup_styles()
        self._build_ui()

    # ────────────────────── STYLES ──────────────────────
    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                         fieldbackground="#2d2d4a",
                         background="#2d2d4a",
                         foreground="white",
                         selectbackground="#7c3aed",
                         selectforeground="white")
        style.configure("green.Horizontal.TProgressbar",
                         troughcolor="#2d2d4a",
                         background="#22c55e",
                         thickness=18)

    # ────────────────────── UI BUILD ──────────────────────
    def _build_ui(self):
        # ── TOP: URL bar ──
        top = tk.Frame(self.root, bg="#16213e", pady=8, padx=10)
        top.pack(fill="x")

        tk.Label(top, text="🔗 Channel URL:", bg="#16213e", fg="#e0e0e0",
                 font=("Segoe UI", 11)).pack(side="left", padx=(5, 2))

        self.url_entry = tk.Entry(top, font=("Segoe UI", 11), width=55,
                                  bg="#2d2d4a", fg="white",
                                  insertbackground="white", relief="flat",
                                  highlightthickness=1,
                                  highlightcolor="#7c3aed",
                                  highlightbackground="#3d3d5c")
        self.url_entry.pack(side="left", padx=5, fill="x", expand=True)
        self.url_entry.bind("<Return>", lambda e: self.load_channel())

        self.load_btn = tk.Button(top, text="📺  Load Channel",
                                  font=("Segoe UI", 10, "bold"),
                                  bg="#7c3aed", fg="white",
                                  activebackground="#6d28d9",
                                  activeforeground="white",
                                  relief="flat", cursor="hand2", padx=14,
                                  command=self.load_channel)
        self.load_btn.pack(side="left", padx=5)

        # ── SELECT ALL / DESELECT / COUNT / JSON INFO ──
        sel = tk.Frame(self.root, bg="#1a1a2e")
        sel.pack(fill="x", padx=12, pady=(6, 0))

        btn_style = dict(font=("Segoe UI", 9), bg="#2d2d4a", fg="white",
                         activebackground="#3d3d5c", relief="flat",
                         cursor="hand2", padx=8)

        tk.Button(sel, text="✅ Select All",
                  command=self.select_all, **btn_style).pack(side="left", padx=2)
        tk.Button(sel, text="❌ Deselect All",
                  command=self.deselect_all, **btn_style).pack(side="left", padx=2)

        self.json_lbl = tk.Label(sel, text="", bg="#1a1a2e", fg="#7c3aed",
                                 font=("Segoe UI", 9))
        self.json_lbl.pack(side="right", padx=5)

        self.count_lbl = tk.Label(sel, text="0 videos | 0 selected",
                                  bg="#1a1a2e", fg="#888",
                                  font=("Segoe UI", 9))
        self.count_lbl.pack(side="right", padx=5)

        # ── MIDDLE: scrollable video list ──
        list_wrap = tk.Frame(self.root, bg="#1a1a2e")
        list_wrap.pack(fill="both", expand=True, padx=12, pady=6)

        self.canvas = tk.Canvas(list_wrap, bg="#1a1a2e",
                                highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_wrap, orient="vertical",
                                  command=self.canvas.yview)
        self.scroll_frame = tk.Frame(self.canvas, bg="#1a1a2e")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.canvas.bind_all("<MouseWheel>",
                             lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        self.canvas.bind_all("<Button-4>",
                             lambda e: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>",
                             lambda e: self.canvas.yview_scroll(1, "units"))

        # ── BOTTOM: format · folder · download ──
        bot = tk.Frame(self.root, bg="#16213e", padx=10, pady=8)
        bot.pack(fill="x", padx=12, pady=(0, 6))

        tk.Label(bot, text="Format:", bg="#16213e", fg="#e0e0e0",
                 font=("Segoe UI", 10)).pack(side="left", padx=(5, 2))

        self.format_var = tk.StringVar(value="MP3 (Best)")
        formats = [
            "MP3 (Best)",
            "MP4  (Best)",
            "MP4  (4K - 2160p)",
            "MP4  (1080p)",
            "MP4  (720p)",
            "MP4  (480p)",
            "WebM (Best)",
        ]
        self.format_cb = ttk.Combobox(bot, textvariable=self.format_var,
                                      values=formats, state="readonly",
                                      width=18, font=("Segoe UI", 10))
        self.format_cb.pack(side="left", padx=4)

        self.folder_entry = tk.Entry(bot, font=("Segoe UI", 10),
                                     bg="#2d2d4a", fg="white",
                                     insertbackground="white", relief="flat",
                                     highlightthickness=1,
                                     highlightcolor="#7c3aed",
                                     highlightbackground="#3d3d5c")
        self.folder_entry.pack(side="left", padx=4, fill="x", expand=True)
        self.folder_entry.insert(0, os.path.expanduser("~/Downloads"))

        tk.Button(bot, text="📁", font=("Segoe UI", 11),
                  bg="#2d2d4a", fg="white", relief="flat",
                  cursor="hand2", padx=6,
                  command=self.browse_folder).pack(side="left", padx=2)

        self.dl_btn = tk.Button(bot, text="⬇  Download",
                                font=("Segoe UI", 11, "bold"),
                                bg="#22c55e", fg="white",
                                activebackground="#16a34a",
                                activeforeground="white",
                                relief="flat", cursor="hand2", padx=16,
                                command=self.start_download)
        self.dl_btn.pack(side="right", padx=5)

        # ── PROGRESS ──
        self.progress = ttk.Progressbar(self.root, mode="determinate",
                                        style="green.Horizontal.TProgressbar")
        self.progress.pack(fill="x", padx=12, pady=(0, 4))

        self.status_lbl = tk.Label(self.root, text="Ready — paste a channel URL above",
                                   bg="#1a1a2e", fg="#888",
                                   font=("Segoe UI", 9), anchor="w")
        self.status_lbl.pack(fill="x", padx=14, pady=(0, 6))

    # ────────────────────── HELPERS ──────────────────────
    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def select_all(self):
        for v in self.check_vars:
            v.set(True)

    def deselect_all(self):
        for v in self.check_vars:
            v.set(False)

    def _update_count(self):
        sel = sum(v.get() for v in self.check_vars)
        self.count_lbl.config(text=f"{len(self.videos)} videos | {sel} selected")

    @staticmethod
    def _fmt_duration(seconds):
        if seconds is None:
            return "—"
        s = int(seconds)
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    # ────────────────────── JSON: LOAD / SAVE ──────────────────────
    @staticmethod
    def _load_clips_json():
        """
        Read existing clips.json.
        Returns (list_of_entries, set_of_ids).
        Creates the file/dir if missing.
        """
        if not os.path.exists(CLIPS_JSON_PATH):
            os.makedirs(os.path.dirname(CLIPS_JSON_PATH), exist_ok=True)
            with open(CLIPS_JSON_PATH, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=4)
            return [], set()

        try:
            with open(CLIPS_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                data = []
        except (json.JSONDecodeError, IOError):
            data = []

        existing_ids = {entry.get("id") for entry in data if "id" in entry}
        return data, existing_ids

    @staticmethod
    def _save_clips_json(data):
        """Write the full list back to clips.json."""
        os.makedirs(os.path.dirname(CLIPS_JSON_PATH), exist_ok=True)
        with open(CLIPS_JSON_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _append_new_to_json(self, videos):
        """
        Add only new videos to clips.json.
        Returns (new_count, already_count).
        """
        data, existing_ids = self._load_clips_json()

        new_count = 0
        for vid in videos:
            vid_id = vid.get("id")
            if not vid_id:
                continue
            if vid_id not in existing_ids:
                title = vid.get("title", "Untitled").strip()
                # ensure trailing \n like your example
                if not title.endswith("\n"):
                    title += "\n"
                data.append({
                    "type": "youtube",
                    "title": title,
                    "id": vid_id,
                })
                existing_ids.add(vid_id)
                new_count += 1

        self._save_clips_json(data)
        already_count = len(videos) - new_count
        return new_count, already_count

    # ────────────────────── LOAD CHANNEL ──────────────────────
    def load_channel(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Paste a YouTube channel URL first.")
            return

        self.load_btn.config(state="disabled", text="⏳ Loading…")
        self.status_lbl.config(text="Fetching channel info…")
        self.json_lbl.config(text="")

        # clear old
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self.videos.clear()
        self.check_vars.clear()
        self.thumbnail_refs.clear()

        threading.Thread(target=self._fetch_channel, args=(url,), daemon=True).start()

    def _fetch_channel(self, url):
        try:
            ydl_opts = {
                "extract_flat": True,
                "quiet": True,
                "no_warnings": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)

            entries = info.get("entries") or []

            for e in entries:
                if e is None:
                    continue
                if e.get("_type") == "playlist":
                    continue
                vid_id = e.get("id")
                if not vid_id:
                    continue
                self.videos.append(e)

            # ── AUTO APPEND TO clips.json ──
            new_count, already_count = self._append_new_to_json(self.videos)

            self.root.after(0, lambda: self._display_videos(new_count, already_count))

        except Exception as exc:
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"Could not fetch channel:\n{exc}"))
            self.root.after(0, self._reset_load_btn)

    def _reset_load_btn(self):
        self.load_btn.config(state="normal", text="📺  Load Channel")
        self.status_lbl.config(text="❌ Failed to load channel")

    def _display_videos(self, new_count, already_count):
        for i, vid in enumerate(self.videos):
            self._make_row(i, vid)

        self._reset_load_btn()
        self.status_lbl.config(
            text=f"✅ Loaded {len(self.videos)} videos — {new_count} new added to JSON, {already_count} already existed"
        )
        self.json_lbl.config(
            text=f"📝 clips.json  +{new_count} new | {new_count + already_count} total"
        )
        self._update_count()

    def _make_row(self, idx, vid):
        row = tk.Frame(self.scroll_frame, bg="#22223b", pady=6, padx=8)
        row.pack(fill="x", padx=4, pady=2)

        row.bind("<Enter>", lambda e, r=row: r.configure(bg="#2d2d4a"))
        row.bind("<Leave>", lambda e, r=row: r.configure(bg="#22223b"))

        var = tk.BooleanVar(value=False)
        self.check_vars.append(var)
        var.trace_add("write", lambda *_: self._update_count())

        cb = tk.Checkbutton(row, variable=var, bg="#22223b",
                            activebackground="#22223b",
                            selectcolor="#7c3aed",
                            cursor="hand2")
        cb.pack(side="left", padx=(0, 6))

        thumb_lbl = tk.Label(row, bg="#3d3d5c", width=10, height=5, relief="flat")
        thumb_lbl.pack(side="left", padx=(0, 10))

        info = tk.Frame(row, bg="#22223b")
        info.pack(side="left", fill="x", expand=True)

        title = vid.get("title", "Untitled")
        tk.Label(info, text=title, bg="#22223b", fg="white",
                 font=("Segoe UI", 10, "bold"),
                 wraplength=550, justify="left",
                 anchor="w").pack(fill="x")

        dur = self._fmt_duration(vid.get("duration"))
        channel = vid.get("channel") or vid.get("uploader") or ""
        meta = f"⏱ {dur}   📌 {channel}" if channel else f"⏱ {dur}"
        tk.Label(info, text=meta, bg="#22223b", fg="#777",
                 font=("Segoe UI", 9), anchor="w").pack(fill="x")

        for child in (cb, thumb_lbl, info):
            child.bind("<Enter>", lambda e, r=row: r.configure(bg="#2d2d4a"))
            child.bind("<Leave>", lambda e, r=row: r.configure(bg="#22223b"))

        vid_id = vid.get("id", "")
        thumb_url = vid.get("thumbnail", "")
        if not thumb_url and vid_id:
            thumb_url = f"https://img.youtube.com/vi/{vid_id}/mqdefault.jpg"
        if thumb_url:
            threading.Thread(target=self._load_thumb,
                             args=(thumb_url, thumb_lbl), daemon=True).start()

    def _load_thumb(self, url, lbl):
        try:
            resp = requests.get(url, timeout=6)
            resp.raise_for_status()
            img = Image.open(BytesIO(resp.content))
            img = img.resize((120, 68), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            self.thumbnail_refs.append(photo)
            self.root.after(0, lambda: lbl.config(image=photo,
                                                   width=120, height=68))
        except Exception:
            pass

    # ────────────────────── DOWNLOAD ──────────────────────
    def start_download(self):
        selected = [(i, self.videos[i])
                    for i, v in enumerate(self.check_vars) if v.get()]
        if not selected:
            messagebox.showwarning("Nothing selected",
                                   "Tick at least one video.")
            return

        save_dir = self.folder_entry.get().strip()
        if not save_dir or not os.path.isdir(save_dir):
            messagebox.showwarning("Bad folder", "Choose a valid save folder.")
            return

        fmt = self.format_var.get()
        self.dl_btn.config(state="disabled", text="⏳ Downloading…")
        self.progress["value"] = 0

        threading.Thread(target=self._download_all,
                         args=(selected, save_dir, fmt), daemon=True).start()

    def _download_all(self, selected, save_dir, fmt):
        total = len(selected)
        errors = []

        for step, (i, vid) in enumerate(selected, 1):
            vid_id = vid.get("id")
            url = vid.get("url") or f"https://www.youtube.com/watch?v={vid_id}"
            title = vid.get("title", "video")

            self.root.after(0, lambda s=step, t=total, ti=title:
                            self.status_lbl.config(
                                text=f"({s}/{t}) ⬇ {ti}"))
            self.root.after(0, lambda s=step, t=total:
                            self.progress.config(value=(s - 1) / t * 100))

            opts = self._ydl_opts(fmt, save_dir)

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    ydl.download([url])
            except Exception as exc:
                errors.append((title, str(exc)))

        self.root.after(0, lambda: self.progress.config(value=100))

        if errors:
            msg = "\n".join(f"• {t}: {e[:80]}" for t, e in errors)
            self.root.after(0, lambda: messagebox.showwarning(
                "Some downloads failed", msg))
            self.root.after(0, lambda: self.status_lbl.config(
                text=f"⚠ Done with {len(errors)} error(s)"))
        else:
            self.root.after(0, lambda: self.status_lbl.config(
                text=f"✅ All {total} file(s) saved to {save_dir}"))

        self.root.after(0, lambda: self.dl_btn.config(
            state="normal", text="⬇  Download"))

    @staticmethod
    def _ydl_opts(fmt, save_dir):
        out = os.path.join(save_dir, "%(title).100s.%(ext)s")

        if fmt.startswith("MP3"):
            return {
                "format": "bestaudio/best",
                "outtmpl": out,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "0",
                }],
                "quiet": True, "no_warnings": True,
            }

        height_map = {
            "4K":   "2160",
            "1080": "1080",
            "720":  "720",
            "480":  "480",
        }

        if fmt.startswith("WebM"):
            return {
                "format": "bestvideo+bestaudio/best",
                "outtmpl": out,
                "merge_output_format": "webm",
                "quiet": True, "no_warnings": True,
            }

        h = None
        for key, val in height_map.items():
            if key in fmt:
                h = val
                break

        if h:
            fmt_str = (f"bestvideo[height<={h}][ext=mp4]+"
                       f"bestaudio[ext=m4a]/"
                       f"best[height<={h}]")
        else:
            fmt_str = ("bestvideo[ext=mp4]+bestaudio[ext=m4a]/"
                       "best[ext=mp4]/best")

        return {
            "format": fmt_str,
            "outtmpl": out,
            "merge_output_format": "mp4",
            "quiet": True, "no_warnings": True,
        }


# ────────────────────── MAIN ──────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeChannelDownloader(root)
    root.mainloop()