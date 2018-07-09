# nexcloud_auto_groupfolders

Python script to manage GroupFolders API (https://github.com/nextcloud/groupfolders)

## Example 

```
(env) alex ~$ ipython
Python 3.4.5 (default, Nov  7 2016, 11:43:32) 
Type 'copyright', 'credits' or 'license' for more information
IPython 6.4.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import auto_groupfolders

In [2]: auto_groupfolders._get_all_mount_point()
Out[2]: []

In [3]: element = {'mount_point': 'group_folder'}

In [4]: auto_groupfolders._create_mount_point(element)
[2018-07-09 15:04:50,379] {/home/alex/Documents/nextcloud/auto_groupfolders.py:122} INFO - Create mount_point {'id': '1661', 'groups': [], 'mount_point': 'group_folder'}
INFO:auto_groupfolders:Create mount_point {'id': '1661', 'groups': [], 'mount_point': 'group_folder'}
Out[4]: {'groups': [], 'id': '1661', 'mount_point': 'group_folder'}

In [5]: auto_groupfolders._get_all_mount_point()
Out[5]: [{'groups': [], 'id': '1661', 'mount_point': 'group_folder'}]

In [6]: element = auto_groupfolders._get_mount_point(1661)

In [7]: auto_groupfolders._set_quota_mount_point(element, 1024 * 1024 * 1024)
Out[7]: True

In [8]: auto_groupfolders._set_group_mount_point(element, 'admin')
Out[8]: True

In [9]: auto_groupfolders._get_all_mount_point()
Out[9]: [{'groups': ['admin'], 'id': '1661', 'mount_point': 'group_folder'}]

In [10]: auto_groupfolders._delete_mount_point(element)
[2018-07-09 15:09:33,021] {/home/alex/Documents/nextcloud/auto_groupfolders.py:141} INFO - Delete mount_point group_folder with id 1661
INFO:auto_groupfolders:Delete mount_point group_folder with id 1661
Out[10]: True

In [11]: auto_groupfolders._get_all_mount_point()
Out[11]: []
```
