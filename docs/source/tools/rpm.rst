Packages
========

Since the **Revitron** API enables you to easily create specifi extensions for certain projects, you also want to be able to easily 
roll out those extension to your team without individually installing them manually. The **Revitron Package Manager** (RPM)- takes care 
of that.    

Installing Dependencies
-----------------------

The package manager basically lets you define a list of **pyRevit** extensions and stores it in Revitron's 
`Document Config Storage <https://revitron.readthedocs.io/en/latest/revitron.document.html#revitron.document.DocumentConfigStorage>`_.
Since your list of dependencies becomes then part of your Revit model you can just synchronize to ddistribute it to other team members.
To actually load the extension tools, you can hit the **Install Extension** button when needed at any time.

.. container:: .gif

   .. image:: https://i.imgur.com/JVYkHM6.gif

Updating Packages
-----------------

The package manager can also search for available updates automatically. 
When starting Revit, the updater automatically checks for available updates of both --- the pyRevit core and any installed extension. 
In case there updates waiting to be installed they can just be applied with a single click.

.. note::

   The updater shipping with the Revitron UI requires Git to be installed properly on your System in order to pull changes and check for updates. 

In contrast to extension updates, core updates require a shutdown of all running Revit instances to proceed. 
So make sure, all open files are saved! 
It is possible to also check for updated manually at any time hitting the **Check for Updates** button in the RPM panel.