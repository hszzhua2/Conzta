# -*- coding: utf-8 -*-

from pyrevit.forms import WPFWindow
from System.Windows.Controls import TextBox

class DataContextSample(WPFWindow):
    def __init__(self, xaml_file_name):
        WPFWindow.__init__(self, xaml_file_name)
        self.DataContext = self

    def btn_updatesource_click(self, sender, e):
        binding = self.txtWindowTitle.GetBindingExpression(TextBox.TextProperty)
        binding.UpdateSource()

DataContextSample('wpfbindingsample.xaml').ShowDialog()




