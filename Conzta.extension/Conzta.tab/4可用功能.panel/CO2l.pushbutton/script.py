# -*- coding: utf-8 -*-
import os
import System
import clr
import sys

clr.AddReference('ProtoGeometry')
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
clr.AddReference('RevitNodes')
import Revit
clr.AddReference('System.Data')
clr.ImportExtensions(Revit.Elements)
clr.ImportExtensions(Revit.GeometryConversion)
clr.AddReference('RevitAPI')
clr.AddReference('RevitAPIUI')
from System import Type
from System import Type
from System import Array
from System.IO import FileInfo
from Autodesk.Revit import DB, UI
from Autodesk.Revit.DB import FilteredElementCollector as FEC
from System.Collections.Generic import List
from Autodesk.Revit.DB import Architecture as AR
from Autodesk.Revit.UI import Selection as SELolumns

clr.AddReference("DSOffice")
import DSOffice
from DSOffice import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

def unit_conventer(
        doc,
        value,
        to_internal=False,
        unit_type=DB.UnitType.UT_Length,
        number_of_digits=None):
    display_units = doc.GetUnits().GetFormatOptions(unit_type).DisplayUnits
    method = DB.UnitUtils.ConvertToInternalUnits if to_internal \
        else DB.UnitUtils.ConvertFromInternalUnits
    if number_of_digits is None:
        return method(value, display_units)
    elif number_of_digits > 0:
        return round(method(value, display_units), number_of_digits)
    return int(round(method(value, display_units), number_of_digits))

def get_all_solids(element, g_options, solids=None):
    if solids is None:
        solids = []
    if hasattr(element, "Geometry"):
        for item in element.Geometry[g_options]:
            get_all_solids(item, g_options, solids)
    elif isinstance(element, DB.GeometryInstance):
        for item in element.GetInstanceGeometry():
            get_all_solids(item, g_options, solids)
    elif isinstance(element, DB.Solid):
        solids.append(element)
    elif isinstance(element, DB.FamilyInstance):
        for item in element.GetSubComponentIds():
            family_instance = element.Document.GetElement(item)
            get_all_solids(family_instance, g_options, solids)
    return solids

def flatten(element, flat_list=None):
    if flat_list is None:
        flat_list = []
    if hasattr(element, "__iter__"):
        for item in element:
            flatten(item, flat_list)
    else:
        flat_list.append(element)
    return flat_list

def to_list(element, list_type=None):
    if not hasattr(element, '__iter__') or isinstance(element, dict):
        element = [element]
    if list_type is not None:
        if isinstance(element, List[list_type]):
            return element
        if all(isinstance(item, list_type) for item in element):
            typed_list = List[list_type]()
            for item in element:
                typed_list.Add(item)
            return typed_list
    return element

# collecting all elements that have KostenGr. parameter

# list for category elements
categories_filter = List[DB.BuiltInCategory]()
# add categoties to the list
categories_filter.Add(DB.BuiltInCategory.OST_Stairs)
categories_filter.Add(DB.BuiltInCategory.OST_StructuralColumns)
categories_filter.Add(DB.BuiltInCategory.OST_StructuralFoundation)
categories_filter.Add(DB.BuiltInCategory.OST_StructuralFraming)
categories_filter.Add(DB.BuiltInCategory.OST_Walls)
categories_filter.Add(DB.BuiltInCategory.OST_Floors)
categories_filter.Add(DB.BuiltInCategory.OST_Ceilings)
categories_filter.Add(DB.BuiltInCategory.OST_Doors)
categories_filter.Add(DB.BuiltInCategory.OST_Windows)

# create multi category filter
multi_category_filter = DB.ElementMulticategoryFilter(categories_filter)

# list for class elements
class_filter = List[Type]()
# add classes to the list
class_filter.Add(DB.BeamSystem)
# create multi class filter
multi_class_filter = DB.ElementMulticlassFilter(class_filter)

