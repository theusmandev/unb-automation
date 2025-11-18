# import cv2
# import os
# from pytube import YouTube
# from PIL import Image

# def video_to_slides(youtube_url, output_dir="slides", interval_sec=1):
#     # Create output folder
#     os.makedirs(output_dir, exist_ok=True)

#     # Step 1: Download video
#     print("📥 Downloading video...")
#     yt = YouTube(youtube_url)
#     stream = yt.streams.filter(file_extension="mp4", res="720p").first()
#     if not stream:
#         stream = yt.streams.get_highest_resolution()
#     video_path = stream.download(filename="temp_video.mp4")
#     print("✅ Video downloaded!")

#     # Step 2: Read video
#     cap = cv2.VideoCapture(video_path)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frame_interval = int(fps * interval_sec)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     total_seconds = frame_count / fps

#     print(f"🎞 Total duration: {total_seconds:.1f}s — Extracting every {interval_sec}s")

#     count = 0
#     slide_num = 1
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if count % frame_interval == 0:
#             img_path = os.path.join(output_dir, f"slide_{slide_num:03}.png")
#             cv2.imwrite(img_path, frame)
#             slide_num += 1
#         count += 1

#     cap.release()
#     os.remove(video_path)
#     print(f"✅ {slide_num-1} slides saved in '{output_dir}' folder.")

# # Example use
# youtube_link = input("Enter YouTube Video URL: ")
# video_to_slides(youtube_link, interval_sec=2)







#ok good

# import cv2, os, subprocess
# from PIL import Image

# def video_to_slides(youtube_url, output_dir="slides", interval_sec=1):
#     os.makedirs(output_dir, exist_ok=True)

#     print("📥 Downloading with yt-dlp...")
#     subprocess.run([
#         "yt-dlp", "-f", "best[ext=mp4]", "-o", "temp_video.mp4", youtube_url
#     ], check=True)

#     cap = cv2.VideoCapture("temp_video.mp4")
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frame_interval = int(fps * interval_sec)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     total_seconds = frame_count / fps

#     print(f"🎞 Duration: {total_seconds:.1f}s — Every {interval_sec}s")

#     count = 0
#     slide_num = 1
#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if count % frame_interval == 0:
#             img_path = os.path.join(output_dir, f"slide_{slide_num:03}.png")
#             cv2.imwrite(img_path, frame)
#             slide_num += 1
#         count += 1

#     cap.release()
#     os.remove("temp_video.mp4")
#     print(f"✅ {slide_num-1} slides saved in '{output_dir}' folder.")

# youtube_link = input("Enter YouTube link: ")
# video_to_slides(youtube_link, interval_sec=10)



#ok good version with pdf converter

# import cv2, os, subprocess
# from PIL import Image

# def video_to_pdf(youtube_url, output_pdf="slides.pdf", interval_sec=10):
#     temp_dir = "temp_slides"
#     os.makedirs(temp_dir, exist_ok=True)

#     print("📥 Downloading YouTube video...")
#     subprocess.run([
#         "yt-dlp", "-f", "best[ext=mp4]", "-o", "temp_video.mp4", youtube_url
#     ], check=True)

#     cap = cv2.VideoCapture("temp_video.mp4")
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frame_interval = int(fps * interval_sec)
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     total_seconds = frame_count / fps
#     print(f"🎞 Duration: {total_seconds:.1f}s — Every {interval_sec}s")

#     count = 0
#     slide_num = 1
#     slides = []

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break
#         if count % frame_interval == 0:
#             img_path = os.path.join(temp_dir, f"slide_{slide_num:03}.png")
#             cv2.imwrite(img_path, frame)
#             slides.append(img_path)
#             slide_num += 1
#         count += 1

#     cap.release()
#     os.remove("temp_video.mp4")

#     # Convert PNGs → PDF
#     if slides:
#         print("🧩 Converting slides to PDF...")
#         images = [Image.open(p).convert("RGB") for p in slides]
#         images[0].save(output_pdf, save_all=True, append_images=images[1:])
#         print(f"✅ PDF created: {output_pdf}")
#     else:
#         print("⚠ No slides captured!")

#     # Clean up PNGs
#     for f in slides:
#         os.remove(f)
#     os.rmdir(temp_dir)

# # ---- Run ----
# youtube_link = input("Enter YouTube link: ")
# video_to_pdf(youtube_link, output_pdf="output.pdf", interval_sec=10)



#same uper wala code ha lakin fast ha 


# import cv2, os, subprocess, shutil
# from PIL import Image

# def video_to_pdf_fast(youtube_url, output_pdf="slides.pdf", interval_sec=10):
#     temp_dir = "temp_slides"
#     if os.path.exists(temp_dir):
#         shutil.rmtree(temp_dir)
#     os.makedirs(temp_dir)

#     print("📥 Downloading YouTube video (fast mode)...")

#     # ✅ Correct for Windows CMD — no extra quotes
#     cmd = f'yt-dlp -f "best[ext=mp4]" -o "temp_video.mp4" "{youtube_url}"'
#     result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
#     if result.returncode != 0:
#         print("❌ yt-dlp download failed:\n", result.stderr)
#         return
#     else:
#         print("✅ Download complete!")

#     cap = cv2.VideoCapture("temp_video.mp4")
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     frame_interval = int(fps * interval_sec)
#     total_seconds = total_frames / fps
#     print(f"🎞 Duration: {total_seconds:.1f}s — Capturing every {interval_sec}s")

#     slides = []
#     slide_num = 1
#     for pos in range(0, total_frames, frame_interval):
#         cap.set(cv2.CAP_PROP_POS_FRAMES, pos)
#         ret, frame = cap.read()
#         if not ret:
#             break
#         img_path = os.path.join(temp_dir, f"slide_{slide_num:03}.jpg")
#         cv2.imwrite(img_path, frame, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
#         slides.append(img_path)
#         slide_num += 1

#     cap.release()
#     os.remove("temp_video.mp4")

#     if slides:
#         print("🧩 Creating PDF...")
#         images = [Image.open(p).convert("RGB") for p in slides]
#         images[0].save(output_pdf, save_all=True, append_images=images[1:])
#         print(f"✅ PDF saved successfully: {output_pdf}")
#     else:
#         print("⚠ No frames captured!")

#     shutil.rmtree(temp_dir)

# # ---- Run ----
# youtube_link = input("Enter YouTube link: ").strip()
# video_to_pdf_fast(youtube_link, output_pdf="output.pdf", interval_sec=10)




