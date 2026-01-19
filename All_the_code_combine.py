import os
import requests
import subprocess

# === SETTINGS ===
base_url = "http://example.com/videos"
quality = "720p"
start = 0
end = 1000
save_folder = "downloads"

# === CREATE SAVE FOLDER ===
os.makedirs(save_folder, exist_ok=True)

# === DOWNLOAD LOOP ===
for i in range(start, end + 1):
    url = f"{base_url}/{quality}/video_{i}.ts"

    # zero-padded filename: video0001.ts
    filename = os.path.join(save_folder, f"video{i:04d}.ts")

    print(f"⬇ Downloading {url}")

    try:
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f" Saved {filename}")
    except Exception as e:
        print(f" Failed {url} -> {e}")

print("🎉 All downloads finished!")

# === MERGE STEP USING CMD COPY ===
print("Merging all .ts files into merged.ts ...")

merge_command = "copy /b *.ts merged.ts"

subprocess.run(
    ["cmd", "/c", merge_command],
    cwd=save_folder,
    shell=True
)

print("merged.ts created inside downloads folder")
