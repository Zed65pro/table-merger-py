import pandas as pd
from tkinter import filedialog, messagebox, Toplevel
from tkinter import ttk
import tkinter as tk
from utils import Colors


def load_data(file_path):
    try:
        if file_path.endswith(('.xlsx', '.xls', '.xlsm')):
            file = pd.ExcelFile(file_path)
            sheets = file.sheet_names

            # if there's more than one sheet - prompt the user to select which sheet he wanna use
            if len(sheets) > 1:
                sheet_name = prompt_sheet_selection(sheets)
            else:
                sheet_name = sheets[0]

            if sheet_name:
                return pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                messagebox.showerror('Sheet Error', 'Sheet selection canceled.')
                return None

        # If the file is a CSV type, read it directly with read_csv
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path)

        else:
            if file_path:
                messagebox.showerror('Error', 'Unsupported file format. Please select an Excel or CSV file.')
            return None

    except Exception as e:
        messagebox.showerror('Error', f'Error loading file: {e}')
        return None


def prompt_sheet_selection(sheets):
    # This function basically creates a modal on top of tkinter app - which prompts user to select sheet name and return it
    top = Toplevel(background=Colors.primary_color)
    top.title('Select Sheet')

    label = ttk.Label(top, text='Choose a sheet:')
    label.pack(padx=100, pady=50)

    combo = ttk.Combobox(top, values=sheets, state='readonly')
    combo.pack(padx=20, pady=20)
    combo.current(0)

    selected_sheet = [None]

    def on_ok():
        selected_sheet[0] = combo.get()
        top.destroy()

    ok_button = ttk.Button(top, text='OK', command=on_ok)
    ok_button.pack(padx=10, pady=10)

    top.transient()
    top.grab_set()

    top.wait_window()

    return selected_sheet[0]


def merge_data(master_key, slave_key, remove_duplicates, remove_master_duplicates, remove_slave_duplicates, master_df,
               slave_df, master_columns, slave_columns, join_type):
    if not master_key or not slave_key:
        messagebox.showwarning('Warning', 'Please select keys for merging.')
        return None

    # filter columns based on selection
    selected_master_cols = [col for col, var in master_columns.items() if var.get()]
    selected_slave_cols = [col for col, var in slave_columns.items() if var.get()]

    try:
        if remove_master_duplicates:
            master_df.drop_duplicates(inplace=True)

        if remove_slave_duplicates:
            slave_df.drop_duplicates(inplace=True)

        merged_df = pd.merge(master_df[selected_master_cols],
                             slave_df[selected_slave_cols], left_on=master_key, right_on=slave_key,
                             how=join_type.get())

        if remove_duplicates:
            merged_df.drop_duplicates(inplace=True)

        return merged_df
    except Exception as e:
        messagebox.showerror('Error', f'Error merging data: {e}')
        return None


def merge_and_save(master_key, slave_key, remove_duplicates, remove_master_duplicates, remove_slave_duplicates,
                   master_df, slave_df, master_columns, slave_columns, join_type):
    if master_df is None or slave_df is None:
        messagebox.showwarning('Warning', 'Please load both master and slave files.')
        return

    merged_df = merge_data(master_df=master_df, slave_df=slave_df, master_key=master_key, slave_key=slave_key,
                           slave_columns=slave_columns, master_columns=master_columns,
                           remove_master_duplicates=remove_master_duplicates,
                           remove_slave_duplicates=remove_slave_duplicates, remove_duplicates=remove_duplicates,
                           join_type=join_type)

    if merged_df is None:
        return

    save_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                             filetypes=[('Excel files', '*.xlsx'), ('CSV files', '*.csv')],
                                             title='Save Merged File')
    if save_path:
        try:
            if save_path.endswith('.xlsx'):
                merged_df.to_excel(save_path, index=False)
            elif save_path.endswith('.csv'):
                merged_df.to_csv(save_path, index=False)
            messagebox.showinfo('Success', f'Merged file saved as {save_path}')
        except Exception as e:
            messagebox.showerror('Error', f'Error saving file: {e}')


def select_file(file_entry, combobox, columns_inner_frame, columns_scrollbar):
    file_path = filedialog.askopenfilename(filetypes=[('Excel and CSV files', '*.xlsx *.csv')])
    if not file_path:
        return None
    file_entry.delete(0, tk.END)
    file_entry.insert(0, file_path)

    df = load_data(file_path)
    columns = {}
    if df is not None:
        # Populate combobox with column names
        columns = populate_columns(df=df, columns_inner_frame=columns_inner_frame,
                                   columns_scrollbar=columns_scrollbar)
        combobox.set('')
        combobox['values'] = df.columns.tolist()
        combobox['state'] = 'readonly'
    else:
        for widget in columns_inner_frame.winfo_children():
            widget.destroy()
    return df, columns


def populate_columns(df, columns_inner_frame, columns_scrollbar):
    for widget in columns_inner_frame.winfo_children():
        widget.destroy()

    columns = {}

    for col in df.columns:
        var = tk.BooleanVar(value=True)
        checkbox = ttk.Checkbutton(columns_inner_frame, text=col, variable=var)
        checkbox.pack(anchor='w')
        columns[col] = var

    if df.shape[1] > 0:
        columns_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    return columns
