import os
import requests

# === SETTINGS ===
base_url = "https://d3e4y8hquds3ek.cloudfront.net/institute/brilliantpalaelearn/courses/long-term-super-batch-medical-2025-online-g1/videos/transcoded/53b0a1abd7d74085865cdd0f9ca79bc0"
quality = "720p"   # change to "240p" if you want that version
start = 121          # first video number
end = 543          # last video number
save_folder = "downloads"  # folder to save files

# === CREATE SAVE FOLDER ===
os.makedirs(save_folder, exist_ok=True)

# === DOWNLOAD LOOP ===
for i in range(start, end + 1):
    url = f"{base_url}/{quality}/video_{i}.ts"
    filename = os.path.join(save_folder, f"video_{i}.ts")

    print(f"Downloading {url} ...")

    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f" Saved {filename}")
    except Exception as e:
        print(f"Failed {url} -> {e}")

print("🎉 All downloads finished!")
