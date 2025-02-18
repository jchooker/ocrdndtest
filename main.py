import tkinter as tk
from tkinter import messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from utils import *
from PIL import Image, ImageTk
from ocrext import *
from ocrext.ocrext.ocr import extract_text
#import debugpy

# debugpy.listen(("localhost", 5678)) #attaching debugger
# waiting_msg="xx*Waiting for debugger to attach*++"
# wait_count = 0
# def transform_waiting_msg():
#     for i in waiting_msg:
#         if i=='x':
#             i = '+'
#         elif i=='+':
#             i = 'x'
# print(f"{waiting_msg}")
# try:
#     debugpy.wait_for_client()
    
# except Exception as e:
#     print("DebugPy failed to initialize!")
# else:
#     print("DebugPy successfully initialized.")
DEFAULT_LF_LBL_TEXT = "Drop image here"

class DragDropApp:
    def __init__(self):
        print("Initializing drag and drop app")
        self.root = TkinterDnD.Tk()
        self.root.title("Test OCR space")
        self.root.geometry("800x600")
        self.root.config(bg="lightgray")

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)

        self.overlay_label = None
        self.set_up_frames()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.valid_file_state = False

    def set_up_frames(self):

        #configure grid to make columns expand proportionally
        self.left_frame = tk.Frame(self.root, bg="lightsteelblue1", relief="sunken", padx=10, pady=10)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        try:
            print("Registering drop target...")
            self.left_frame.drop_target_register(DND_FILES)
            print("✅ Drop target successfully registered!")
        except Exception as e:
            print(f"Error registering drop target:\n {e}")

        try:
            self.left_frame.dnd_bind('<<DropEnter>>', self.on_drag_enter)
            self.left_frame.dnd_bind('<<DropLeave>>', self.on_drag_leave)
            self.left_frame.dnd_bind('<<Drop>>', self.drag_response)
            print("✅ Events successfully bound!")
        except Exception as e:
            print(f"Error binding drag and drop events:\n {e}")


        self.right_frame = tk.Frame(self.root, background="steelblue1", relief="sunken")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        jetbrains_font1, jetbrains_font2 = get_font_for_label()

        lf_width = self.left_frame.winfo_width()

        self.lf_lbl = tk.Label(self.left_frame, text=DEFAULT_LF_LBL_TEXT, bg="lightsteelblue1", wraplength=lf_width, justify="left", font=jetbrains_font2)
        #^^making this one the "overlay" label, with both text and image during drag actions
        self.lf_lbl.place(relx=0.5, rely=0.5, anchor="center")
        #update wraplength for label in left frame if it becomes necessary
        self.left_frame.bind("<Configure>", self.update_wraplength)

        self.rf_lbl = tk.Label(self.right_frame, bg="steelblue1", fg="white", text="Test text content", font=jetbrains_font1)
        self.rf_lbl.place(anchor="nw", x=10, y=10)
        #^^removing "overlay_label" and making image and text both appear here
    
    def update_wraplength(self, event):
        new_width = event.width - 20
        self.lf_lbl.config(wraplength=new_width)

    def handle_overlay(self, is_valid: bool) -> None:
        # if self.lf_lbl is not None:
        #     return
        self.overlay_controller(is_valid)

    def overlay_controller(self, is_valid: bool) -> None:
        print("overlay_controller method init")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        check_loc = os.path.join(BASE_DIR, "assets", "green-check.png")
        x_loc = os.path.join(BASE_DIR, "assets", "red-x.png")
        if not os.path.exists(check_loc) or not os.path.exists(x_loc):
            both_scenario = not os.path.exists(check_loc) and not os.path.exists(x_loc)
            if both_scenario:
                print(f"Paths \'{check_loc}\' and \'{x_loc}\' not found!")
            else:
                which_causing_err = check_loc if not os.path.exists(check_loc) else x_loc
                print(f"Path \'{which_causing_err}\' not found!")
        image = None
        new_text = None
        if is_valid:
            image=Image.open(check_loc).convert("RGBA")
            new_text="Valid image type"
        else:
            image=Image.open(x_loc).convert("RGBA")
            new_text="Please provide a valid image type! (PNG, JPG, etc)"
        orig_width, orig_height = image.size
        aspect_ratio = orig_height / orig_width
        new_width = self.left_frame.winfo_width() - 10
        new_height = int(new_width * aspect_ratio)
        image = image.resize((new_width, new_height), Image.LANCZOS)
        #opacity / transparency / alpha adjustment
        r,g,b,alpha = image.split() #Extract channels (R,G,B,A)
        new_alpha = alpha.point(lambda p: int(p * 0.5)) #transparency layer preserving opacity
        #^^0.5 to reduce opacity to half
        image.putalpha(new_alpha)

        self.overlay_img = ImageTk.PhotoImage(image)

        self.lf_lbl.config(image=self.overlay_img, text=new_text, compound="top")
        print("image overlay changed")

    def remove_image_overlay(self):
        if self.lf_lbl:
            self.lf_lbl.config(image="", text=DEFAULT_LF_LBL_TEXT)
            print("Overlay destroyed.")

    def on_drag_enter(self, event) -> None:
        file_path = event.data #get file name?
        check_file_run = check_file_type(file_path)
        if check_file_run:
            self.handle_overlay(True)
        else:
            self.handle_overlay(False)
        self.valid_file_state = check_file_run

    def drag_response(self, event):
        self.remove_image_overlay()
        file_path = event.data.strip("{}")

        if not self.valid_file_state:
            self.remove_image_overlay()
            messagebox.showerror("Invalid file type", "Please provide a valid image type! (PNG, JPG, etc)")
            return
        
        try:
            print(file_path)
            extracted_text = extract_text(file_path)
            print(f"{type(extracted_text)}-type extracted_text came out as {extracted_text}")
            self.rf_lbl.config(text=extracted_text[:300], wraplength=self.right_frame.winfo_width() - 10)
        except Exception as e:
            messagebox.showerror("Exception", f"Exception encountered will extracting text from image: \n {e}")
            self.rf_lbl.config(text="OCR scan failed!", fg="red")

    def on_drag_leave(self, event) -> None:
        self.remove_image_overlay()
        print("left drag n drop area!")

    def run(self):
        try:
            print("Starting mainloop")
            self.root.mainloop()
        except Exception as e:
            print(f"Error starting mainloop: {e}")
        else:
            print("Main loop started!")
    
    def on_closing(self): #to properly shut window down
        self.root.quit()
        self.root.destroy()

def main():
    app = DragDropApp()
    app.run()


if __name__ == '__main__':
    main()

    #ok, apart from what I'm doing with the larger project, how can I import this library into a barebones project that tests the ocr function. Like if I have this as my main.py: