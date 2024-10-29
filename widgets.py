from tkinter import ttk
import tkinter as tk

from utils import Colors


def create_file_select_row(text, scrollable_frame, function, row):
    ttk.Label(scrollable_frame, text=text).grid(row=row, column=0, padx=10, pady=10, sticky='w')
    file_entry = ttk.Entry(scrollable_frame, width=40)
    file_entry.grid(row=row, column=1, padx=10, pady=10)
    browse_btn = ttk.Button(scrollable_frame, text='Browse', command=function)
    browse_btn.grid(row=row, column=2, padx=10, pady=10)

    return file_entry


def create_selection_combobox(text, scrollable_frame, row, column):
    ttk.Label(scrollable_frame, text=text).grid(row=row, column=column, padx=10, pady=10,
                                                sticky='w')
    key_combobox = ttk.Combobox(scrollable_frame, state='disabled')
    key_combobox.grid(row=row, column=column + 1, padx=10, pady=10, sticky='w')
    return key_combobox


def create_checkbox(text, scrollable_frame, row, column):
    checkbox_var = tk.BooleanVar()
    remove_master_duplicates_checkbox = ttk.Checkbutton(scrollable_frame, text=text,
                                                        variable=checkbox_var)
    remove_master_duplicates_checkbox.grid(row=row, column=column, padx=10, pady=10, sticky='w')
    return checkbox_var


def create_scrollable_columns_frame_row(text, scrollable_frame, row):
    ttk.Label(scrollable_frame, text=text).grid(row=row, column=0, padx=10, pady=10,
                                                sticky='w')
    columns_frame = ttk.Frame(scrollable_frame)
    columns_frame.grid(row=row, column=1, padx=10, pady=10, sticky='w')

    # Create scrollable frame for master columns
    columns_canvas = tk.Canvas(columns_frame, background=Colors.primary_color, width=150,
                               height=150)
    columns_scrollbar = ttk.Scrollbar(columns_frame, orient='vertical',
                                      command=columns_canvas.yview)
    columns_inner_frame = ttk.Frame(columns_canvas)

    columns_inner_frame.bind('<Configure>', lambda e: columns_canvas.configure(
        scrollregion=columns_canvas.bbox('all')))
    columns_canvas.create_window((0, 0), window=columns_inner_frame, anchor='nw')
    columns_canvas.configure(yscrollcommand=columns_scrollbar.set)

    columns_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    columns_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    return columns_inner_frame, columns_scrollbar


def create_filled_selection_box(text, scrollable_frame, row, column):
    ttk.Label(scrollable_frame, text=text).grid(row=row, column=column, padx=10, pady=10, sticky='w')
    selected_var = tk.StringVar(value='inner')
    menu = ttk.Combobox(scrollable_frame, textvariable=selected_var,
                        values=['inner', 'left', 'right', 'outer'])
    menu.grid(row=row, column=column + 1, padx=10, pady=10, sticky='w')
    return selected_var


def create_button(text, scrollable_frame, function, row, column):
    merge_btn = ttk.Button(scrollable_frame, text=text, command=function)
    merge_btn.grid(row=row, column=column, padx=10, pady=20)
