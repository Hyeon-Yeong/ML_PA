# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2023.1.1
# 22:26:47  Feb 04, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("InP_stack_EXAMPLE")
oDesign = oProject.SetActiveDesign("Inverse_Design")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.Delete(
	[
		"NAME:Selections",
		"Selections:="		, "MET4_403,MET4_404,MET4_405,MET4_406,MET4_407,MET4_408,MET4_409,MET4_410,MET4_411,MET4_412,MET4_413,MET4_414"
	])
