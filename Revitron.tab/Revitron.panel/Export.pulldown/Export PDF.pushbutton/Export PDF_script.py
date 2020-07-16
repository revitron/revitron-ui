import revitron
from revitron import _
from rpw.ui.forms import SelectFromList

info = _(revitron.DOC.ProjectInformation)

exporter = revitron.PDFExporter(info.get('Revitron PDF Printer Address'), info.get('Revitron PDF Temporary Output Path'))

sizeParamName = info.get('Revitron Sheet Size Parameter Name')
defaultSize = info.get('Revitron Default Sheet Size')
orientationParamName = info.get('Revitron Sheet Orientation Parameter Name')
defaultOrientation = info.get('Revitron Default Sheet Orientation')

sheetSize = defaultSize
sheetOrientation = defaultOrientation

if sizeParamName:
    sheetSize = _(revitron.ACTIVEVIEW).get(sizeParamName)

if orientationParamName:
    sheetOrientation = _(revitron.ACTIVEVIEW).get(orientationParamName)

exporter.printSheet(revitron.ACTIVEVIEW, sheetSize, defaultOrientation, info.get('Revitron Sheet Export Directory'), info.get('Revitron Sheet Naming Template'))
