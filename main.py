import tkinter as tk
from PIL import Image
from PIL.PngImagePlugin import PngInfo
import os
import traceback

def read_file():
    filepath = text_filepath.get()
    filepath = filepath.strip('"')
    
    global img
    
    try:
        img = Image.open(filepath) # type is PIL.PngImagePlugin.PngImageFile
        parameters = img.text['parameters']
        text_png_info.delete("1.0", tk.END)
        text_png_info.insert(tk.END, parameters)
        label_status.config(text="")
    except (FileNotFoundError, AttributeError):
        img = None
        label_status.config(text="File cannot be opened.")
    except Exception as e:
        img = None
        label_status.config(text=traceback.format_exception_only(type(e), e))

def write_file():
    filepath = text_filepath.get()
    filepath = filepath.strip('"')
    fname, ext = os.path.splitext(filepath)
    filepath_new = f"{fname}_new{ext}"
    
    global img
    
    if img is None:
        label_status.config(text="Invalied operation.")
        return
    
    metadata = PngInfo()
    for k, v in img.text.items():
        if k == "parameters":
            metadata.add_text(k, text_png_info.get("1.0","end"))
        else:
            metadata.add_text(k, str(v))
            
    img.save(filepath_new, pnginfo=metadata)


img = None

# tkinterウィンドウ作成
root = tk.Tk()
root.title("PNG Info 取得・変更ツール")

# header
header = tk.Frame(master=root)
header.pack(side=tk.TOP, fill="both", expand=False)

# body
body = tk.Frame(master=root)
body.pack(side=tk.TOP, fill="both", expand=True)

# footer
footer = tk.Frame(master=root)
footer.pack(side=tk.TOP, fill="both", expand=False)

# ラベル
label = tk.Label(header, text="ファイル名: ")
label.pack(side=tk.LEFT)

# ファイルパス用のテキストボックス
text_filepath = tk.Entry(header)
text_filepath.pack(fill="both")

# 読み込みボタン
read_button = tk.Button(body, text="読み込み", command=read_file)
read_button.pack(side=tk.LEFT)

# 書き込みボタン
write_button = tk.Button(body, text="書き込み", command=write_file)
write_button.pack(side=tk.LEFT)

# png info用テキストボックス
text_png_info = tk.Text(body)
text_png_info.pack(fill="both", expand=True)

# ステータス表示用ラベル
label_status = tk.Label(footer)
label_status.pack(side=tk.LEFT)

root.mainloop()
