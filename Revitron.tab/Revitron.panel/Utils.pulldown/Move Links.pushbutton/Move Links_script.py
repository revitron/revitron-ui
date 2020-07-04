import revitron
from rpw.ui.forms import select_file
from rpw.ui.forms.resources import *

__context__ = 'zerodoc'

def select_folder(title):
    form = Forms.FolderBrowserDialog()
    form.Description = title
    if form.ShowDialog() == Forms.DialogResult.OK:
        return form.SelectedPath

host = select_file('Revit Model (*.rvt)|*.rvt')
source = select_folder('Select source directory for link structure')
target = select_folder('Select target directory for link structure')

print(host)
print('Moving Links ...')
revitron.TransmissionData(host).moveLinksOnDisk(source, target)
print('Done')