powerline_iconcwd
=================

A drop in replacement for the stock `cwd` segment in
[powerline](https://github.com/powerline/powerline), which allows for specifying
icons for paths/folders. To add an icon for a path, simply create a hidden file
`.powerline_icon` containing the desired glyphs at that path.

![screenshot](https://github.com/pronobis/powerline_iconcwd/blob/master/screenshot.png)


Installation
------------

The segment can be installed with pip:

```shell
pip install git+https://github.com/pronobis/powerline_iconcwd.git
```

It uses an additional custom highlight group `cwd:icon`. This group must be defined in `.config/powerline/colorschemes/default.json`. A custom color can be defined in `.config/powerline/colors.json`.

For example, to get the result shown in the screenshot, add to `.config/powerline/colorschemes/default.json`:

```json
{
  "groups": {
    "cwd:icon": { "fg": "white", "bg": "iconcwd", "attrs": [] }
  }
}
```

and to `.config/powerline/colors.json`:

```json
{
  "colors": {
    "iconcwd": 96
  }
}
```

The segment uses default icons for the home and root folders (if `.powerline_icon` is not found). To override those, add the following to your default top theme:

```json
{
  "segment_data": {
    "powerline_iconcwd.cwd": {
      "args": {
        "root_icon": "",
        "home_icon": ""
      }
    }
  }
}
```


License
-------

Licensed under [the MIT License](https://github.com/pronobis/powerline_iconcwd/blob/master/LICENSE).
