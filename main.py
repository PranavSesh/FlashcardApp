import time

import customtkinter as ctk
from ctypes import windll
from database import *
from functions import *
from random import sample

FONT_TYPE = 'Helvetica'
USERNAME = 'Your'
BACK_COLOR = '#2a2b29'
BUTTON_HOVER_COLOR = '#858282'


class HomePage:

    def __init__(self, master):
        self.user_packs = get_records(USERNAME)
        self.create_pack_page = None
        self.root = master
        windll.shcore.SetProcessDpiAwareness(1)
        screen_x, screen_y = 1600, 900
        self.root.geometry(f'{screen_x}x{screen_y}')
        self.root.configure(bg=BACK_COLOR)
        self.root.minsize(screen_x, screen_y)
        self.root.maxsize(screen_x, screen_y)
        self.root.title('FastCards')

        self.home_page = tk.Frame(self.root)
        self.home_page.pack(fill=tk.X)
        self.home_page.configure(bg=BACK_COLOR)

        self.top_bar = ctk.CTkFrame(self.home_page,
                                    bg_color=BACK_COLOR,
                                    fg_color=BACK_COLOR)
        self.top_bar.pack(fill=tk.X, pady=25, padx=20)

        ctk.CTkLabel(self.top_bar,
                     text=f"{USERNAME} Packs",
                     bg_color=BACK_COLOR,
                     fg_color=BACK_COLOR,
                     text_color='white',
                     font=(FONT_TYPE, 30)).pack(side=tk.LEFT,
                                                padx=50,
                                                pady=10)

        ctk.CTkButton(self.top_bar,
                      text='Create Pack',
                      height=50,
                      font=(FONT_TYPE, 20, 'bold'),
                      fg_color='#383836',
                      width=150,
                      hover_color=BUTTON_HOVER_COLOR,
                      command=self.create_pack_window).pack(side=tk.RIGHT,
                                                            padx=30)

        self.user_pack_list = ctk.CTkScrollableFrame(self.home_page,
                                                     width=self.home_page.winfo_screenwidth(),
                                                     height=self.home_page.winfo_screenheight(),
                                                     label_text=' ',
                                                     label_anchor='w',
                                                     fg_color=BACK_COLOR)

        self.user_pack_list.pack(padx=10,
                                 pady=5)

        for pack_data in self.user_packs:
            pack_button = PackButton(pack_data, self.user_pack_list, self.root, self.home_page).pack_object
            pack_button.pack(pady=3,
                             fill=tk.X)

    def create_pack_window(self):
        self.home_page.destroy()
        CreatePack(self.root)


class PackButton:

    def __init__(self, pack_info, list_frame, master, page_frame):
        self.root = master
        self.page_frame = page_frame
        self.pack_list_frame = list_frame
        self.pack_id = pack_info[0]
        self.pack_name = pack_info[2]
        self.description = pack_info[3]
        self.pack_cards = pack_info[4]
        self.pack_size = len(card_extractor(self.pack_cards))
        self.pack_object = ctk.CTkButton(list_frame,
                                         text=f'     {self.pack_name}     ||   Cards: {self.pack_size}',
                                         anchor='w',
                                         height=65,
                                         corner_radius=0,
                                         fg_color='#383836',
                                         hover_color=BUTTON_HOVER_COLOR,
                                         font=(FONT_TYPE, 16, 'bold'),
                                         command=self.go_into_pack_window)

    def go_into_pack_window(self):
        self.page_frame.destroy()
        InPack(self.root, self.description, self.pack_id, self.pack_name, self.pack_cards)


