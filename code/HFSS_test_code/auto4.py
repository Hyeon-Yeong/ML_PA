# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2023.1.1
# 15:59:37  Feb 04, 2024
# ----------------------------------------------
import ScriptEnv

ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("InP_stack_EXAMPLE")
oDesign = oProject.SetActiveDesign("Inverse_Design")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.ImportGDSII(
	[
		"NAME:options",
		"FileName:="		, "/home/local/ace/hy7593/Pixel_2layer_data/gds/TF2_sim=1.gds",
		"FlattenHierarchy:="	, True,
		"ImportMethod:="	, 2,
		[
			"NAME:LayerMap",
			[
				"NAME:LayerMapInfo",
				"LayerNum:="		, 20,
				"DestLayer:="		, "MET3",
				"layer_type:="		, "signal"
			],
			[
				"NAME:LayerMapInfo",
				"LayerNum:="		, 23,
				"DestLayer:="		, "MET4",
				"layer_type:="		, "signal"
			]
		],
		"OrderMap:="		, [			"entry:="		, [				"order:="		, 0,				"layer:="		, "MET3",				"LayerNumber:="		, 20,				"Thickness:="		, 1E-06,				"Elevation:="		, 5E-06,				"Color:="		, "red"],			"entry:="		, [				"order:="		, 1,				"layer:="		, "MET4",				"LayerNumber:="		, 23,				"Thickness:="		, 3E-06,				"Elevation:="		, 7E-06,				"Color:="		, "PINK"]]
	])

unamed_object=oEditor.GetObjectsByMaterial("Not Assigned")

for each_object in unamed_object:
	


	oEditor.ChangeProperty(
			[
				"NAME:AllTabs",
				[
					"NAME:Geometry3DAttributeTab",
					[
						"NAME:PropServers", 
						str(each_object)
					],
					[
						"NAME:ChangedProps",
						[
							"NAME:Material",
							"Value:="		, "\"Au_InP\""
						]
					]
				]
			])



