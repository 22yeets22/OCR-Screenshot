# OCR-Screenshot

OCR-Screenshot is a lightweight Python tool that lets you **take a screenshot and instantly extract the text from it** using [Tesseract OCR](https://github.com/tesseract-ocr/tesseract). The recognized text is automatically copied to your clipboard for quick pasting.

---

## ✨ Features
- 🔍 OCR (Optical Character Recognition) on any screen region  
- 🖼 Uses Windows' built-in Snipping Tool GUI (Win+Shift+S experience)  
- 📋 Copies extracted text directly to clipboard  
- 🧹 Optionally deletes leftover screenshot files saved by Windows  
- 🔒 Singleton process — prevents multiple instances from running at once  
- ⌨️ Hotkey support (default: **Shift+Win+O**)  

---

## 🚀 Usage
1. Run the script
2. Use Shift+Win+O to trigger OCR.
3. Select a region with the Windows snipping overlay.
4. The text will be extracted and copied to your clipboard automatically.

---

## 📝 Notes
- Works on **Windows** 10/11, since it uses the native ms-screenclip: snipping tool.
- OCR accuracy depends on the quality of text and Tesseract’s language data (you can install extra language packs if needed).
