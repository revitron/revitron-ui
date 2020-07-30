import revitron 




revitron.DOC.ParameterBindings

e = revitron.Filter().byCategory('Walls').noTypes().byStringEquals('Comments', 'test', True).getElements()


