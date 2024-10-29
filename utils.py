from tkinter import ttk


class Colors:
    primary_color = '#ffffff'
    primary_hover_color = '#f0e9e9'
    primary_foreground_color = '#000000'


def get_app_styles():
    style = ttk.Style()

    style.configure('TFrame', background=Colors.primary_color)
    style.configure('TLabel', background=Colors.primary_color, foreground=Colors.primary_foreground_color)

    style.map('TButton', background=[('active', Colors.primary_hover_color)],
              foreground=[('active', Colors.primary_foreground_color)])
    style.configure('TButton', background=Colors.primary_hover_color, foreground=Colors.primary_foreground_color,
                    borderwidth=0)

    style.map('TCheckbutton', background=[('active', Colors.primary_hover_color)],
              foreground=[('active', Colors.primary_foreground_color)])
    style.configure('TCheckbutton', background=Colors.primary_color, foreground=Colors.primary_foreground_color,
                    indicatorcolor=Colors.primary_foreground_color)
    return style
