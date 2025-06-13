# -*- coding: utf-8 -*-
__title__ = "Testing"
__author__ = "Nico Augsburger"
__doc__ ="""Version = 1.0
-----------------------------------------------------------------------
Description:
        Este script automatiza la creación de vistas de Assembly en Revit. 
        Genera vistas 3D, planta, elevaciones frontales y secciones laterales con nombres personalizados y aplicando templates específicos.
-----------------------------------------------------------------------
Last update: 
        Junio 2025
"""

import clr
import sys
clr.AddReference("RevitAPI")
clr.AddReference("RevitServices")

import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
from RevitServices.Persistence import *
from RevitServices.Transactions import *
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)

from pyrevit import revit, forms
from Autodesk.Revit.DB import FilteredElementCollector, AssemblyInstance, BuiltInCategory, ElementId
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import AssemblyType

doc = revit.doc

def get_symbol_family_and_type(sym):
    family_name = sym.get_Parameter(DB.BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsValueString()
    type_name = sym.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsValueString()
    joined_name = '{}: {}'.format(family_name, type_name)
    return joined_name

def get_titleblock_type(doc):
    titleblock_types = [e for e in DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType()]
    if titleblock_types == []:
        UI.TaskDialog.Show("Operación cancelada", "No existe ningun Title Block en el Proyecto")
        sys.exit()
    
    titleblock_names = [get_symbol_family_and_type(sym) for sym in titleblock_types]
    titleblock_type_dict = dict(zip(titleblock_names,titleblock_types))

    titleblocks = [Label('Seleccione un Title Block:'), ComboBox('titleblockType', titleblock_type_dict), Separator(), Button('Seleccionar')]
    form = FlexForm('Seleccione un Title Block', titleblocks)
    form.show()
    if not form.values:
        UI.TaskDialog.Show("Operacion cancelada",
                           "No has seleccionado ningun Title Block")
        sys.exit()
    titleblock_type = form.values['titleblockType']
    return titleblock_type

# def get_viewport_type(doc):
    
#     viewport_rule = DB.ParameterFilterRuleFactory.CreateContainsRule(DB.ElementId(DB.BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM),"Viewports",False)
#     viewport_filter = DB.ElementParameterFilter(viewport_rule)
#     viewport_types = DB.FilteredElementCollector(doc) \
#                         .OfClass(DB.ElementType) \
#                         .OfCategory(DB.BuiltInCategory.OST_Viewports) \
#                         .WhereElementIsElementType() \
#                         .WherePasses(viewport_filter) \
#                         .ToElements()
#     print(viewport_types)
    
#     if not viewport_types:
#         UI.TaskDialog.Show("Operación cancelada", "No hay tipos de Viewport en el modelo.")
#         sys.exit()

#     # Mostrar lista con nombre de tipo
#     viewport_type_names = [get_symbol_family_and_type(vp) for vp in viewport_types]
#     viewport_dict = dict(zip(viewport_type_names, viewport_types))

#     form_fields = [Label('Seleccione un tipo de Viewport:'),
#                    ComboBox('viewportType', viewport_dict),
#                    Separator(), Button('Seleccionar')]
    
#     form = FlexForm('Seleccionar Viewport', form_fields)
#     form.show()

#     if not form.values:
#         UI.TaskDialog.Show("Operación cancelada", "No se seleccionó ningún tipo de Viewport.")
#         sys.exit()

#     return form.values['viewportType']

def get_viewport_type(doc):
    # Recolectar todas las instancias de Viewport colocadas en láminas
    viewports = DB.FilteredElementCollector(doc) \
                  .OfClass(DB.Viewport) \
                  .ToElements()

    if not viewports:
        UI.TaskDialog.Show("Operación cancelada", "No hay ningún Viewport en el proyecto.")
        sys.exit()

    # Obtener tipos únicos desde las instancias de Viewport
    viewport_type_elements = []
    for vp in viewports:
        vp_type = doc.GetElement(vp.GetTypeId())
        if vp_type not in viewport_type_elements:
            viewport_type_elements.append(vp_type)

    # Crear diccionario para el formulario
    viewport_type_names = []
    for vt in viewport_type_elements:
        name = get_symbol_family_and_type(vt)
        viewport_type_names.append(name)

    viewport_dict = {}
    for i in range(len(viewport_type_names)):
        viewport_dict[viewport_type_names[i]] = viewport_type_elements[i]

    # Crear y mostrar formulario
    form_fields = [Label('Seleccione un tipo de Viewport:'),
                   ComboBox('viewportType', viewport_dict),
                   Separator(), Button('Seleccionar')]

    form = FlexForm('Seleccionar Viewport', form_fields)
    form.show()

    if not form.values:
        UI.TaskDialog.Show("Operación cancelada", "No se seleccionó ningún tipo de Viewport.")
        sys.exit()

    return form.values['viewportType']


get_titleblock_type(doc)
get_viewport_type(doc)



