# -*- coding: utf-8 -*-
__title__ = "Create Views"
__doc__ = """Version = 1.0
Date    = 03.08.2025
_____________________________________________________________________
Description:
This is a template file for pyRevit Scripts.
_____________________________________________________________________
How-to: (Example)
-> Click on the button
-> Change Settings(optional)
-> Make a change
_____________________________________________________________________
Last update:
- [03.08.2025] - 1.1 UPDATE - New Feature
- [03.08.2025] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
- Check Revit 2021
- Add ... Feature
_____________________________________________________________________
Author: Nicolas Augsburger"""                                           

# pyRevit EXTRA metatags: You can remove them.
__author__ = "Nicolas Augsburger"                               
__helpurl__ = "https://www.linkedin.com/in/nicolasaugsburger/"  

#region Imports: Regular + Autodesk
import os, sys, math, datetime, time                                    
# from Autodesk.Revit.DB import Transaction, FilteredElementCollector
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)

#region Imports: pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

#region Imports: .NET
import clr                                  
clr.AddReference("System")                  
from System.Collections.Generic import List 
# List_example = List[ElementId]()          

#region Variables
doc       = __revit__.ActiveUIDocument.Document   
active_view  = doc.ActiveView
active_level = active_view.GenLevel           


view_types = FilteredElementCollector(doc).OfClass(ViewFamilyType).ToElements()
view_type_plans = [vt for vt in view_types if vt.ViewFamily == ViewFamily.FloorPlan]
floor_plan_type = view_type_plans[0]

view_names = ["PLANTA GENERAL - DISTRIBUCION",
              "PLANTA GENERAL - DISTRIBUCION COTAS",
              "PLANTA GENERAL - PINTURAS",
              "PLANTA GENERAL - MOBILIARIOS",
              "PLANTA GENERAL - PAVIMENTOS Y ZOCALOS",
              "PLANTA GENERAL - TERMINACIONES",
              "PLANTA GENERAL - ILUMINACION",
              "PLANTA GENERAL - CARPINTERIAS Y MESADAS",
              "PLANTA GENERAL - EQUIPAMIENTO Y VEGETACION",
              "PLANTA GENERAL - CIELORRASOS Y ACUSTICOS",
              "PLANTA GENERAL - COORDINACION INGENERIA I",
              "PLANTA GENERAL - COORDINACION INGENIERIA II",
              "PLANTA GENERAL - COORDINACION INGENIERIA III",
              "PLANTA GENERAL - INDICACION I",
              "PLANTA GENERAL - INDICACION II",
              "PLANTA GENERAL - INDICACION III",
              "PLANTA GENERAL - INDICACION IV",
              "PLANTA GENERAL - INDICACION V",
              "PLANTA GENERAL - INDICACION VI",
              ]

with Transaction(doc,'Create Floor Plan') as t:
    t.Start()

    for name in view_names:
        view = ViewPlan.Create(doc, floor_plan_type.Id, active_level.Id)
        view.Name = name

    t.Commit()