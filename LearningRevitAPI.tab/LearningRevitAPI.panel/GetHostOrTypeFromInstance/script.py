# -*- coding: utf-8 -*-
from Autodesk.Revit.UI.Selection import ObjectType
from Autodesk.Revit.DB import Part
from pyrevit import revit
from Autodesk.Revit.DB import ElementId, FamilyInstance
from zero11h.newflow.parts import PartsUtils

from pyrevit import revit, DB
from pyrevit.forms import *

uidoc = revit.uidoc
doc = revit.doc
selection = uidoc.Selection

def get_host_from_part(doc, ref):
    host = doc.GetElement(ref.GetSourceElementIds()[0].HostElementId)
    host_type = doc.GetElement(host.GetTypeId())
    # host_name = host_type.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    return host, host_type

def get_type_from_instance(doc, ref):
    instance = doc.GetElement(ref.ElementId)
    type_id = instance.GetTypeId()
    type_element = doc.GetElement(type_id)
    # type_name = type_element.get_Parameter(DB.BuiltInParameter.SYMBOL_NAME_PARAM).AsString()
    return instance, type_element

parts_and_instances = []

selected_refs = selection.PickObjects(ObjectType.Element, "Selecciona una Instancia o una Part")

for ref in selected_refs:
    element = doc.GetElement(ref)
    
    if isinstance(element, Part):
        parts_and_instances.append(get_host_from_part(doc, element))
    
    elif isinstance(element, FamilyInstance):
        parts_and_instances.append(get_type_from_instance(doc, ref))

    else:
        parts_and_instances.append(get_type_from_instance(doc, ref))    

print(parts_and_instances)

