from Autodesk.Revit.DB import *
from pyrevit import script

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document
output = script.get_output()

#1 Linkify Single - Walls
all_walls = FilteredElementCollector(doc, doc.ActiveView.Id).OfClass(Wall).ToElements()

for wall in all_walls:
    linkify_walls = output.linkify(wall.Id, wall.Name)
    print(linkify_walls)
