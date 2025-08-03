# -*- coding: utf-8 -*-
__title__ = "Nico Augsburger Template"
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


view_types = FilteredElementCollecto(doc).OfClass(ViewFamilyType).ToElements()
print(view_types)