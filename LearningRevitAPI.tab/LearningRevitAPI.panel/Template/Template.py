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
Author: Nicolas Augsburger"""                                           # Button Description shown in Revit UI

# pyRevit EXTRA metatags: You can remove them.
__author__ = "Nicolas Augsburger"                               # Script's Author
__helpurl__ = "https://www.linkedin.com/in/nicolasaugsburger/"  # Link that can be opened with F1 when hovered over the tool in Revit UI.
# __highlight__ = "new"                                         # Button will have an orange dot + Description in Revit UI
__min_revit_ver__ = 2020                                        # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
__max_revit_ver = 2025                                          # Limit your Scripts to certain Revit versions if it's not compatible due to RevitAPI Changes.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.
# __context__     = ['Walls', 'Floors', 'Roofs']                # Make your button available only when certain categories are selected. Or Revit/View Types.
# Docs Link: https://pyrevitlabs.notion.site/Anatomy-of-IronPython-Scripts-f11d0099667f46a28d29b028dd99ccaf

#region Imports
# Regular + Autodesk
import os, sys, math, datetime, time                                    # Regular Imports
# from Autodesk.Revit.DB import Transaction, FilteredElementCollector   # or Import only classes that are used.
from Autodesk.Revit.DB.Architecture import Room, TopographySurface      # Import Discipline Specific Elements
from Autodesk.Revit.DB import *                                         # Import everything from DB (Very good for beginners)

# pyRevit
from pyrevit import revit, forms                                        # import pyRevit modules. (Lots of useful features)

# Custom Imports
from Snippets._selection import get_selected_elements                   # lib import
from Snippets._convert   import convert_internal_to_m                   # lib import

# .NET Imports
import clr                                  # Common Language Runtime. Makes .NET libraries accessinble
clr.AddReference("System")                  # Refference System.dll for import.
from System.Collections.Generic import List # List<ElementType>() <- it's special type of list from .NET framework that RevitAPI requires
# List_example = List[ElementId]()          # use .Add() instead of append or put python list of ElementIds in parentesis.

#region Variables
doc       = __revit__.ActiveUIDocument.Document   #type: UIDocument     # Document   class from RevitAPI that represents project. Used to Create, Delete, Modify and Query elements from the project.
uidoc     = __revit__.ActiveUIDocument            #type: Document       # UIDocument class from RevitAPI that represents Revit project opened in the Revit UI.
selection = uidoc.Selection                       #type: Selection
app       = __revit__.Application                 #type: UIApplication  # Represents the Autodesk Revit Application, providing access to documents, options and other application wide data and settings.
rvt_year  = int(app.VersionNumber)                # e.g. 2023

active_view  = doc.ActiveView
active_level = active_view.GenLevel           # Only FloorPlans are associated with a Level!
PATH_SCRIPT  = os.path.dirname(__file__)      # Absolute path to the folder where script is placed.

# GLOBAL VARIABLES

# - Place global variables here.

#region Functions

# - Place local functions here. If you might use any functions in other scripts, consider placing it in the lib folder.

#region Classes

# - Place local classes here. If you might use any classes in other scripts, consider placing it in the lib folder.

#region Main
if __name__ == '__main__':
    # START CODE HERE

    # AVOID  placing Transaction inside of your loops! It will drastically reduce perfomance of your script.
    t = Transaction(doc,__title__)  # Transactions are context-like objects that guard any changes made to a Revit model.

    # You need to use t.Start() and t.Commit() to make changes to a Project.
    t.Start()  # <- Transaction Start

    #- CHANGES TO REVIT PROJECT HERE

    t.Commit()  # <- Transaction End

    # Notify user that script is complete.
    print('-' * 50)
    print('Script is finished.')
    print('Template has been developed by Nico Augsburger.')