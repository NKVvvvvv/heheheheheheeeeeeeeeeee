import os
import requests
import subprocess

# === SETTINGS ===
base_url = "<link of the vide>"  #enter the url of the download without the video_{}.ts 

quality = "720p"   # change to "240p" if you want that version
start = 1
end = 543
save_folder = "downloads"
merged_video = "final_video.mp4"

# === CREATE SAVE FOLDER ===
os.makedirs(save_folder, exist_ok=True)

# === DOWNLOAD LOOP ===
for i in range(start, end + 1):
    url = f"{base_url}/{quality}/video_{i}.ts"
    filename = os.path.join(save_folder, f"video_{i}.ts")

    if os.path.exists(filename):
        print(f" Skipping {filename}, already exists.")
        continue

    print(f" Downloading {url} ...")
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

# === CREATE FILE LIST FOR FFMPEG ===
file_list = os.path.join(save_folder, "file_list.txt")
with open(file_list, "w") as f:
    for i in range(start, end + 1):
        f.write(f"file 'video_{i}.ts'\n")

# === MERGE USING FFMPEG ===
print(" Merging all .ts files into one video...")
cmd = [
    "ffmpeg",
    "-f", "concat",
    "-safe", "0",
    "-i", file_list,
    "-c", "copy",
    merged_video
]

subprocess.run(cmd)

print(f"🎉 Done! Final video saved as {merged_video}")

