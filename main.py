from functions import *
from utils import get_app_styles
from widgets import *


class TableMerger:
    def __init__(self, root):
        self.scrollable_frame = self.init_frame(root)

        # Initialize Dataframes
        self.master_df = None
        self.slave_df = None

        # Initialize column variables
        self.master_columns = {}
        self.slave_columns = {}

        # Init style
        self.style = get_app_styles()
        self.create_widgets()

    def init_frame(self, root):
        # Initialize Tkinter root
        root.title("Excel File Merger")
        root.geometry("650x700")
        root.iconbitmap("assets/document.ico")

        # Create a main frame
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas for scrolling
        canvas = tk.Canvas(main_frame, background=Colors.primary_color)
        scrollable_frame = ttk.Frame(canvas)

        # Create a vertical scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Bind the scrollbar to the canvas
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        return scrollable_frame

    def create_widgets(self):
        # Widgets for Master File
        self.master_file_entry = create_file_select_row(text="Master File:", scrollable_frame=self.scrollable_frame,
                                                        function=self.update_master_df_and_columns,
                                                        row=0)

        self.master_key_combobox = create_selection_combobox(text="Select Key from Master:",
                                                             scrollable_frame=self.scrollable_frame, row=1, column=0)

        self.remove_master_duplicates_var = create_checkbox(text="Drop Master Duplicates",
                                                            scrollable_frame=self.scrollable_frame, row=1, column=2)

        self.master_columns_inner_frame, self.master_columns_scrollbar = create_scrollable_columns_frame_row(
            text="Select Columns from Master:", scrollable_frame=self.scrollable_frame, row=2)

        # Widgets for Slave File
        self.slave_file_entry = create_file_select_row(text="Slave File:", scrollable_frame=self.scrollable_frame,
                                                       function=self.update_slave_df_and_columns,
                                                       row=3)

        self.slave_key_combobox = create_selection_combobox(text="Select Key from Slave:",
                                                            scrollable_frame=self.scrollable_frame, row=4, column=0)

        self.remove_slave_duplicates_var = create_checkbox(text="Drop Slave Duplicates",
                                                           scrollable_frame=self.scrollable_frame, row=4, column=2)

        self.slave_columns_inner_frame, self.slave_columns_scrollbar = create_scrollable_columns_frame_row(
            text="Select Columns from Slave:", scrollable_frame=self.scrollable_frame, row=5)

        # Join type selection
        self.join_type_var = create_filled_selection_box(text="Join Type:", scrollable_frame=self.scrollable_frame,
                                                         row=6,
                                                         column=0)

        # Remove duplicates checkbox
        self.remove_duplicates_var = create_checkbox(text="Remove Merged Duplicates",
                                                     scrollable_frame=self.scrollable_frame,
                                                     row=7, column=1)

        # merge btn
        create_button(text="Merge and Save", scrollable_frame=self.scrollable_frame,
                      function=lambda: merge_and_save(master_key=self.master_key_combobox.get(),
                                                      slave_key=self.slave_key_combobox.get(),
                                                      remove_duplicates=self.remove_duplicates_var,
                                                      remove_master_duplicates=self.remove_master_duplicates_var,
                                                      remove_slave_duplicates=self.remove_slave_duplicates_var,
                                                      slave_columns=self.slave_columns,
                                                      master_columns=self.master_columns, master_df=self.master_df,
                                                      slave_df=self.slave_df, join_type=self.join_type_var),
                      row=8, column=1)

    def update_master_df_and_columns(self):
        result = select_file(
            file_entry=self.master_file_entry,
            combobox=self.master_key_combobox,
            columns_inner_frame=self.master_columns_inner_frame,
            columns_scrollbar=self.master_columns_scrollbar)
        if result:
            self.master_df, self.master_columns = result

    def update_slave_df_and_columns(self):
        result = select_file(
            file_entry=self.slave_file_entry,
            combobox=self.slave_key_combobox,
            columns_inner_frame=self.slave_columns_inner_frame,
            columns_scrollbar=self.slave_columns_scrollbar)
        self.slave_df, self.slave_columns = result


if __name__ == "__main__":
    root = tk.Tk()
    app = TableMerger(root)
    root.mainloop()
