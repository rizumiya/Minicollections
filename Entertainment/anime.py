# Rend Ray (Rizumiya)
# Powered by api.waifu.im
# 2023/08/12
# Mini collections of rizumiya
# =================================

import customtkinter as ctk
import requests
import threading
import PIL.Image
import os

from PIL import ImageTk
from io import BytesIO
from tkinter import *

class AnimeAPI:
    API_URL = 'https://api.waifu.im/search'

    def __init__(self):
        self.params = {}

    def set_parameters(self, tags, height):
        self.params = {
            'included_tags': tags,
            'height': height
        }

    def get_image_urls(self, count=5):
        image_urls = []

        for _ in range(count):
            response = requests.get(self.API_URL, params=self.params)
            
            if response.status_code == 200:
                data = response.json()
                if 'images' in data and len(data['images']) > 0:
                    image_urls.append(data['images'][0]['url'])
                else:
                    print('No images found in the response.')
            else:
                print('Request failed with status code:', response.status_code)

        return image_urls


class MyGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Free Waifu Pics")
        self.geometry('700x500+500+200')
        self.resizable(False, False)

        self.scrollable_frame = None  # Tambahkan atribut scrollable_frame
        self.create_widgets()

    def create_widgets(self):
        self.create_template()
        self.create_var_widgets()

    def create_template(self):
        self.header = ctk.CTkLabel(self, text="Waifu Pics", font=('Fugaz One', 32, 'bold'))
        self.header.place(relx=0.5, y=30, anchor=CENTER)

        self.ordinary_frame = ctk.CTkFrame(self, width=170, height=200)
        self.ordinary_frame.place(x=20, y=80)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=450, height=380)
        self.scrollable_frame.place(x=200, y=80)

        self.bottom_frame = ctk.CTkFrame(self, width=170, height=180)
        self.bottom_frame.place(x=20, y=293)

    def create_var_widgets(self):
        self.sfw_tags = ['waifu', 'maid', 'marin-kitagawa', 'mori-calliope', 'raiden-shogun', 'oppai', 'selfies', 'uniform']
        self.nsfw_tags = ['ero', 'ass', 'hentai', 'milf', 'oral', 'paizuri', 'ecchi']

        self.tags_lbl = ctk.CTkLabel(self.ordinary_frame, text="Pick a tag")
        self.tags_lbl.place(x=15, y=10)

        self.ddown_tags = ctk.CTkOptionMenu(self.ordinary_frame, values=self.nsfw_tags) # Switch between nsfw or sfw
        self.ddown_tags.place(x=15, y=40)

        self.many_entry = ctk.CTkEntry(self.ordinary_frame, placeholder_text="How many pictures")
        self.many_entry.place(x=15, y=80)

        self.btn_confirm = ctk.CTkButton(self.ordinary_frame, height=32, text="Confirm", command=self.confirm_button_clicked)
        self.btn_confirm.place(x=15, y=140)

        # Download section
        self.dwnd_lbl = ctk.CTkLabel(self.bottom_frame, text="Download picture")
        self.dwnd_lbl.place(x=15, y=10)

        self.btn_download = ctk.CTkButton(self.bottom_frame, height=32, text="Download", command=self.download_images_threaded)
        self.btn_download.place(x=15, y=50)

    def show_image(self, urls):
        col = 0  
        # Ubah start menjadi 1 agar dimulai dari 1
        for x, url in enumerate(urls, start=1):
            response = requests.get(url)
            img_data = response.content
            img = PIL.Image.open(BytesIO(img_data))
            img = img.resize((270, 400))
            img_tk = ImageTk.PhotoImage(img)

            # Mengubah kondisi agar sesuai dengan perpindahan baris baru
            if (x - 1) % 2 == 0 and x != 1:  
                col = 0

            # Menggunakan floor division untuk menentukan baris
            ctk.CTkLabel(self.scrollable_frame, image=img_tk, text="").grid(
                row=(x - 1) // 2, column=col  
            )
            col += 1
    
    def download_image(self, url, save_path=None):
        if not save_path:
            save_path = os.path.join(os.getcwd(), url.split('/')[-1])
        
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Image downloaded and saved as {save_path}")
        else:
            print(f'Failed to download image from {url}')

    def download_images_threaded(self):
        threads = []
        for url in self.urls:
            thread = threading.Thread(target=self.download_image, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def confirm_button_clicked(self):
        self.tags = self.ddown_tags.get()
        self.manypics = self.many_entry.get()

        if not self.manypics:
            self.manypics = 1
        else:
            self.manypics = int(self.manypics)

        anime = AnimeAPI()

        anime.set_parameters([self.tags], '>=2000')
        self.urls = anime.get_image_urls(self.manypics)

        if self.urls:
            self.show_image(self.urls)
    

if __name__ == "__main__":
    cek = MyGUI()
    cek.mainloop()