# unite both filters by LogicalOrFilter
or_filter = DB.LogicalOrFilter(
    to_list(
        [
            multi_category_filter,
            multi_class_filter,
        ],
        DB.ElementFilter
    )
)

# filtering elements from project
elements = FEC(doc).WherePasses(or_filter).WhereElementIsNotElementType().ToElements()

filtered_elements_kosten = [doc.GetElement(el.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString() for el in elements]
filtered_elements_Id = [el.Id for el in elements]
filtered_elements_type = [doc.GetElement(el.GetTypeId()) for el in elements]

g_options = DB.Options()

material_rohbau = []
temp = []
# getting element info by Id
for id in filtered_elements_Id:
    # getting element by Id
    element = doc.GetElement(id)
    material_list = []
# families
    if isinstance(element, DB.FamilyInstance):
        # getting solids from elements
        solids = get_all_solids(element, g_options)
        for solid in solids:
            if isinstance(solid, DB.Solid):
                if solid.Volume > 0:
                    material_volume = unit_conventer(doc, solid.Volume, to_internal=False, unit_type=DB.UnitType.UT_Volume)
                    material_area = unit_conventer(doc, solid.SurfaceArea, to_internal=False, unit_type=DB.UnitType.UT_Area)
        # extract materials from solids for windows and doors
                    if element.Category.Id.IntegerValue == int(DB.BuiltInCategory.OST_Windows) or \
                        element.Category.Id.IntegerValue == int(DB.BuiltInCategory.OST_Doors):
                        material_id = doc.GetElement(solid.GraphicsStyleId)
                        if material_id != None:
                            if material_id.GraphicsStyleCategory != None:
                                if material_id.GraphicsStyleCategory.Material != None:
                                    material = material_id.GraphicsStyleCategory.Material.Name
                        material_list.append([material, material_area, material_volume])
        # extract materials from other families
        if element.Category.Id.IntegerValue != int(DB.BuiltInCategory.OST_Windows) or \
                        element.Category.Id.IntegerValue != int(DB.BuiltInCategory.OST_Doors):
        # extracting materials and finishes, structural material applyed to element
            if element.StructuralMaterialId != DB.ElementId(-1):
                material = doc.GetElement(element.StructuralMaterialId).Name
        # extracting materials and finishes, structural material applyed to family type
            elif element.StructuralMaterialId == DB.ElementId(-1) and \
                element.Symbol.Parameter[DB.BuiltInParameter.STRUCTURAL_MATERIAL_PARAM] != None and \
                element.Symbol.Parameter[DB.BuiltInParameter.STRUCTURAL_MATERIAL_PARAM].AsElementId() == DB.ElementId(-1):
                material = []
                material_id = []
                subcategories = element.Category.SubCategories
                for cat in subcategories:
                    if cat.Material != None and cat.Material.Id not in material_id:
                        material_id.append(cat.Material.Id)
                        material.append(cat.Material.Name)
        # extracting materials and finishes, structural material applyed by category
            elif element.StructuralMaterialId == DB.ElementId(-1) and \
                element.Symbol.Parameter[DB.BuiltInParameter.STRUCTURAL_MATERIAL_PARAM] != None and \
                element.Symbol.Parameter[DB.BuiltInParameter.STRUCTURAL_MATERIAL_PARAM].AsElementId() != DB.ElementId(-1):
                material = doc.GetElement(element.Symbol.Parameter[DB.BuiltInParameter.STRUCTURAL_MATERIAL_PARAM].AsElementId()).Name
            material_list.append([material, material_area, material_volume])
        material_rohbau.append(flatten([element, 
                                        material_list, 
                                        doc.GetElement(element.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                        doc.GetElement(element.GetTypeId())]))

# stairs
    elif isinstance(element, AR.Stairs):
        stair_material_id = element.GetMaterialIds(False)
        stair_list = []
        for item in stair_material_id:
            stair_material = doc.GetElement(item).Name
            stair_material_volume = unit_conventer(doc, element.GetMaterialVolume(item), to_internal=False, unit_type=DB.UnitType.UT_Volume)
            stair_material_area = unit_conventer(doc, element.GetMaterialArea(item, False), to_internal=False, unit_type=DB.UnitType.UT_Area)
            stair_list.append([stair_material, stair_material_area, stair_material_volume])
        material_list.append(flatten(stair_list))
        material_rohbau.append(flatten([element, 
                                            material_list, 
                                            doc.GetElement(element.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                            doc.GetElement(element.GetTypeId())]))

# walls and floors
    else:
        if isinstance(element, DB.Floor):
            material_id = element.GetMaterialIds(False)
            for item in material_id:
                material = doc.GetElement(item).Name
                material_volume = unit_conventer(doc, element.GetMaterialVolume(item), to_internal=False, unit_type=DB.UnitType.UT_Volume)
                material_area = unit_conventer(doc, element.GetMaterialArea(item, False), to_internal=False, unit_type=DB.UnitType.UT_Area)
                material_list.append([material, material_area, material_volume])
                material_rohbau.append(flatten([element, 
                                                material_list, 
                                                doc.GetElement(element.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                                doc.GetElement(element.GetTypeId())]))
        elif isinstance(element, DB.Wall):
            if element.CurtainGrid == None:
                material_id = element.GetMaterialIds(False)
                for item in material_id:
                    material = doc.GetElement(item).Name
                    material_volume = unit_conventer(doc, element.GetMaterialVolume(item), to_internal=False, unit_type=DB.UnitType.UT_Volume)
                    material_area = unit_conventer(doc, element.GetMaterialArea(item, False), to_internal=False, unit_type=DB.UnitType.UT_Area)
                    material_list.append([material, material_area, material_volume])
                    material_rohbau.append(flatten([element, 
                                                    material_list, 
                                                    doc.GetElement(element.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                                    doc.GetElement(element.GetTypeId())]))

# structural elements
        else:
            material_id = element.GetMaterialIds(False)
            for item in material_id:
                material = doc.GetElement(item).Name
                material_volume = unit_conventer(doc, element.GetMaterialVolume(item), to_internal=False, unit_type=DB.UnitType.UT_Volume)
                material_area = unit_conventer(doc, element.GetMaterialArea(item, False), to_internal=False, unit_type=DB.UnitType.UT_Area)
                material_list.append([material, material_area, material_volume])

                material_rohbau.append(flatten([element, 
                                                material_list, 
                                                doc.GetElement(element.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                                doc.GetElement(element.GetTypeId())]))

# curtain panells
panels = FEC(doc).OfCategory(DB.BuiltInCategory.OST_CurtainWallPanels).WhereElementIsNotElementType().ToElements()
for panel in panels:
    material_list = []
    solids = get_all_solids(panel, g_options)
    for solid in solids:
        if isinstance(solid, DB.Solid):
            if solid.Volume > 0:
                material_volume = unit_conventer(doc, solid.Volume, to_internal=False, unit_type=DB.UnitType.UT_Volume)
                material_area = unit_conventer(doc, solid.SurfaceArea, to_internal=False, unit_type=DB.UnitType.UT_Area)
                if panel.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM] != None and \
                    panel.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM].AsElementId() != DB.ElementId(-1):
                    panel_material_id = panel.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM].AsElementId()
                    material = doc.GetElement(panel_material_id)
                elif panel.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM] != None and \
                    panel.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM].AsElementId() == DB.ElementId(-1):
                    subcategories = panel.Category.SubCategories
                    for cat in subcategories:
                        if cat.Material != None and cat.Material.Id not in material_id:
                            material_id.append(cat.Material.Id)
                            material.append(cat.Material.Name)
                material_list.append([material, material_area, material_volume])
                material_rohbau.append(flatten([panel, 
                                                material_list, 
                                                doc.GetElement(panel.Host.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                                doc.GetElement(panel.GetTypeId())]))

# mullions
mullions = FEC(doc).OfCategory(DB.BuiltInCategory.OST_CurtainWallMullions).WhereElementIsNotElementType().ToElements()
for mullion in mullions:
    material_list = []
    solids = get_all_solids(mullion, g_options)
    for solid in solids:
        if isinstance(solid, DB.Solid):
            if solid.Volume > 0:
                material_volume = unit_conventer(doc, solid.Volume, to_internal=False, unit_type=DB.UnitType.UT_Volume)
                material_area = unit_conventer(doc, solid.SurfaceArea, to_internal=False, unit_type=DB.UnitType.UT_Area)
                if mullion.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM] != None and \
                    mullion.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM].AsElementId() != DB.ElementId(-1):
                    mullion_material_id = mullion.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM].AsElementId()
                    material = doc.GetElement(mullion_material_id)
                elif mullion.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM] != None and \
                    mullion.Symbol.Parameter[DB.BuiltInParameter.MATERIAL_ID_PARAM].AsElementId() == DB.ElementId(-1):
                    subcategories = mullion.Category.SubCategories
                    for cat in subcategories:
                        if cat.Material != None and cat.Material.Id not in material_id:
                            material_id.append(cat.Material.Id)
                            material.append(cat.Material.Name)
                material_list.append([material.Name, material_area, material_volume])
                material_rohbau.append(flatten([mullion, 
                                                material_list, 
                                                doc.GetElement(mullion.Host.GetTypeId()).Parameter[DB.BuiltInParameter.UNIFORMAT_CODE].AsString(),
                                                doc.GetElement(mullion.GetTypeId())]))


