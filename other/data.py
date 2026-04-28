import customtkinter as ctk
from tkinter import ttk, messagebox
import json, os, re, requests, yt_dlp, threading
from PIL import Image
from datetime import datetime
from io import BytesIO

# --- Configuration ---
DB_FILE = os.path.join("data", "episodes.json")
THUMB_DIR = os.path.join("data", "thumbnails")
os.makedirs(THUMB_DIR, exist_ok=True)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def format_views(n):
    if not n: return "0"
    try:
        n = int(n)
        if n >= 1000000: return f"{n/1000000:.1f}M"
        if n >= 1000: return f"{n/1000:.1f}K"
        return str(n)
    except: return "0"

class ModernEpisodePanel(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Savage Seerat | Admin Dashboard")
        self.geometry("1300x850")
        self.episodes = self.load_data()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="EPISODE\nPANEL", font=("Arial", 24, "bold")).pack(pady=30)

        self.add_btn = ctk.CTkButton(self.sidebar, text="+ New Episode", command=self.open_add_window, height=40)
        self.add_btn.pack(pady=10, padx=20)

        # MAGIC SYNC BUTTON
        self.sync_btn = ctk.CTkButton(self.sidebar, text="🔄 Sync All Views", fg_color="orange", text_color="black", command=self.sync_all_views_threaded)
        self.sync_btn.pack(pady=10, padx=20)

        self.stats_label = ctk.CTkLabel(self.sidebar, text=f"Total: {len(self.episodes)}")
        self.stats_label.pack(side="bottom", pady=20)

        # --- Main Table ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        cols = ("id", "title", "date", "time", "views")
        self.tree = ttk.Treeview(self.main_frame, columns=cols, show="headings")
        for col in cols: self.tree.heading(col, text=col.upper())
        
        self.tree.column("id", width=60)
        self.tree.column("title", width=400)
        self.tree.column("views", width=100, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=20, pady=20)

        self.btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.btn_frame.pack(fill="x", padx=20, pady=10)
        ctk.CTkButton(self.btn_frame, text="Edit Selected", fg_color="#2196F3", command=self.edit_selected).pack(side="left", padx=5)
        ctk.CTkButton(self.btn_frame, text="Delete", fg_color="#f44336", command=self.delete_selected).pack(side="left", padx=5)

        self.refresh_tree()

    def load_data(self):
        if os.path.exists(DB_FILE):
            with open(DB_FILE, "r", encoding="utf-8") as f: return json.load(f)
        return []

    def save_data(self):
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(self.episodes, f, indent=2, ensure_ascii=False)
        self.stats_label.configure(text=f"Total: {len(self.episodes)}")

    def refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for ep in self.episodes:
            v = format_views(ep.get("views", 0))
            self.tree.insert("", "end", values=(ep["id"], ep["title"], ep["date"], ep.get("time", ""), v))

    # --- THE SYNC LOGIC ---
    def sync_all_views_threaded(self):
        """Runs the sync in a background thread so the UI doesn't freeze."""
        self.sync_btn.configure(state="disabled", text="Syncing...")
        threading.Thread(target=self.run_sync, daemon=True).start()

    def run_sync(self):
        count = 0
        total = len(self.episodes)
        
        with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
            for ep in self.episodes:
                vid_id = ep.get("videoId")
                if vid_id:
                    try:
                        # Fetch only basic info (fast)
                        info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid_id}", download=False)
                        ep["views"] = info.get("view_count", 0)
                        count += 1
                        print(f"Synced {ep['id']}: {ep['views']} views")
                    except Exception as e:
                        print(f"Failed to sync {vid_id}: {e}")
        
        self.save_data()
        self.after(0, self.finish_sync)

    def finish_sync(self):
        self.refresh_tree()
        self.sync_btn.configure(state="normal", text="🔄 Sync All Views")
        messagebox.showinfo("Success", "All episode views have been updated from YouTube!")

    # --- FORM & CRUD ---
    def edit_selected(self):
        sel = self.tree.selection()
        if sel: 
            idx = self.tree.index(sel[0])
            self.episode_form(self.episodes[idx], idx)

    def delete_selected(self):
        sel = self.tree.selection()
        if sel:
            idx = self.tree.index(sel[0])
            if messagebox.askyesno("Confirm", "Delete episode?"):
                del self.episodes[idx]; self.save_data(); self.refresh_tree()

    def open_add_window(self): self.episode_form()

    def episode_form(self, data=None, index=None):
        win = ctk.CTkToplevel(self)
        win.title("Episode Editor")
        win.geometry("950x850")
        win.attributes("-topmost", True)

        left = ctk.CTkFrame(win, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, padx=20, pady=20)
        right = ctk.CTkFrame(win, width=300)
        right.pack(side="right", fill="both", padx=20, pady=20)

        thumb_preview = ctk.CTkLabel(right, text="No Image", width=280, height=160, fg_color="#1a1a1a")
        thumb_preview.pack(pady=20)
        view_label = ctk.CTkLabel(right, text="Views: 0", font=("Arial", 16, "bold"))
        view_label.pack(pady=10)

        ctk.CTkLabel(left, text="YouTube Link:").pack(anchor="w")
        yt_input = ctk.CTkEntry(left, width=450)
        yt_input.pack(pady=5, anchor="w")
        
        state = {"thumb": data.get("thumbnail", "") if data else "", "raw_views": data.get("views", 0) if data else 0}
        if data: view_label.configure(text=f"Views: {format_views(state['raw_views'])}")

        def auto_fill():
            url = yt_input.get()
            if not url: return
            try:
                with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                    info = ydl.extract_info(url, download=False)
                    entries["title"].delete(0, 'end'); entries["title"].insert(0, info.get('title', ''))
                    entries["videoId"].delete(0, 'end'); entries["videoId"].insert(0, info.get('id', ''))
                    entries["time"].delete(0, 'end'); entries["time"].insert(0, f"{info.get('duration', 0)//60} min")
                    
                    date_str = datetime.strptime(info.get('upload_date', '20250101'), '%Y%m%d').strftime('%Y-%m-%d')
                    entries["date"].delete(0, 'end'); entries["date"].insert(0, date_str)
                    
                    state["raw_views"] = info.get('view_count', 0)
                    view_label.configure(text=f"Views: {format_views(state['raw_views'])}")

                    clean_t = re.sub(r'[^a-zA-Z0-9 ]', '', info.get('title', '')).lower().replace(" ", "-")
                    ep_id = entries["id"].get().lower().replace(" ", "") or "ep"
                    entries["link"].delete(0, 'end'); entries["link"].insert(0, f"/episode/{ep_id}-{clean_t}")

                    thumb_url = info.get('thumbnail', '')
                    if thumb_url:
                        img_data = requests.get(thumb_url).content
                        img = Image.open(BytesIO(img_data))
                        filename = f"{info.get('id')}.jpg"
                        save_path = os.path.join(THUMB_DIR, filename)
                        img.save(save_path)
                        state["thumb"] = f"data/thumbnails/{filename}"
                        img.thumbnail((280, 160))
                        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(280, 160))
                        thumb_preview.configure(image=ctk_img, text=""); thumb_preview.image = ctk_img
            except Exception as e: messagebox.showerror("Error", str(e))

        ctk.CTkButton(left, text="✨ Auto-Fill", fg_color="purple", command=auto_fill).pack(pady=10, anchor="w")

        fields = ["id", "title", "videoId", "time", "date", "link", "yt", "sp"]
        entries = {}
        for f in fields:
            ctk.CTkLabel(left, text=f.upper()).pack(anchor="w")
            e = ctk.CTkEntry(left, width=450)
            e.pack(anchor="w", pady=2)
            if data: e.insert(0, data.get(f, ""))
            entries[f] = e

        ctk.CTkLabel(left, text="DESCRIPTION").pack(anchor="w")
        entries["desc"] = ctk.CTkTextbox(left, width=450, height=80)
        entries["desc"].pack(anchor="w")
        if data: entries["desc"].insert("0.0", data.get("desc", ""))

        def save():
            new_ep = {f: entries[f].get() if f != "desc" else entries[f].get("0.0", "end").strip() for f in fields + ["desc"]}
            new_ep["thumbnail"] = state["thumb"]
            new_ep["views"] = state["raw_views"]
            if index is not None: self.episodes[index] = new_ep
            else: self.episodes.insert(0, new_ep)
            self.save_data(); self.refresh_tree(); win.destroy()

        ctk.CTkButton(win, text="SAVE EPISODE", height=50, fg_color="green", command=save).pack(side="bottom", pady=20)

if __name__ == "__main__":
    app = ModernEpisodePanel()
    app.mainloop()