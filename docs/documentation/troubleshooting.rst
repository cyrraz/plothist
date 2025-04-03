

===============
Troubleshooting
===============

.. _usage-fonts-label:

Font installation
=================

Latin Modern fonts are used by default (Latin Modern Math, Latin Modern Roman, Latin Modern Sans).

The fonts are stored in the |plothist_utils|_, which is a dependency of ``plothist``. The fonts are automatically registered within ``matplotlib`` whenever ``plothist`` is imported in a script.

.. |plothist_utils| replace:: ``plothist_utils`` package
.. _plothist_utils: https://github.com/0ctagon/plothist_utils

If a font is not correctly installed, you can try to install it manually. You can download the fonts from the following links:

- `Latin Modern Math <http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf>`_
- `Latin Modern Roman <https://www.1001fonts.com/download/latin-modern-roman.zip>`_
- `Latin Modern Sans <https://www.1001fonts.com/download/latin-modern-sans.zip>`_

After downloading the fonts, they should be placed in the folder ``~/.fonts/`` for Linux system and ``/Users/your_login_username/Library/Fonts`` for MacOS. If the folder doesn't exist, you can create it by running in a terminal:

.. code-block:: bash

   mkdir ~/.fonts # for Linux
   mkdir /Users/your_login_username/Library/Fonts # for MacOS

Then you can move the downloaded fonts to the folder by running in a terminal:

For Linux:

.. code-block:: bash

   mv path/to/latinmodern-math.otf ~/.fonts/
   unzip -o path/to/latin-modern-roman.zip -d ~/.fonts/latin-modern-roman
   unzip -o path/to/latin-modern-sans.zip -d ~/.fonts/latin-modern-sans

For MacOS:

.. code-block:: bash

   mv path/to/latinmodern-math.otf /Users/your_login_username/Library/Fonts/
   unzip -o path/to/latin-modern-roman.zip -d /Users/your_login_username/Library/Fonts/latin-modern-roman
   unzip -o path/to/latin-modern-sans.zip -d /Users/your_login_username/Library/Fonts/latin-modern-sans

The last step is to delete the cache of matplotlib by running in a python console:

.. code-block:: python

   import matplotlib
   import subprocess
   from pathlib import PosixPath

   cache_files = PosixPath(matplotlib.get_cachedir()).glob("fontlist-v???.json")
   for cache_file in cache_files:
       subprocess.run(["rm", "-v", cache_file])