excel_file_path = r'path.xlsx'
# Convert the file path string to a FileInfo object
file_info = System.IO.FileInfo(excel_file_path)
# Import the Excel file
file = DSOffice.Data.ImportExcel(file_info, 'Sheet1', 1, 1)

# calculating CO2

names = []
co2_list = []

for mat_list in material_rohbau:
    gwp = 0
    for calc_list in file:
        for item in mat_list:
            # check if material name is in list
            if calc_list[1] in str(item):
                index = mat_list.index(item)
            # check the calculation method
                if calc_list[2] == 'm3':
                    gwp += float(mat_list[index+2]) * (float(calc_list[4]) + float(calc_list[5]) + float(calc_list[6]))
                elif calc_list[2] == 'kg':
                    gwp += float(mat_list[index+2]) * float(calc_list[3]) * (float(calc_list[4]) + float(calc_list[5]) + float(calc_list[6]))
                elif calc_list[2] == 'm2':
                    gwp += 0
                else:
                    gwp += 0
    co2_list.append(gwp)

for element, number in zip(material_rohbau, co2_list):
    print('{} contributes to the CO2 emissions = {}'.format(element[0].Name, number))
print('*****')
print('Final CO2 emissions = {}'.format(sum(co2_list)))

import pyrevit
from pyrevit import script

output = script.get_output()
# get line chart object
chart = output.make_doughnut_chart()
chart.set_style('height:150px')

chart.options.title = {'display': True,
                       'text':'Chart Title',
                       'fontSize': 18,
                       'fontColor': '#000',
                       'fontStyle': 'bold'}
# this is a list of labels for the X axis of the line graph

# chart.data.labels = ['a','b','c','d','e','f','g', 'k']

chart.data.labels = names

# Let's add the first dataset to the chart object
# we'll give it a name: set_a
set_a = chart.data.new_dataset('set_a')
# And let's add data to it.
# These are the data for the Y axis of the graph
# The data length should match the length of data for the X axis
set_a.data = co2_list
# Set the color for this graph
# set_a.set_color(0xFF, 0x8C, 0x8D, 0.8)
chart.randomize_colors()

chart.draw()
print('Done!')