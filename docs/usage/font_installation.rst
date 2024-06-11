.. _usage-fonts-label:

=================
Font installation
=================

Latin Modern fonts are used by default (Latin Modern Math, Latin Modern Roman, Latin Modern Sans).

On Linux/Ubuntu/MacOS, after installing ``plothist``, you can install the fonts by running on your terminal:

.. code-block:: bash

    install_latin_modern_fonts

Try to restart your python session and run ``import plothist`` again. If no warning is raised, the fonts are installed correctly and you can skip the rest of this section.

Troubleshooting
===============

Command not found
-----------------

If the command doesn't exist, you can run the script manually. First you need to get the folder where ``plothist`` is installed. You can do this by running in a python console:

.. code-block:: python

   import plothist

   plothist.__file__

   # > '/path/to/plothist/__init__.py'

Then you can run the following command in a terminal:

.. code-block:: bash

   python3 /path/to/plothist/scripts/install_latin_modern_fonts.py


Fail to download the fonts
--------------------------

If a font is not correctly installed, you can try to install it manually. You can download the fonts from the following links:

- `Latin Modern Math <http://mirrors.ctan.org/fonts/lm-math/opentype/latinmodern-math.otf>`_
- `Latin Modern Roman <https://www.1001fonts.com/download/latin-modern-roman.zip>`_
- `Latin Modern Sans <https://www.1001fonts.com/download/latin-modern-sans.zip>`_

After downloading the fonts, they should be placed in the folder ``~/.fonts/``. If the folder doesn't exist, you can create it by running in a terminal:

.. code-block:: bash

   mkdir -p ~/.fonts

Then you can move the downloaded fonts to the folder by running in a terminal:

.. code-block:: bash

   mv ~/path/to/latinmodern-math.otf ~/.fonts/
   unzip -o ~/path/to/latin-modern-roman.zip -d ~/.fonts/latin-modern-roman
   unzip -o ~/path/to/latin-modern-sans.zip -d ~/.fonts/latin-modern-sans

The last step is to delete the cache of matplotlib by running in a python console:

.. code-block:: python

   import matplotlib
   import subprocess

   cache_dir = matplotlib.get_cachedir()
   subprocess.run(["rm", "-rv", cache_dir])

Try to restart your python session and run ``import plothist`` again. If no warning is raised, the fonts are installed correctly and you can skip the rest of this section.

Font not used by matplotlib
---------------------------

It was observed in some cases that, after running ``install_latin_modern_fonts``, you may need to move the font files ``latinmodern-math.otf``, ``latin-modern-roman/`` and ``latin-modern-sans/`` from ``~/.fonts/`` into another folder. To get an idea of where the fonts are installed on your system, you can run the following commands in a python console:

.. code-block:: python

   from matplotlib import font_manager

   font_manager.findSystemFonts(fontpaths=None, fontext="ttf")

Make also sure to delete the cache of matplotlib, otherwise the fonts may not be loaded correctly.