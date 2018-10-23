# vim:fileencoding=utf-8:noet
from __future__ import (unicode_literals, division, absolute_import, print_function)

import os

from powerline.theme import requires_segment_info
from powerline.segments import Segment, with_docstring
from powerline.lib.unicode import out_u


@requires_segment_info
class IconCwdSegment(Segment):

    def __call__(self, pl, segment_info,
                 dir_shorten_len=None,
                 dir_limit_depth=None,
                 use_path_separator=False,
                 ellipsis='...',
                 default_icon='🖿',
                 home_icon='⌂',
                 root_icon='/',
                 ** kwargs):
        def get_icon(icon_path):
            icon_file = os.path.join(icon_path, '.powerline_icon')
            if os.path.isfile(icon_file):
                try:
                    with open(icon_file, 'r') as f:
                        icon = f.readline().strip('\n')
                        if not icon:
                            icon = default_icon
                        return (icon_path, icon)
                except PermissionError:
                    return (icon_path, default_icon)
            elif icon_path == home:
                return (icon_path, home_icon)
            else:
                return (os.path.dirname(icon_path), root_icon)

        try:
            path = out_u(segment_info['getcwd']())
        except OSError as e:
            path = ""
        home = segment_info['home']
        # Find icon file
        icon_path = path
        new_icon_path, icon = get_icon(icon_path)
        while new_icon_path != icon_path:
            icon_path = new_icon_path
            new_icon_path, icon = get_icon(icon_path)
        # Update path
        if icon_path[-1] != os.sep:
            icon_path = icon_path + os.sep
        path = path[len(icon_path):]
        # Process updated path
        cwd_split = path.split(os.sep)
        cwd_split_len = len(cwd_split)
        cwd = [i[0:dir_shorten_len] if dir_shorten_len and i else i for i in cwd_split[:-1]] + [cwd_split[-1]]
        if dir_limit_depth and cwd_split_len > dir_limit_depth + 1:
            del(cwd[0:-dir_limit_depth])
            if ellipsis is not None:
                cwd.insert(0, ellipsis)
        # Add icon
        ret = [{
            'contents': icon,
            'highlight_groups': ['cwd:icon']
        }]
        # Add parts for path
        if cwd[0]:
            draw_inner_divider = not use_path_separator
            for part in cwd:
                if not part:
                    continue
                if use_path_separator:
                    part += os.sep
                ret.append({
                    'contents': part,
                    'divider_highlight_group': 'cwd:divider',
                    'draw_inner_divider': draw_inner_divider,
                })
            ret[-1]['highlight_groups'] = ['cwd:current_folder', 'cwd']
            if use_path_separator:
                ret[-1]['contents'] = ret[-1]['contents'][:-1]
                if len(ret) > 1 and ret[0]['contents'][0] == os.sep:
                    ret[0]['contents'] = ret[0]['contents'][1:]
        return ret


cwd = with_docstring(IconCwdSegment(),
                     '''Return the current working directory.

Returns a segment list to create a breadcrumb-like effect.

:param int dir_shorten_len:
	shorten parent directory names to this length (e.g. 
	:file:`/long/path/to/powerline` → :file:`/l/p/t/powerline`)
:param int dir_limit_depth:
	limit directory depth to this number (e.g. 
	:file:`/long/path/to/powerline` → :file:`⋯/to/powerline`)
:param bool use_path_separator:
	Use path separator in place of soft divider.
:param str ellipsis:
	Specifies what to use in place of omitted directories. Use None to not 
	show this subsegment at all.
:param str default_icon:
	Icon used when .powerline_icon file is empty or inaccessible.
:param str home_icon:
	Icon used for the home directory.
:param str root_icon:
	Icon used for the file system root.

Divider highlight group used: ``cwd:divider``.

Highlight groups used: ``cwd:icon`` ``cwd:current_folder`` or ``cwd``. It is recommended to define all highlight groups.
''')
