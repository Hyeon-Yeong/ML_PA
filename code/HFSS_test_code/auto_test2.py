# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2023.1.1
# 19:07:54  Feb 04, 2024
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
		"Selections:="		, "MET4_391,MET4_392,MET4_393,MET4_394,MET4_395,MET4_396,MET4_397,MET4_398,MET4_399"
	])
