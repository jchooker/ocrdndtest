import tkinter as tk
import tkinter.font as tkFont
import os
from ctypes import windll
#
def get_font_for_label(size=14) -> tuple[tuple[str, int], tuple[str, int]]:
    root = tk.Tk()
    root.withdraw() #<-prevent accessory window from appearing

    #Load the custom font
    base_dir = os.path.dirname(os.path.abspath(__file__))
    prefix = os.path.join(base_dir, "assets", "fonts")
    font1_path = os.path.join(prefix, "JetBrainsMono[wght].ttf")
    font2_path = os.path.join(prefix, "JetBrainsMono-Italic[wght].ttf")

    #check if font 1 exists
    if not os.path.exists(font1_path):
        print("⚠️ JetBrains Mono TTF file not found! Falling back to default font.")
        root.destroy()
        return ("Courier", size) #<-fallback font
    
        #check if font 2 exists
    if not os.path.exists(font2_path):
        print("⚠️ JetBrains Mono Italic TTF file not found! Falling back to default font.")
        root.destroy()
        return ("Courier", size) #<-fallback font
    
    #load font 1 dynamically
    try:
        # On Windows, manually add font to system memory (does not install permanently)
        if os.name == "nt":
            FR_PRIVATE = 0x10
            FR_NOT_ENUM = 0x20
            windll.gdi32.AddFontResourceExW(font1_path, FR_PRIVATE, 0)
            font1_name = "JetBrains Mono"

    except Exception as e:
        print(f"⚠️ Error loading JetBrains Mono: {e}")
        root.destroy()
        return ("Courier", size) #<- fallback font
    
        #load font 2 dynamically
    try:
        # On Windows, manually add font to system memory (does not install permanently)
        if os.name == "nt":
            FR_PRIVATE = 0x10
            FR_NOT_ENUM = 0x20
            windll.gdi32.AddFontResourceExW(font2_path, FR_PRIVATE, 0)
            font2_name = "JetBrains Mono Italic"

    except Exception as e:
        print(f"⚠️ Error loading JetBrains Mono Italic: {e}")
        root.destroy()
        return ("Courier", size) #<- fallback font
    
    font1 = (font1_name, size)
    font2 = (font2_name, size - 2)
    
    #clean up tkinter
    root.destroy()

    return font1, font2

def check_file_type(file_path) -> bool:
    if file_path.startswith('{') and file_path.endswith('}'):
        file_path = file_path[1:-1]
        
    file_extension = os.path.splitext(file_path)[1].lower()
    allowed_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')

    if file_extension in allowed_extensions:
        #self.rf_lbl
        print('correct file type!')
        return True
    elif file_path.lower().endswith(allowed_extensions):
        #frame.config(cursor="@correct_file_cursor.xbm")
        print('correct file type!')
        return True
    else:
        print('incorrect file type!')
        return False