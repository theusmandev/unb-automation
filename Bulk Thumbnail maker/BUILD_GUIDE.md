# Bulk Thumbnail Maker - EXE Build Guide

## 📦 Quick Start (Easiest Method)

### Option 1: One-Click Build (Recommended)
Simply double-click `build_exe.bat` in Windows Explorer!

This will:
1. ✅ Install all dependencies
2. ✅ Build your .exe file
3. ✅ Place it in the `dist` folder

### Option 2: Manual Build

1. **Install PyInstaller**
   ```bash
   pip install -r requirements.txt
   ```

2. **Build the executable**
   ```bash
   pyinstaller --clean build_exe.spec
   ```

3. **Find your .exe**
   The executable will be in: `dist\BulkThumbnailMaker.exe`

---

## 🚀 Running Your Application

1. Navigate to the `dist` folder
2. Double-click `BulkThumbnailMaker.exe`
3. The app will run without needing Python installed!

---

## ⚙️ Customization Options

### Change Console Behavior
In `build_exe.spec`, line 32:
- `console=True` → Shows console window (good for debugging)
- `console=False` → No console window (cleaner for end users)

### Add an Icon
1. Get a `.ico` file (icon image)
2. Place it in the project folder
3. In `build_exe.spec`, line 34, change:
   ```python
   icon='your_icon.ico'
   ```

### Include Additional Files
In `build_exe.spec`, modify the `datas` list:
```python
datas=[
    ('RobotoCondensed-BoldItalic.ttf', '.'),
    ('other_file.txt', '.'),  # Add more files here
],
```

---

## 📋 Distribution

### Sharing Your App
To share your app with others:

**Simple Distribution:**
- Share the entire `dist` folder
- Users can run `BulkThumbnailMaker.exe` directly
- No Python installation required!

**Single File Distribution:**
Already configured! The .exe is standalone.

---

## 🛠 Creating an MSI Installer (Advanced)

If you want a professional installer (.msi), use these tools:

### Option A: Advanced Installer (Recommended)
1. Download [Advanced Installer](https://www.advancedinstaller.com/)
2. Create new project → Simple Project
3. Add your .exe file from the `dist` folder
4. Build the MSI installer

### Option B: WiX Toolset (Free, More Complex)
1. Install [WiX Toolset](https://wixtoolset.org/)
2. Create a WiX configuration file
3. Build using WiX commands

### Option C: Inno Setup (Free, Easy)
1. Download [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Use the wizard to create an installer
3. Point to your .exe file

---

## 🐛 Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "Module not found" errors
- Run: `pip install -r requirements.txt`
- Try: `pip install --upgrade pillow pyinstaller`

### .exe is too large
- This is normal! PyInstaller bundles Python + all libraries
- Typical size: 20-50 MB
- You can reduce size with UPX compression (already enabled)

### .exe doesn't run on other computers
- Make sure you built on the same architecture (32-bit or 64-bit)
- For maximum compatibility, build on a 64-bit system with `--onefile` flag

---

## 📁 Project Structure After Build

```
Bulk Thumbnail maker/
├── main.py                          # Your source code
├── RobotoCondensed-BoldItalic.ttf  # Font file
├── requirements.txt                 # Python dependencies
├── build_exe.spec                   # PyInstaller config
├── build_exe.bat                    # One-click builder
├── build/                           # Temporary build files
└── dist/
    └── BulkThumbnailMaker.exe      # 🎉 Your final executable!
```

---

## ✅ Next Steps

1. Run `build_exe.bat` to create your .exe
2. Test the .exe in the `dist` folder
3. Share the .exe with others (no Python needed!)
4. (Optional) Create an MSI installer for professional distribution

**Happy distributing! 🚀**
