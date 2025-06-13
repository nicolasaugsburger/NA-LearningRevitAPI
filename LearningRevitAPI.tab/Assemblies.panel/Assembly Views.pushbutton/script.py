# -*- coding: utf-8 -*-
__title__ = "Assembly Views"
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

from pyrevit import revit, forms
from rpw.ui.forms import (FlexForm, Label, ComboBox, TextBox, Separator, Button, CheckBox)
from Autodesk.Revit.DB import FilteredElementCollector, AssemblyInstance, BuiltInCategory, ElementId
from Autodesk.Revit.DB import Transaction
from Autodesk.Revit.DB import AssemblyType, AssemblyViewUtils, AssemblyDetailViewOrientation

doc = revit.doc

# Diccionario de renombrado
RENAME_RULES = {
    "3D Ortho": "VISTA 3D",
    "Detail Section A": "SECCION A",
    "Detail Section B": "SECCION B",
    "Elevation Back": "ELEVACION TRASERA",
    "Elevation Bottom": "ELEVACION INFERIOR",
    "Elevation Front": "ELEVACION FRONTAL",
    "Elevation Left": "ELEVACION LATERAL IZQ",
    "Elevation Right": "ELEVACION LATERAL DER",
    "Elevation Top": "ELEVACION SUPERIOR",
    "HorizontalDetail": "PLANTA"
}

def get_symbol_family_and_type(sym):
    family_name = sym.get_Parameter(DB.BuiltInParameter.SYMBOL_FAMILY_NAME_PARAM).AsValueString()
    type_name = sym.get_Parameter(DB.BuiltInParameter.ALL_MODEL_TYPE_NAME).AsValueString()
    joined_name = '{}: {}'.format(family_name, type_name)
    return joined_name

def get_titleblock_type(doc):
    titleblock_types = [e for e in DB.FilteredElementCollector(doc).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).WhereElementIsElementType()]
    if titleblock_types == []:
        UI.TaskDialog.Show("Operacion cancelada",
                            "No existe ningun Title Block en el Proyecto")
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

# ------------------------------------------------------------------------------------

# 1. Obtener todos los Assemblies del modelo
assemblies = FilteredElementCollector(doc).OfClass(AssemblyInstance).ToElements()

# 2. Crear lista de nombres para mostrar al usuario
assembly_list = []
for asm in assemblies:
    asm_names = asm.Name
    assembly_list.append(asm.Name)

selected_assembly = forms.SelectFromList.show(
    sorted(assembly_list),
    title="Selecciona un Assembly",
    button_name="Seleccionar")

if not selected_assembly:
    forms.alert("No seleccionaste ningún Assembly", exitscript=True)
else:
    forms.alert("Assembly seleccionado: {}".format(selected_assembly))

# 3. Buscar el Assembly Instance correspondiente al nombre seleccionado

selected_asm_instance = None
for asm in assemblies:
    if asm.Name == selected_assembly:
        selected_asm_instance = asm
        break

if not selected_asm_instance:
    forms.alert("No se encontró el Assembly seleccionado.", exitscript=True)


# 4 Recolectar todos los View Templates disponibles
from Autodesk.Revit.DB import View

view_templates_collector = FilteredElementCollector(doc).OfClass(View).ToElements()
view_templates = [v for v in view_templates_collector if v.IsTemplate]

# 4.1 Lista de nombres para el desplegable

template_names = [v.Name for v in view_templates]

selected_template_name = forms.SelectFromList.show(
    sorted(template_names),
    title="Selecciona un View Template",
    button_name="Aplicar")

if not selected_template_name:
    forms.alert("No seleccionaste ningún View Template", exitscript=True)

# 4.2 Buscar el View Template seleccionado

selected_template = next((v for v in view_templates if v.Name == selected_template_name), None)

if not selected_template:
    forms.alert("No se encontró el View Template seleccionado", exitscript=True)

# 6. Crear vistas del Assembly y renombrarlas

assembly_name = selected_asm_instance.Name
assembly_id = selected_asm_instance.Id

created_views = []

t = Transaction(doc, "Crear vistas del Assembly")
t.Start()

for key, label in RENAME_RULES.items():
    try:
        if key == "3D Ortho":
            view = AssemblyViewUtils.Create3DOrthographic(doc, assembly_id)
        else:
            orientation = getattr(AssemblyDetailViewOrientation, key.replace(" ", ""))
            view = AssemblyViewUtils.CreateDetailSection(doc, assembly_id, orientation)

        view.Name = "{} - {}".format(assembly_name, label)
        view.ViewTemplateId = selected_template.Id
        created_views.append(view.Name)

    except Exception as e:
        forms.alert("No se pudo crear la vista '{}':\n{}".format(key, str(e)))

t.Commit()

forms.alert("Vistas creadas:\n" + "\n".join(created_views))

# # 7. Crear Sheet con el Title Block seleccionado y colocar las vistas
# titleblock_type = get_titleblock_type(doc)
# viewport_type = get_viewport_type(doc)

# sheet_transaction = Transaction(doc, "Crear Sheet y colocar vistas")
# sheet_transaction.Start()

# # Crear el Sheet
# sheet = DB.ViewSheet.Create(doc, titleblock_type.Id)
# sheet.LookupParameter("Sheet Name").Set(assembly_name)

# # Colocar las vistas en el Sheet
# offset_x = 0
# offset_y = 0
# spacing = 0.25  # en pies (~7.5 cm)

# for i, view in enumerate([doc.GetElement(v.Id) for v in view_templates_collector if v.Name in created_views]):
#     try:
#         # Punto base para colocar la vista (puede ajustarse)
#         point = DB.XYZ(offset_x, offset_y - i * spacing, 0)

#         # Crear Viewport en el Sheet
#         viewport = DB.Viewport.Create(doc, sheet.Id, view.Id, point)

#         # Cambiar el tipo de Viewport al seleccionado
#         if viewport_type:
#             viewport.ChangeTypeId(viewport_type.Id)

#     except Exception as e:
#         forms.alert("No se pudo colocar la vista en el Sheet:\n{}".format(str(e)))

# sheet_transaction.Commit()

# forms.alert("Sheet creado y vistas colocadas: {}".format(sheet.Name))
