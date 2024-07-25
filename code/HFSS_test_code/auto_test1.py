# ----------------------------------------------
# Script Recorded by Ansys Electronics Desktop Version 2023.1.1
# 19:06:57  Feb 04, 2024
# ----------------------------------------------
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("InP_stack_EXAMPLE")
oDesign = oProject.SetActiveDesign("Inverse_Design")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.Unite(
	[
		"NAME:Selections",
		"Selections:="		, "MET1_1,MET1_2,MET1_3,MET1_4,MET1_5,MET1_6,MET1_8,MET1_9,MET1_10,MET1_12,MET1_13,MET1_14,MET1_16,MET1_17,MET1_18,MET1_20,MET1_21,MET1_22,MET1_23,MET1_24,MET1_25,MET1_26,MET1_27,MET1_28,MET1_29,MET1_30,MET1_31,MET1_32,MET1_33,MET1_36,MET1_53,MET1_54,MET1_55,MET1_56,MET1_57,MET1_58,MET1_59,MET1_60,MET1_61,MET1_62,MET1_63,MET1_65,MET1_66,MET1_67,MET1_69,MET1_70,MET1_71,MET1_73,MET1_74,MET1_75,MET1_77,MET1_78,MET1_79,MET1_80,MET1_81,MET1_82,MET1_83,MET1_84,MET1_85,MET1_86,MET1_87,MET1_88,MET1_89,MET1_90,MET1_93,MET1_110,MET1_111,MET1_112,MET3_69,MET3_70,MET3_71,MET3_72,MET3_73,MET3_74,MET3_75,MET3_76,MET3_77,MET3_78,MET3_79,MET3_80,MET3_81,MET3_83,MET3_84,MET3_86,MET3_87,MET3_88,MET3_89,MET3_90,MET3_91,MET3_92,MET3_93,MET3_94,MET3_95,MET3_96,MET3_97,MET3_98,MET3_99,MET3_100,MET3_101,MET3_102,MET3_103,MET3_104,MET3_105,MET3_106,MET3_107,MET3_108,MET3_109,MET3_110,MET3_113,MET3_114,MET3_116,MET3_117,MET3_119,MET3_120,MET3_121,MET3_122,MET3_123,MET3_124,MET3_125,MET3_126,MET3_127,MET3_128,MET3_129,MET3_130,MET3_131,MET3_132,MET3_133,MET3_134,MET3_135,MET3_136,MET3_137,MET3_138,MET3_140,MET3_141,MET3_143,MET3_144,MET3_145,MET3_146,MET3_147,MET3_148,MET3_149,MET3_150,MET3_151,MET3_152,MET3_153,MET3_154,MET3_155,MET3_156,MET3_157,MET3_158,MET3_159,MET3_160,MET3_161,MET3_162,MET3_163,MET3_164,MET3_165,MET3_166,MET3_167,MET3_170,MET3_171,MET3_173,MET3_174,MET3_176,MET3_177,MET3_178,MET3_179,MET3_180,MET3_181,MET3_182,MET3_183,MET3_184,MET3_185,MET3_186,MET3_187,MET3_188,MET3_189,MET3_190,MET3_191,MET3_192,MET3_193,MET3_194,MET3_195,MET3_197,MET3_198,MET3_200,MET3_201,MET3_202,MET3_203,MET3_204,MET3_205,MET3_206,MET3_207,MET3_208,MET3_209,MET3_210,MET3_211,MET3_212,MET3_213,MET3_214,MET3_215,MET3_216,MET3_217,MET3_218,MET3_219,MET3_220,MET3_221,MET3_222,MET3_223,MET3_224,MET3_227,MET3_228,MET3_229,MET3_230,MET3_231,MET3_232,MET3_233,MET3_234,MET3_235,MET3_236,MET3_237,MET3_238,MET3_239,MET3_240,MET3_241,MET3_242,MET3_243,MET3_244,MET3_245,MET3_246,MET3_247,MET3_248,MET3_249,MET3_250,MET3_251,MET3_252,MET3_253,MET3_254,MET3_255,MET3_256,MET3_257,MET3_258,MET3_259,MET3_260,MET3_261,MET3_262,MET3_263,MET3_264,MET3_265,MET3_266,MET3_267,MET3_268,MET3_269,MET3_270,MET3_271,MET3_272,MET3_273,MET3_274,MET3_275,MET3_276,MET3_277,MET3_278,MET3_279,MET3_280,MET3_281,MET3_282,MET3_283,MET3_284,MET3_285,MET3_286,MET3_287,MET3_288,MET4_273,MET4_274,MET4_275,MET4_276,MET4_277,MET4_278,MET4_279,MET4_280,MET4_281,MET4_282,MET4_283,MET4_284,MET4_285,MET4_286,MET4_287,MET4_288,MET4_289,MET4_290,MET4_291,MET4_292,MET4_293,MET4_294,MET4_295,MET4_296,MET4_297,MET4_298,MET4_299,MET4_300,MET4_301,MET4_302,MET4_303,MET4_304,MET4_305,MET4_306,MET4_307,MET4_308,MET4_309,MET4_310,MET4_311,MET4_312,MET4_313,MET4_314,MET4_315,MET4_316,MET4_317,MET4_318,MET4_319,MET4_320,MET4_321,MET4_322,MET4_323,MET4_324,MET4_325,MET4_326,MET4_327,MET4_328,MET4_329,MET4_330,MET4_331,MET4_332,MET4_333,MET4_334,MET4_335,MET4_336,MET4_337,MET4_338,MET4_339,MET4_340,MET4_341,MET4_342,MET4_343,MET4_344,MET4_345,MET4_346,MET4_347,MET4_348,MET4_349,MET4_350,MET4_351,MET4_352,MET4_353,MET4_354,MET4_355,MET4_356,MET4_357,MET4_358,MET4_359,MET4_360,MET4_361,MET4_362,MET4_363,MET4_364,MET4_365,MET4_366,MET4_367,MET4_368,MET4_369,MET4_370,MET4_371,MET4_372,MET4_373,MET4_374,MET4_375,MET4_376,MET4_377,MET4_378,MET4_379,MET4_380,MET4_381,MET4_382,MET4_383,MET4_384,MET4_385,MET4_386,MET4_387,MET4_388,MET4_389,MET4_390,MET4_391,MET4_392,MET4_393,MET4_394,MET4_395,MET4_396,MET4_397,MET4_398,MET4_399,MET4_400,MET4_401,MET4_402,MET4_403,MET4_404,MET4_405,MET4_406,MET4_407,MET4_408,MET4_409,MET4_410,MET4_411,MET4_412,MET4_413,MET4_414"
	], 
	[
		"NAME:UniteParameters",
		"KeepOriginals:="	, False,
		"TurnOnNBodyBoolean:="	, True
	])
oDesign.Undo()
