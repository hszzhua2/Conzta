using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Autodesk.Revit.UI;
using Autodesk.Revit.DB;
using Autodesk.Revit.UI.Selection;
using Autodesk.Revit.Attributes;


namespace GLSRevitDev
{
    [Autodesk.Revit.Attributes.Transaction(Autodesk.Revit.Attributes.TransactionMode.Manual)]
    public class Lab5CreateWall : IExternalCommand
    {

        public Result Execute(ExternalCommandData commandData, ref string message, ElementSet elements)
        {
            Autodesk.Revit.DB.Document doc = commandData.Application.ActiveUIDocument.Document;
            try
            {
                //选择墙起点终点
                Selection sel = commandData.Application.ActiveUIDocument.Selection;
                XYZ point1 = sel.PickPoint("选择墙的起点");
                XYZ point2 = sel.PickPoint("选择墙的终点");
                //创建墙线
                Line wallLine = Line.CreateBound(point1, point2);
                //得到墙类型
                Element walltype = filterElement(doc, typeof(WallType), "外部 - 带砌块与金属立筋龙骨复合墙");
                WallType wallType = doc.GetElement(walltype.Id) as WallType;
                //得到标高
                Element Level1 = filterElement(doc, typeof(Level), "标高 1");
                Element Level2 = filterElement(doc, typeof(Level), "标高 2");
                Level level1 = doc.GetElement(Level1.Id) as Level;
                Level level2 = doc.GetElement(Level2.Id) as Level;
                //得到墙高度
                double height = level2.Elevation - level1.Elevation;
                //开启事务
                Transaction trans = new Transaction(doc, "创建墙");
                trans.Start();
                //创建墙
                Wall wall = Wall.Create(doc, wallLine, wallType.Id, level1.Id, height, 0, false, false);
                //更新文档
                doc.Regenerate();
                //得到门的位置点
                XYZ doorPoint = (point1 + point2) / 2;
                //得到门类型
                FamilySymbol doolsymbol = filterFamilySymbol(doc, BuiltInCategory.OST_Doors, "0915 x 2134 mm");
                //创建门
                FamilyInstance door = doc.Create.NewFamilyInstance(doorPoint, doolsymbol, wall, level1, Autodesk.Revit.DB.Structure.StructuralType.NonStructural);

                trans.Commit();

            }

            catch (Exception ex)
            {
                return Result.Cancelled;

            }

            return Result.Succeeded;


        }



        /// <summary>
        /// 根据名字和类型得到需要的Element
        /// </summary>
        /// <param name="doc"></param>
        /// <param name="type"></param>
        /// <param name="ElementName"></param>
        /// <returns></returns>
        public Element filterElement(Document doc, Type type, string ElementName)
        {

            FilteredElementCollector collector = new FilteredElementCollector(doc);

            collector.OfClass(type);

            var ElementList = from wt in collector
                              where wt.Name.Equals(ElementName)
                              select wt;
            return ElementList.First();
        }


        /// <summary>
        /// 根据builtincategory和类型名称。得到familySymbol
        /// </summary>
        /// <param name="doc"></param>
        /// <param name="category"></param>
        /// <param name="SymbolName"></param>
        /// <returns></returns>
        public FamilySymbol filterFamilySymbol(Document doc, BuiltInCategory category, string SymbolName)
        {

            FilteredElementCollector collector = new FilteredElementCollector(doc);

            collector.OfCategory(category);

            var ElementList = from wt in collector
                              where wt.Name.Equals(SymbolName)
                              select wt;
            return ElementList.First() as FamilySymbol;
        }
    }
}
