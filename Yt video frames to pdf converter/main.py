
import cv2, os, subprocess, shutil
from PIL import Image
from tqdm import tqdm  # ✅ Progress bar library

def video_to_pdf_fast(youtube_url, output_pdf="slides.pdf", interval_sec=10):
    temp_dir = "temp_slides"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    print("📥 Downloading YouTube video (fast mode)...")

    # ✅ Download video using yt-dlp
    cmd = f'yt-dlp -f "best[ext=mp4]" -o "temp_video.mp4" "{youtube_url}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("❌ yt-dlp download failed:\n", result.stderr)
        return
    else:
        print("✅ Download complete!")

    # ✅ Read video
    cap = cv2.VideoCapture("temp_video.mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_interval = int(fps * interval_sec)
    total_seconds = total_frames / fps
    print(f"🎞 Duration: {total_seconds:.1f}s — Capturing every {interval_sec}s\n")

    slides = []
    slide_num = 1
    frame_positions = range(0, total_frames, frame_interval)

    # ✅ Progress bar loop
    for pos in tqdm(frame_positions, desc="🖼 Extracting frames", ncols=80):
        cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
        ret, frame = cap.read()
        if not ret:
            break
        img_path = os.path.join(temp_dir, f"slide_{slide_num:03}.jpg")
        cv2.imwrite(img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        slides.append(img_path)
        slide_num += 1

    cap.release()
    os.remove("temp_video.mp4")

    # ✅ Create PDF
    if slides:
        print("\n🧩 Creating PDF...")
        images = [Image.open(p).convert("RGB") for p in slides]
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"✅ PDF saved successfully: {output_pdf}")
    else:
        print("⚠ No frames captured!")

    shutil.rmtree(temp_dir)


# ---- Run ----
if __name__ == "__main__":
    youtube_link = input("Enter YouTube link: ").strip()
    video_to_pdf_fast(youtube_link, output_pdf="output.pdf", interval_sec=21)