class CreatePack:

    def __init__(self, master):
        self.root = master
        self.create_pack_page = tk.Frame(self.root,
                                         bg=BACK_COLOR)

        self.create_pack_page.pack(padx=50,
                                   pady=50,
                                   fill=tk.BOTH,
                                   expand=True)

        name_bar = ctk.CTkFrame(self.create_pack_page,
                                bg_color=BACK_COLOR,
                                fg_color=BACK_COLOR)
        name_bar.pack(padx=5,
                      pady=15,
                      fill=tk.X)

        ctk.CTkLabel(name_bar,
                     text='Name',
                     bg_color=BACK_COLOR,
                     font=(FONT_TYPE, 28, 'bold'),
                     fg_color=BACK_COLOR,
                     text_color='white').pack(side=tk.LEFT,
                                              padx=14)

        name_var = ctk.StringVar(value='New Pack')
        self.pack_name = ctk.CTkEntry(name_bar,
                                      bg_color=BACK_COLOR,
                                      fg_color=BACK_COLOR,
                                      text_color='white',
                                      font=(FONT_TYPE, 30, 'bold'),
                                      textvariable=name_var,
                                      border_width=0)
        self.pack_name.pack(side=tk.LEFT,
                            padx=10,
                            fill=tk.X,
                            expand=True)

        name_var.trace("w", lambda *args: character_limit(name_var, 40))

        self.x_button = ctk.CTkButton(name_bar,
                                      text_color='#878282',
                                      text='X',
                                      fg_color=BACK_COLOR,
                                      hover_color=BACK_COLOR,
                                      font=(FONT_TYPE, 20),
                                      width=10,
                                      command=lambda: name_var.set(''))
        self.x_button.pack(side=tk.RIGHT, padx=15)

        tk.Frame(self.create_pack_page,
                 bg='#4d4c4b',
                 height=1,
                 width=1150).pack(fill=tk.X)

        self.description = ctk.CTkTextbox(self.create_pack_page,
                                          bg_color='transparent',
                                          fg_color='#343632',
                                          height=80,
                                          font=(FONT_TYPE, 18),
                                          text_color='#bfbfbf')
        self.description.insert('0.0', 'Description')
        self.description.pack(padx=15, pady=15, fill=tk.X)

        bottom_bar = ctk.CTkFrame(self.create_pack_page,
                                  bg_color=BACK_COLOR,
                                  fg_color=BACK_COLOR,
                                  height=80)
        bottom_bar.pack(side=tk.BOTTOM,
                        fill=tk.X)

        ctk.CTkButton(bottom_bar,
                      text='Back',
                      height=40,
                      width=60,
                      fg_color=BACK_COLOR,
                      hover_color=BUTTON_HOVER_COLOR,
                      font=(FONT_TYPE, 25, 'bold'),
                      command=self.back_to_homepage).pack(padx=5,
                                                          side=tk.LEFT)

        saved_label = ctk.CTkLabel(bottom_bar,
                                   text='Pack Created',
                                   text_color='green',
                                   font=('Sans', 15),
                                   bg_color='transparent')

        self.save_button = ctk.CTkButton(bottom_bar,
                                         text='Save',
                                         height=40,
                                         width=60,
                                         fg_color=BACK_COLOR,
                                         hover_color=BUTTON_HOVER_COLOR,
                                         font=(FONT_TYPE, 25, 'bold'),
                                         command=lambda: add_record([USERNAME,
                                                                     self.pack_name.get(),
                                                                     self.description.get('1.0', 'end-1c'),
                                                                     None], saved_label,
                                                                    self.save_button,
                                                                    self.pack_name,
                                                                    self.description,
                                                                    self.x_button))

        self.save_button.pack(padx=5, side=tk.RIGHT)

    def back_to_homepage(self):
        self.create_pack_page.destroy()
        HomePage(self.root)


class Card:

    def __init__(self, front, back, front_box, back_box):
        self.front_box = front_box
        self.back_box = back_box

        self.front_initial = front
        self.back_initial = back

    def update(self):
        try:
            self.front_initial = self.front_box.get('1.0', 'end-1c')
            self.back_initial = self.back_box.get('1.0', 'end-1c')
        except Exception as e:
            print(e)


