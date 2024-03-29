# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE


import os
import subprocess
from libqtile import hook
from libqtile import bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import qtile
from qtile_extras import widget
from qtile_extras.widget.decorations import RectDecoration
from qtile_extras.widget.decorations import PowerLineDecoration

mod = "mod4"
terminal = guess_terminal()
home = os.path.expanduser('~')

if qtile.core.name == "x11":
    term = "urxvt"
elif qtile.core.name == "wayland":
    term = "foot"


  
keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h",  lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "x", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key(["control", "mod1"], "delete", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),

    # Volume
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer --decrease 5 -u"), desc="Decrease Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer --increase 5 -u"), desc="Increase Volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle &&"), desc="Toggle Mute"),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause"), desc="Toggle play"),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next"), desc="Next"),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous"), desc="Previous"),

    # Backlight
    Key([], "XF86MonBrightnessUp", lazy.spawn("brillo -u 200000 -A 10; notify-send 'brightness up'"), desc="Brightness up"),
    Key([], "XF86MonBrightnessDown", lazy.spawn("brillo -u 200000 -U 10; notify-send 'brightness down'"), desc="Brightness up"),

    # Custom keybinds
    Key([mod], "F2", lazy.spawn("firefox"), desc="Launch Firefox"),
    Key([mod], "t", lazy.spawn("kitty -b -e nvim"), desc="Launch Neovim"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch rofi"),
    Key([mod], "e", lazy.spawn("Thunar"), desc="Launch Thunar"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod, "shift"], "f", lazy.window.toggle_floating(), desc="Toggle floating"),

    # Flameshot
    Key([], "Print", lazy.spawn("flameshot screen"), desc="Screenshot"),
    Key([mod, "shift"], "s", lazy.spawn("flameshot gui"), desc="Flameshot clip"),

    #Key([mod], "section", lazy.function(switch_monitor), desc="Switch focused monitor"),
    Key([mod], "section", lazy.next_screen(), desc="change focus screen"),
    
    
    # Key([mod], "i", lazy.to_screen(1), desc='Keyboard focus to monitor 2'),

]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=False),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme =  {"border_width": 2,
            "margin": 4,
            "border_focus": "2e9ef4",
            "border_normal": "555555",
            "border_on_single": True
    }    

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    #     layout.Stack(**layout_theme),
     layout.Bsp(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.RatioTile(**layout_theme),
    # layout.Tile(**layout_theme),
    # layout.TreeTab(**layout_theme),
    # layout.VerticalTile(**layout_theme),
    # layout.Zoomy(**layout_theme)
]

widget_defaults = dict(
    #font="JetBrainsMono Nerd Font Medium",
    font="DejaVu Sans Book",
    fontsize=14,
    padding=6,
)
extension_defaults = widget_defaults.copy()

# def longNameParse(text): 
#     for string in ["Brave", "NVIM", "Firefox"]: #Add any other apps that have long names here
#         if string in text:
#             text = string
#         else:
#             text = text
#     return text


APPLICATION_NAME_SUB = {
    "Firefox": "Firefox",
    "NVIM": "Nvim",
    "Visual Studio Code": "VScode",
    "None": "",
}


def replace_window_title(text):
    for key in APPLICATION_NAME_SUB.keys():
        if key in text:
            return APPLICATION_NAME_SUB[key]
    return text




powerline = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_y=0, filled=True, radius=0),
        PowerLineDecoration(path="forward_slash", padding_y=0)
    ]
}

powerline1 = {
    "decorations": [
        RectDecoration(use_widget_background=False, padding_y=0, filled=True, radius=1),
        PowerLineDecoration(path="forward_slash", padding_y=0, shift = 20)
    ]
}

powercurve = {
    "decorations": [
        RectDecoration(use_widget_background=True, padding_y=0, filled=True, radius=0),
        PowerLineDecoration(path="rounded_right", padding_y=0, size = 7 )
    ]
}

#systray = {"decorations": [RectDecoration(colour="#6b6b6b",line_width= 0,radius=1000,filled=True, )],}

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")], padding=0, width=20, scale=1,  **powerline1),
                widget.Image(filename='~/.config/qtile/custom/empty.png', background='#4b4e58', margin_x=-8, **powerline),
                widget.GroupBox(active='#b6b6b6', hide_unused=True, highlight_method="line", highlight_color=['#303030', '#303030'],margin=3, this_current_screen_border='#ffffff', background='#303030', **powerline ),
                widget.Prompt(),
                #widget.WindowName(parse_text=longNameParse),
                # widget.WindowName(foreground='#b6b6b6', parse_text=replace_window_title),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                widget.CheckUpdates(distro='Arch', no_update_string='\uf021', display_format='\uf021', colour_have_updates='#f17884', colour_no_updates='#90d17d', execute="kitty --hold -e sudo pacman -Syu"),
                widget.Wttr(location={'Malmö': 'Malmö'}, format='%c %t %C ' , foreground='#7b9cad'),
                widget.Image(filename='~/.config/qtile/custom/clock.png', background='#1a1e21',),
                widget.Clock(format=" %I:%M %p", foreground='#f17884', background = '#303030'),
                widget.Image(filename='~/.config/qtile/custom/systray.png', background='#303030'),
                widget.Volume(foreground='#90d17d', scroll_interval=0.03, fontsize=14, background = '#303030'),
                widget.Systray(background = '#303030'),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#1a1e21",
            opacity=0.8,
            margin=[0,0,4,0]
        ),

        bottom=bar.Gap(4),
        left=bar.Gap(4),
        right=bar.Gap(4),

    ),
    Screen(
        top=bar.Bar(
            [
                widget.CurrentLayoutIcon(custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")], padding=0, width=20, scale=1,  **powerline1),
                widget.Image(filename='~/.config/qtile/custom/empty.png', background='#4b4e58', margin_x=-8, **powerline),
                widget.GroupBox(active='#b6b6b6', hide_unused=True, highlight_method="line", highlight_color=['#303030', '#303030'],margin=3, this_current_screen_border='#ffffff', background='#303030', **powerline ),
                widget.Prompt(),
                #widget.WindowName(parse_text=longNameParse),
                # widget.WindowName(foreground='#b6b6b6', parse_text=replace_window_title),
                widget.Spacer(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#ff0000", "#ffffff"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                #widget.CheckUpdates(distro='Arch', no_update_string='', colour_have_updates='#d7ff21', execute="kitty --hold -e sudo pacman -Syu"),
                widget.CheckUpdates(distro='Arch', no_update_string='\uf021', display_format='\uf021', colour_have_updates='#f17884', colour_no_updates='#90d17d', execute="kitty --hold -e sudo pacman -Syu"),
                widget.Wttr(location={'Malmö': 'Malmö'}, format='%c %t %C ' , foreground='#7b9cad'),
                widget.Image(filename='~/.config/qtile/custom/clock.png', background='#1a1e21',),
                widget.Clock(format=" %I:%M %p", foreground='#f17884', background = '#303030'),
                widget.Image(filename='~/.config/qtile/custom/systray.png', background='#303030'),
                widget.Volume(foreground='#90d17d', scroll_interval=0.03, fontsize=14, background = '#303030'),
            ],
            24,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#1a1e21",
            opacity=0.8,
            margin=[0,0,4,0]
        ),

        bottom=bar.Gap(4),
        left=bar.Gap(4),
        right=bar.Gap(4),

    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = False
bring_front_click = False
cursor_warp = True
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ],
        border_focus = '#90d17d',
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~')
    subprocess.Popen([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
