import sys, os, re

# --- Get absolute path to resource ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

# --- Retrives songs from songs subfolder ---
songs_folder = resource_path(os.path.join("assets", "song list"))