class InPack:
    def __init__(self, master, description, pack_id, pack_name, pack_cards):
        self.root = master
        self.pack_id: int = pack_id
        self.pack_name: str = pack_name
        self.pack_description: str = description
        self.pack_cards = pack_cards
        self.current_cards_list: list[tuple[str, str]] = card_extractor(pack_cards)
        self.current_cards_obj: list[Card] = []
        self.pack_page: tk.Frame = tk.Frame(self.root, bg=BACK_COLOR)

        self.top_bar = tk.Frame(self.pack_page,
                                height=60,
                                width=50,
                                bg=BACK_COLOR)
        self.top_bar.pack(fill=tk.BOTH)

        self.name_var = tk.StringVar(value=pack_name)
        name = ctk.CTkEntry(self.top_bar,
                            textvariable=self.name_var,
                            bg_color=BACK_COLOR,
                            fg_color=BACK_COLOR,
                            text_color='white',
                            border_width=0,
                            font=(FONT_TYPE, 33))
        name.pack(side=tk.LEFT, padx=20, pady=10, fill=tk.X, expand=True)
        self.name_var.trace("w", lambda *args: character_limit(self.name_var, 40))

        ctk.CTkButton(self.top_bar,
                      text_color='white',
                      text='Delete Pack',
                      height=20,
                      fg_color='#c9363e',
                      hover_color=BUTTON_HOVER_COLOR,
                      font=(FONT_TYPE, 25, 'bold'),
                      width=10,
                      command=self.delete_pack).pack(side=tk.RIGHT, padx=20)

        tk.Frame(self.pack_page,
                 bg='#4d4c4b',
                 height=3,
                 width=1150).pack(fill=tk.X,
                                  pady=5)

        description_bar = tk.Frame(self.pack_page,
                                   bg=BACK_COLOR)
        description_bar.pack(fill=tk.X)

        self.description_box = ctk.CTkTextbox(description_bar,
                                              bg_color='transparent',
                                              fg_color='transparent',
                                              height=80,
                                              font=(FONT_TYPE, 18),
                                              text_color='#bfbfbf')
        self.description_box.insert('0.0', description)
        self.description_box.pack(padx=15, pady=5, fill=tk.X, side=tk.LEFT, expand=True)

        ctk.CTkButton(description_bar,
                      text_color='white',
                      text=' + ',
                      height=0,
                      fg_color='transparent',
                      hover_color=BUTTON_HOVER_COLOR,
                      font=(FONT_TYPE, 50, 'bold'),
                      width=15,
                      command=self.construct_card).pack(side=tk.RIGHT, padx=45)

        self.pack_list = ctk.CTkScrollableFrame(self.pack_page,
                                                label_anchor='w',
                                                label_text=f' ',
                                                orientation='horizontal',
                                                height=220)

        for card in self.current_cards_list:
            self.construct_card(front=card[0], back=card[1])
        else:
            self.pack_page.pack(padx=30,
                                pady=30,
                                fill=tk.BOTH,
                                expand=True)
            self.pack_list.pack(padx=20, pady=10, fill=tk.X)

        self.bottom_bar = tk.Frame(self.pack_page,
                                   bg=BACK_COLOR)

        self.bottom_bar.pack(fill=tk.X, expand=True)

        ctk.CTkButton(self.bottom_bar,
                      text='Back',
                      height=40,
                      width=60,
                      fg_color=BACK_COLOR,
                      hover_color=BUTTON_HOVER_COLOR,
                      font=(FONT_TYPE, 25, 'bold'),
                      command=self.back_to_homepage).pack(padx=20,
                                                          side=tk.LEFT)

        ctk.CTkButton(self.bottom_bar,
                      text='Review',
                      height=40,
                      width=60,
                      fg_color=BACK_COLOR,
                      hover_color=BUTTON_HOVER_COLOR,
                      command=self.go_to_review,
                      font=(FONT_TYPE, 25, 'bold')).pack(padx=20, side=tk.RIGHT)

        ctk.CTkButton(self.bottom_bar,
                      text='Save',
                      height=40,
                      width=60,
                      fg_color=BACK_COLOR,
                      hover_color=BUTTON_HOVER_COLOR,
                      font=(FONT_TYPE, 25, 'bold'),
                      command=self.save_changes).pack(padx=20, side=tk.RIGHT)

    def go_to_review(self):
        if len(self.current_cards_obj):
            self.pack_page.destroy()
            card_count = 10 if len(self.current_cards_obj) >= 10 else len(self.current_cards_obj)
            review_set = sample(self.current_cards_obj, k=card_count)
            Review(self.root, review_set, (self.pack_description, self.pack_id, self.pack_name,
                                           card_compressor(card_class_to_list(self.current_cards_obj))))

    def back_to_homepage(self):
        self.pack_page.destroy()
        HomePage(self.root)

    def delete_pack(self):
        remove_record(self.pack_id)
        self.back_to_homepage()

    def save_changes(self):
        self.pack_name = self.name_var.get()
        self.pack_description = self.description_box.get('1.0', 'end-1c')
        for card in self.current_cards_obj: card.update()
        update_record(self.pack_id, self.pack_name, self.pack_description, self.current_cards_obj)

    def construct_card(self, front='front', back='back'):
        front_box, back_box = self.display_card(front, back, self.pack_list)
        self.current_cards_obj.append(Card(front, back, front_box, back_box))

    def remove_card(self, front_box, back_box, frame):
        check_key = "".join([front_box.get('1.0', 'end-1c'), back_box.get('1.0', 'end-1c')])
        for current_card in self.current_cards_obj:
            current_card.update()
            key = "".join([current_card.front_initial, current_card.back_initial])
            if check_key == key:
                self.current_cards_obj.remove(current_card)
                frame.destroy()
                break

    def display_card(self, front, back, pack_list):
        card_frame = tk.Frame(pack_list,
                              width=350,
                              height=350,
                              bg='#696b68',
                              borderwidth=3)
        card_frame.pack(side=tk.RIGHT, padx=16, fill=tk.Y)

        front_box = ctk.CTkTextbox(card_frame,
                                   height=90,
                                   fg_color='#4f4f4e',
                                   corner_radius=0,
                                   font=('Sans', 15))
        front_box.pack(fill=tk.Y, expand=True)
        front_box.insert('0.0', front)

        ctk.CTkButton(card_frame,
                      text='X',
                      fg_color='#c9363e',
                      hover_color=BUTTON_HOVER_COLOR,
                      height=1,
                      width=20,
                      font=(FONT_TYPE, 10),
                      command=lambda: self.remove_card(front_box,
                                                       back_box,
                                                       card_frame)).pack(pady=5)

        back_box = ctk.CTkTextbox(card_frame,
                                  height=90,
                                  fg_color='#4f4f4e',
                                  corner_radius=0,
                                  font=('Sans', 15))
        back_box.pack(fill=tk.Y, expand=True)
        back_box.insert('0.0', back)

        return front_box, back_box


