Export
======

Export PDF
----------



Configure PDF Export
--------------------



PDF Printer Address	
	The network address of the printer like ``\\server\printer``.

PDF Temporary Output Path	
	The path of the output directory of the network PDF printer. 
	The script will take the incoming PDFs from that location and move it **Sheet Export Directory** (see below).

Sheet Export Directory
	The final output root directory for the exported and correctly named PDFs.

Sheet Naming Template
	The template for the exported files. 
	Parameter names can be wrapped in ``{}`` and will be substituted 
	with their value on export like ``{Sector}\{Sheet Number}-{Sheet Name}``. 
	Note that the template should not have any extension.

Sheet Size Parameter Name
	The name of the paramter of the sheet category where a string to define a paper size can be stored. 
	The values should match the paper sizes defined in the PDF printer's configuration like for example ``A4`` or ``A0``.

Default Sheet Size
	The default paper size for all sheets where no value is set for the sheet size paramter.

Sheet Orientation Parameter Name
	The name of the paramter of the sheet category where a string to define a the sheet Orientation can be stored.
	The values can be either ``Landscape`` or ``Portrait``.

Default Sheet Orientation
	The default sheet orientation for all sheets where no value is set for the sheet orientation paramter.

	