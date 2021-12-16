import revitron
from revitron import _
from pyrevit import output

out = output.get_output()

try:
	cloudModelPath = revitron.DOC.GetCloudModelPath()

	modelGuid = cloudModelPath.GetModelGUID()
	projectGuid = cloudModelPath.GetProjectGUID()

	out.print_table([[modelGuid,
	                  projectGuid]],
	                title='Cloud Model Info',
	                columns=['Model GUID',
	                         'Project GUID'])
except:
	out.print_html('<b>The active model is not a cloud model!</b>')