class Review:
    def __init__(self, master, review_cards, extra_datas):
        self.root = master
        self.pass_through = extra_datas
        self.card_set: list[Card] = review_cards
        self.review_page = tk.Frame(self.root, bg=BACK_COLOR)
        self.review_page.pack(fill=tk.BOTH, expand=True)
        self.display()

    def display(self, front=True):
        tk.Frame(self.review_page,
                 bg=BACK_COLOR,
                 height=2,
                 width=1150).pack(fill=tk.X,
                                  pady=4,
                                  side=tk.BOTTOM)

        button_state = 'Flip'
        display_side = self.card_set[0].front_initial
        if not front:
            button_state = 'Next'
            display_side = self.card_set[0].back_initial
            self.card_set.pop(0)

        flip_button = ctk.CTkButton(self.review_page,
                                    text=button_state,
                                    height=40,
                                    width=60,
                                    fg_color='transparent',
                                    hover_color=BUTTON_HOVER_COLOR,
                                    corner_radius=0,
                                    font=(FONT_TYPE, 25, 'bold'),
                                    command=lambda: self.switch_display(front))
        flip_button.pack(pady=0, side=tk.BOTTOM, fill=tk.X)

        tk.Frame(self.review_page,
                 bg='#4d4c4b',
                 height=2,
                 width=1150).pack(fill=tk.X,
                                  pady=0,
                                  side=tk.BOTTOM)

        prompt_box = ctk.CTkLabel(self.review_page,
                                  text=display_side,
                                  text_color='white',
                                  font=(FONT_TYPE, 20),
                                  bg_color='transparent')
        prompt_box.pack(fill=tk.X, padx=30, pady=170, side=tk.TOP)

    def switch_display(self, front):
        self.review_page.destroy()
        if len(self.card_set):
            self.review_page = tk.Frame(self.root, bg=BACK_COLOR)
            self.review_page.pack(fill=tk.BOTH, expand=True)
            self.display(not front)
        else:
            InPack(self.root, *self.pass_through)


if __name__ == '__main__':
    root = tk.Tk()
    HomePage(root)
    root.mainloop()




