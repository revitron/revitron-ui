Export
======

Export Sheets as PDF
--------------------

Export Sheets as DWG
--------------------

Export Settings
---------------

The export settings control both --- the PDF and the DWG export. Before being able to export sheets from Revit, 
please make sure to configure the main settings correctly as described below.

Sheet Export Directory
	The final output root directory for the exported and correctly named PDFs.

Sheet Naming Template (optional)
	The template for the exported files. 
	Parameter names can be wrapped in ``{}`` and will be substituted 
	with their value on export like ``{Sector}\{Sheet Number}-{Sheet Name}``. 
	Note that the template should not have any extension.
	Defaults to ``{Sheet Number}-{Sheet Name}``.

Sheet Size Parameter Name
	The name of the paramter of the sheet category where a string to define a paper size can be stored. 
	The values should match the paper sizes defined in the PDF printer's configuration like for example ``A4`` or ``A0``.

Default Sheet Size
	The default paper size for all sheets where no value is set for the sheet size paramter.

Sheet Orientation Parameter Name
	The name of the paramter of the sheet category where a string to define a the sheet orientation can be stored.

Default Sheet Orientation (optional)
	The default sheet orientation for all sheets where no value is set for the sheet orientation paramter.
	Defaults to ``Landscape``.

PDF Settings
~~~~~~~~~~~~

To be able to export PDFs, there are two more required settings to be configured. 
Note that the PDF exporter expects a network PDF printer to be running.  

PDF Printer Address	
	The network address of the printer like ``\\server\printer``.

PDF Temporary Output Path	
	The path of the output directory of the network PDF printer. 
	The script will take the incoming PDFs from that location and move it **Sheet Export Directory** (see below).

DWG Settings
~~~~~~~~~~~~

In order to export DWG, the export options for the project have to be defined in the settings.

DWG Export Setup
	The name of the export setup configured in the Revit settings.