# -*- coding: utf-8 -*-
__title__ = "Collect Types" # Name of the button displayed in Revit UI
__doc__ = "Description of the button" # Description of the button displayed in Revit UI
__author__ = "Nico Augsburger" # Your name
# __helpurl__ = "URL to the documentation" # URL to the documentation
# __highlight__ = "New" # To Revise
# __min_revit_ver__ = 2019 # Minimum Revit version required to run the script
# __max_revit_ver__ = 2024 # Maximum Revit version required to run the script
# __context__ = ['Walls', 'Floors', 'Roofs'] # Make your button available only when certain categories are selected

# IMPORTS

# Regular + Autodesk
import os, sys, math, datetime, time
from Autodesk.Revit.DB import * # Import everything from the Revit API

# pyRevit
from pyrevit import revit, forms

# .NET Imports
import clr
clr.AddReference("System")
from System.Collections.Generic import List # List<ElementType>() <- It is special type of list that RevitAPI often requieres.

# Custom Imports

# VARIABLES
doc = __revit__.ActiveUIDocument.Document # Current Revit document
uidoc = __revit__.ActiveUIDocument # Current Revit UIDocument
app = __revit__.Application # Current Revit application
PATH_SCRIPT = os.path.dirname(__file__) # Path to the script folder

# from pyrevit.revit import uidoc, doc, app # Alternative 

# FUNCTIONS

# CLASSES

# MAIN

def collect_types(doc):
    collector = FilteredElementCollector(doc) \
        .OfCategory(BuiltInCategory.OST_GenericModel) \
        .WhereElementIsNotElementType() \
        .ToElements()

    for e in collector:
        type_id = e.get_Parameter(BuiltInParameter.ELEM_FAMILY_AND_TYPE_PARAM).AsElementId()
        family_type = doc.GetElement(type_id)
        print("ID: {}, Name: {}".format(type_id.IntegerValue, family_type.Name))

        
    
    
        
 

