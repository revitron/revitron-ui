Installation 
============

The Revitron UI extension requires the `Revitron <https://revitron.readthedocs.io/>`_. library to be installed 
as well as a pyRevit extension. It is possible to install both extensions manually or bundled with a custom 
`fork <https://github.com/revitron/pyRevit>`_ of pyRevit including the project based package manager 
`RPM <https://github.com/revitron/rpm-ui/blob/master/README.md>`_. 
Generally it is recommendend to install the bundled version as described below.

.. attention:: The bundle installer as well as the Revitron package manager are using `Git <https://git-scm.com/>`_ to manage dependencies.
   Please make sure that Git is installed properly on your system before installing Revitron.

Bundle Installer 
----------------

To install the full bundle including pyRevit, Revitron, RPM and the Revitron UI, follow the instructions below:

1. In case Git is not already installed --- `download <https://git-scm.com/download/win>`_ and install Git.
2. Right-click `here <https://raw.githubusercontent.com/revitron/installer/master/install.bat>`_ to download the installer. 
   Make sure it keeps the ``.bat`` extension.
3. Move the ``install.bat`` to the directory, where you want to install pyRevit.
4. Double-click the ``install.bat`` file.
5. Start **Revit**.

Manual Installation
-------------------

The single library and UI packages can be installed using the pyRevit CLI as follows::

    pyrevit extend lib revitron https://github.com/revitron/revitron.git
    pyrevit extend ui revitron https://github.com/revitron/revitron-ui.git

Alternatively the package can also just be cloned with Git as follows::

    cd C:[\path\to\pyrevit]\extensions
    git clone https://github.com/revitron/revitron.git revitron.lib
    git clone https://github.com/revitron/revitron-ui.git revitron-ui.extension
