import revitron
from revitron import _
from pyrevit import output

out = output.get_output()

try:
	cloudModelPath = revitron.DOC.GetCloudModelPath()

	modelGuid = cloudModelPath.GetModelGUID()
	projectGuid = cloudModelPath.GetProjectGUID()
	try:
		region = cloudModelPath.Region
	except:
		region = ''

	out.print_table([[modelGuid,
	                  projectGuid,
	                  region]],
	                title='Cloud Model Info',
	                columns=['Model GUID',
	                         'Project GUID',
	                         'Region'])
except:
	out.print_html('<b>The active model is not a cloud model!</b>')
