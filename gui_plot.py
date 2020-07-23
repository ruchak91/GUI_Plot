######################################################
#
#              program developed by
#               Ruchita Korgaonkar
#                  PhD student
#                Electrical Engg
#                  IIT Bombay
#                  July 2020
# under the guidance of Prof. M.B.Patil and Prof.K.Appaiah
# 
######################################################
import sys
import time
import numpy as np
import csv
import matplotlib
import matplotlib.pylab as plt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import (
        QApplication, QWidget, QLabel, QPushButton, QRadioButton, QFrame, QMenu,QAction,QScrollArea,
        QLineEdit,QFileDialog,QComboBox,QMainWindow,QSizePolicy,QVBoxLayout,QListWidget,QCheckBox,
       QListWidgetItem,QAbstractItemView,QHBoxLayout,QColorDialog, QPlainTextEdit
    )
import numpy as np
import random
from matplotlib.backends.qt_compat import QtCore, QtWidgets, is_pyqt5
if is_pyqt5():
    print('QT5')
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    print('Qt4')
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

class NavigationToolbar(NavigationToolbar):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

                 
class ScriptObject(QWidget):
    """
    class to create Window of generated python script(to create plot)
    and option to save the script
    """
    def __init__(self):
        super().__init__()
        self.title = "generatePlot.py"
        self.InitWindow()
 
 
    def InitWindow(self):
        self.setWindowTitle(self.title)
        vbox = QVBoxLayout()
        self.frame16 = QFrame(self)
        self.frame16.setGeometry(QRect(1,1,100,25))
        self.saveBtn = QPushButton("Save Script",self.frame16)
        vbox.addWidget(self.saveBtn)
        self.saveBtn.clicked.connect(self.openFileSaveDialog)
        self.saveBtn.setEnabled(1)
	
        self.frame1 = QFrame(self);self.frame1.setGeometry(QRect(1, 25, 600, 300))
        self.plainText = QPlainTextEdit(self.frame1)
        self.plainText.resize(600,300)
        self.plainText.setPlaceholderText("This is some text for our plaintextedit                                               ")
 
        self.plainText.setReadOnly(True)
 
 
        self.text = "import matplotlib.pylab as plt"#\nfrom matplotlib.figure import Figure"
        #text = text + "\nfig = Figure(figsize=(5, 3))" 
        self.text = self.text + "\nfig, ax = plt.subplots()"
        
        if mainWin.ext == '.csv':
            self.text = self.text + "\nimport pandas as pd"
            self.text = self.text + "\nd = pd.read_csv('"+mainWin.fileName+"')"
        if (mainWin.ext == '.dat')|(mainWin.ext == '.txt'):
            self.text = self.text + "\nimport numpy as np"
            self.text = self.text + "\nd = np.loadtxt('"+mainWin.fileName+"')"
        if mainWin.YIndex != None:
            for i in range(0,len(mainWin.YIndex)):
                if mainWin.ext == '.csv':
                    self.text = self.text + "\nax.plot(d.iloc[:,"+str(mainWin.XIndex)+"],d.iloc[:,"+str(mainWin.YIndex[i]) +"],"
                elif (mainWin.ext == '.dat') | (mainWin.ext == '.txt') :
                    self.text = self.text + "\nax.plot(d[:,"+str(mainWin.XIndex)+"],d[:,"+str(mainWin.YIndex[i]) +"],"
                self.text = self.text + "\n\tcolor = '" +str(mainWin.colPlotObject[mainWin.YIndex[i]].lineColor)
                self.text = self.text +"', linestyle ='" + str(mainWin.colPlotObject[mainWin.YIndex[i]].lineStyle)
                self.text = self.text +"', linewidth = " + str(mainWin.colPlotObject[mainWin.YIndex[i]].width)
                self.text = self.text +",\n\tdrawstyle = '" + str(mainWin.colPlotObject[mainWin.YIndex[i]].drawStyle)
                self.text = self.text +"', label = '" + str(mainWin.colPlotObject[mainWin.YIndex[i]].label)
                self.text = self.text +"',\n\t marker = '" + str(mainWin.colPlotObject[mainWin.YIndex[i]]. marker)
                self.text = self.text +"', markersize = " + str(mainWin.colPlotObject[mainWin.YIndex[i]].size)
                self.text = self.text +",markeredgecolor = '" + str(mainWin.colPlotObject[mainWin.YIndex[i]].edgeColor)
                self.text = self.text +"',markerfacecolor = '" + str(mainWin.colPlotObject[mainWin.YIndex[i]].faceColor)+"')"
        if mainWin.plotAxesProp.xScale != None:
            self.text = self.text + "\nax.set_xscale('" + str(mainWin.plotAxesProp.xScale) + "')"
        if mainWin.plotAxesProp.yScale != None:
            self.text = self.text + "\nax.set_yscale('" + str(mainWin.plotAxesProp.yScale) + "')"
            
        if mainWin.plotAxesProp.xLabel != None:
            self.text = self.text + "\nax.set_xlabel('" + str(mainWin.plotAxesProp.xLabel) + "')"
        if mainWin.plotAxesProp.yLabel != None:
            self.text = self.text + "\nax.set_ylabel('" + str(mainWin.plotAxesProp.yLabel) + "')"
            
        if (mainWin.plotAxesProp.xMin != None) & (mainWin.plotAxesProp.xMax != None):
            self.text = self.text + "\nax.set_xlim(left = " + str(mainWin.plotAxesProp.xMin)
            self.text = self.text + ", right = " + str(mainWin.plotAxesProp.xMax) + ")"

        if (mainWin.plotAxesProp.yMin != None) & (mainWin.plotAxesProp.yMax != None):
            self.text = self.text + "\nax.set_ylim(bottom = " + str(mainWin.plotAxesProp.yMin)
            self.text = self.text + ", top = " + str(mainWin.plotAxesProp.yMax)+")" 
        if mainWin.gridObject.gridEnable:
            self.text =  self.text + "\nax.grid(color ='" + str(mainWin.gridObject.lineColor)
            self.text = self.text + "', linestyle = '" + str(mainWin.gridObject.lineStyle)
            self.text = self.text +"',axis = '" + str(mainWin.gridObject.axis)
            self.text = self.text +"',which = '" + str(mainWin.gridObject.which)
            self.text = self.text + "', linewidth = "+ str(mainWin.gridObject.width) + ")"   
                
        if mainWin.legendEnable:
            self.text = self.text + "\nax.legend(loc = '" + mainWin.legProp.location
            self.text = self.text + "',frameon = " + str(mainWin.legProp.frameon)
            self.text = self.text + ", fontsize = " + str(mainWin.legProp.fontsize)
            if mainWin.legProp.title == None:
                self.text = self.text + ", title = " + 'None'
            else:
                self.text = self.text + ", title = '" + mainWin.legProp.title + "'"
            self.text = self.text + ",\n\tmarkerfirst = " + str(mainWin.legProp.markerfirst)
            self.text = self.text + ", markerscale = " + str(mainWin.legProp.markerscale)
            self.text = self.text + ", labelspacing = " + str(mainWin.legProp.labelspacing)
            self.text = self.text + ", columnspacing = "+ str(mainWin.legProp.columnspacing)+")"
        if mainWin.titleObject.titleEnable:
            self.text = self.text + "\nax.set_title(label = '" + str(mainWin.titleObject.label)
            self.text = self.text + "',loc = '" +str(mainWin.titleObject.loc) + "')" 
        #if mainWin.yTicksObject.xTicksEnable:
        #    self.text = self.text + "\nax.set_yticks("+str(mainWin.yTicksObject.xticks)+")"
        #    self.text = self.text + "\nax.tick_params(axis='y',direction='"+mainWin.yTicksObject.direction+"')"
        #    self.text = self.text + "\nax.set_yticklabels("+str(mainWin.yTicksObject.xtickslabels);
        #    self.text = self.text +",rotation = "+str(mainWin.yTicksObject.rotation)+")"
        #if mainWin.xTicksObject.xTicksEnable:
        #    self.text = self.text + "\nax.set_xticks("+str(mainWin.xTicksObject.xticks)+")"
        #    self.text = self.text + "\nax.tick_params(axis='x',direction='"+mainWin.xTicksObject.direction+"')"
        #    self.text = self.text + "\nax.set_xticklabels("+str(mainWin.xTicksObject.xtickslabels);
        #    self.text = self.text +",rotation = "+str(mainWin.xTicksObject.rotation)+")"
#       added by mbp:
        self.text = self.text + "\nplt.tight_layout()"
        self.text = self.text + "\nplt.show()"
        self.text = self.text +"\n"
        self.plainText.appendPlainText(self.text)
        self.plainText.setUndoRedoEnabled(False)
        vbox.addWidget(self.plainText)
        
    def openFileSaveDialog(self):#Callback function to save the script
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", 
                            "","*.py ", options=options)
        print(self.fileName)
        f= open(self.fileName+'.py',"w+")
        f.write(self.text)
        f.close();
        #ax = self.m.fig.axes;
        #self.m.fig.savefig(self.fileName)

class PlotObject(object):
    """
    class to save the properties of plot
    """
    def __init__(self, label = '',lineStyle = 'solid', drawStyle = 'default', width = 0.7, lineColor = None,
                        marker = '', size = 5,edgeColor = 'red',faceColor = 'red'):
        self.lineStyle =lineStyle; self.drawStyle = drawStyle; 
        self.width = width; self.lineColor = lineColor;
        self.marker = marker; self.size = size;
        self.edgeColor = edgeColor;self.faceColor = faceColor;
        self.label = label;
    def setLineStyle(self,lineStyle):
        self.lineStyle = lineStyle;
    def setDrawStyle(self,drawStyle):
        self.drawStyle = drawStyle;
    def setWidth(self,width):
        self.width =  width;
    def setLineColor(self,lineColor):
        self.lineColor = lineColor;
    def setMarker(self,marker):
        self.marker = marker;
    def setSize(self,size):
        self.size = size;
    def setEdgeColor(self,edgeColor):
        self.edgeColor = edgeColor
    def setFaceColor(self,faceColor):
        self.faceColor = faceColor
    def setLabel(self,label):
        self.label = label;
        
class TitleObject(object):
    """
    class to save properties of title of the plot
    """
    def __init__(self, label = "", loc = 'center',titleEnable=True):
        self.label = label; self.loc = loc; 
        self.titleEnable = titleEnable
    def setLabel(self,label):
        self.label = label;
    def setTitleEnable(self,titleEnable):
        self.titleEnable = titleEnable
    def setLoc(self,loc):
        self.loc = loc;

class GridObject(object):
    """
    class to save properties of grid of the plot
    """
    def __init__(self, lineStyle = 'solid', width = 0.7, lineColor = 'black',
                        which = 'both', axis = 'both', gridEnable = True):
        self.lineStyle =lineStyle;  
        self.width = width; self.lineColor = lineColor;
        self.which = which; self.axis = axis;
        self.gridEnable = True;
    def setLineStyle(self,lineStyle):
        self.lineStyle = lineStyle;
    def setWidth(self,width):
        self.width =  width;
    def setLineColor(self,lineColor):
        self.lineColor = lineColor;
    def setWhich(self,which):
        self.which = which;
    def setAxis(self,axis):
        self.axis = axis
    def setGridEnable(self,gridEnable):
        self.gridEnable = gridEnable;

class xTicksPropObject(object):
    """
    class to save properties of x-ticks and y-ticks of the plot
    """
    def __init__(self,xTicksEnable = True, direction='inout',rotation=0,xticks = [],xtickslabels=[]):
        self.direction = direction;self.rotation = rotation; 
        self.xticks = xticks; self.xtickslabels = xtickslabels;
        self.xTicksEnable = xTicksEnable
    def setxTicksEnable(self,xTicksEnable):
        self.xTicksEnable = xTicksEnable;
    def setDirection(self,direction):
        self.direction = direction;
    def setRotation(self,rotation):
        self.rotation = rotation;
    def setXTicks(self,xticks):
        self.xticks = xticks;
    def setXTicksLabels(self,xtickslabels):
        self.xtickslabels = xtickslabels;


class AxesPropObject(object):
    """
    class to save properties of x-axis and y-axis of the plot
    """
    def __init__(self, xScale = 'linear',xLabel = 'X-Axis', xMin = None, xMax = None,
                       yScale = 'linear',yLabel = 'Y-Axis', yMin = None, yMax = None):
        self.xScale = xScale;self.xLabel = xLabel; 
        self.xMin = xMin; self.xMax = xMax;
        self.yScale = yScale; self.yLabel = yLabel;
        self.yMin = yMin; self.yMax = yMax
    def setxScale(self,xScale):
        self.xScale = xScale;
    def setxLabel(self,xLabel):
        self.xLabel = xLabel;
    def setxMin(self,xMin):
        self.xMin = xMin;
    def setxMax(self,xMax):
        self.xMax = xMax;
    def setyScale(self,yScale):
        self.yScale = yScale;
    def setyLabel(self,yLabel):
        self.yLabel = yLabel;
    def setyMin(self,yMin):
        self.yMin = yMin;
    def setyMax(self,yMax):
        self.yMax = yMax;
        
class LegendObject(object):
    """
    class to save properties of legend of the plot
    """
    def __init__(self, location = 'best',frameon = True, fontsize = 10, title = None,
                        markerfirst = True, markerscale = 1.0, labelspacing = 0.5, columnspacing = 2.0):
        self.location = location; self.frameon = frameon;
        self.fontsize = fontsize; self.title = title;
        self.markerfirst = markerfirst; self.markerscale = markerscale; 
        self.labelspacing = labelspacing; self.columnspacing = columnspacing
    def setlocation(self,location):
        self.location = location;
    def setframeon(self,frameon):
        self.frameon = frameon;
    def setfontsize(self,fontsize):
        self.fontsize =  fontsize;
    def settitle(self,title):
        self.title = title;
    def setmarkerfirst(self,markerfirst):
        self.markerfirst = markerfirst;
    def setmarkerscale(self,markerscale):
        self.markerscale = markerscale;
    def setlabelspacing(self,labelspacing):
        self.labelspacing = labelspacing
    def setcolumnspacing(self,columnspacing):
        self.columnspacing = columnspacing
        
class LinePropPopup(QMainWindow):
    """
    class to create window for plot properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();
        
    def widget(self):
        canvas = QPixmap(185, 130)
        canvas.fill(QColor("#FFFFFF"));
        myFont = QFont(); myFont.setBold(True);
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 40, 185, 130))
        self.labelC = QLabel(self.frame18)      
        self.labelC.setPixmap(canvas)
        self.frame19 = QFrame(self);self.frame19.setGeometry(QRect(210, 40, 180, 130))
        self.labelC2 = QLabel(self.frame19)
        self.labelC2.setPixmap(canvas)
        
        self.frame1 = QFrame(self);self.frame1.setGeometry(QRect(10, 10, 250, 25))
        self.combo1 = QComboBox(self.frame1)
        self.combo1.currentIndexChanged.connect(self.yLineProp)
        
        self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 175, 50, 25))
        self.def1 = QLabel("Default:",self.frameD);self.def1.setFont(myFont)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(65, 175, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.cb1.stateChanged.connect(self.dafaultLineProp)
        
        self.frame29 = QFrame(self);self.frame29.setGeometry(QRect(220,1,175,25))
        self.leglabelT = QLabel("Label:(used for legend)",self.frame29);
        self.frame28 = QFrame(self);self.frame28.setGeometry(QRect(220,15,175,25))
        self.leglabel = QLineEdit("0.5",self.frame28);
        self.leglabel.setFixedWidth(120)
        
        self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(20, 45, 250, 25))
        self.Label1 = QLabel("Line Properties:",self.frame2);
        myFont = QFont(); myFont.setBold(True);self.Label1.setFont(myFont)
        
        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 65, 250, 25))
        self.Label2 = QLabel("Line Style:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(90, 65, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("solid");self.combo2.addItem("None");self.combo2.addItem("dotted")
        self.combo2.addItem("dashed");self.combo2.addItem("dashdot");
        
        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 90, 250, 25))
        self.Label3 = QLabel("Draw Style:",self.frame4)
        self.frame8 = QFrame(self);self.frame8.setGeometry(QRect(90, 90, 250, 25))
        self.combo3 = QComboBox(self.frame8)
        self.combo3.addItem("default");self.combo3.addItem("steps-post");
        self.combo3.addItem("steps-pre");self.combo3.addItem("steps-mid")
        
        self.frame5 = QFrame(self);self.frame5.setGeometry(QRect(20, 115, 250, 25))
        self.Label4 = QLabel("Width:",self.frame5)
        self.frame26 = QFrame(self);self.frame26.setGeometry(QRect(90,115,115,25))
        self.wdBtn = QLineEdit("0.5",self.frame26);
        self.wdBtn.setFixedWidth(95)
        validator = QDoubleValidator()
        self.wdBtn.setValidator(validator)
        
        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(20, 140, 250, 25))
        self.Label5 = QLabel("Color:",self.frame6)
        self.frame25 = QFrame(self);self.frame25.setGeometry(QRect(100,140,30,25))
        self.lnBtn = QPushButton(self.frame25);self.lnBtn.clicked.connect(self.openlnColorDlg)
        self.pixmap = QPixmap(10,10);self.pixmap.fill(QColor("red"));
        self.lnCIcon= QIcon(self.pixmap);self.lnBtn.setIcon(self.lnCIcon);
        self.frame11 = QFrame(self);self.frame11.setGeometry(QRect(220, 45, 250, 25))
        self.Label6 = QLabel("Marker Properties:",self.frame11);self.Label6.setFont(myFont)
        
        self.frame12 = QFrame(self);self.frame12.setGeometry(QRect(220, 65, 250, 25))
        self.Label7 = QLabel("Style:",self.frame12)
        self.frame13 = QFrame(self);self.frame13.setGeometry(QRect(300, 65, 250, 25))
        self.combo4 = QComboBox(self.frame13)
        mStyles = ["",".",",","o","v","^","<",">","1","2","3","4","8","s","p","P","*",
		            "h","H","+","x","X","D","d","|","_","0","1","2","3","4","5","6","7","8","9","10","11"]
		            
        for i in range(0,len(mStyles)):
            self.combo4.addItem(mStyles[i]);
            
        self.frame14 = QFrame(self);self.frame14.setGeometry(QRect(220, 90, 250, 25))
        self.Label8 = QLabel("Size:",self.frame14)
        self.frame27 = QFrame(self);self.frame27.setGeometry(QRect(300,90,115,25))
        self.sizeBtn = QLineEdit("0.5",self.frame27);
        self.sizeBtn.setFixedWidth(75)
        validator = QDoubleValidator()
        self.sizeBtn.setValidator(validator)
        
        self.frame16 = QFrame(self);self.frame16.setGeometry(QRect(220, 115, 250, 25))
        self.Label9 = QLabel("Edge Color:",self.frame16)
        self.frame24 = QFrame(self);self.frame24.setGeometry(QRect(325,115,30,25))
        self.edBtn = QPushButton(self.frame24);self.edBtn.clicked.connect(self.openEdColorDlg)
        self.pixmap = QPixmap(10,10);self.pixmap.fill(QColor("black"));
        self.edCIcon= QIcon(self.pixmap);self.edBtn.setIcon(self.edCIcon);
        
        self.frame17 = QFrame(self);self.frame17.setGeometry(QRect(220, 140, 250, 25))
        self.Label10 = QLabel("Face Color:",self.frame17)
        self.frame23 = QFrame(self);self.frame23.setGeometry(QRect(325,140,30,25))
        self.fcBtn = QPushButton(self.frame23);self.fcBtn.clicked.connect(self.openFcColorDlg)
        self.pixmap.fill(QColor("red"));
        self.redIcon= QIcon(self.pixmap);self.fcBtn.setIcon(self.redIcon);
        
        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 10), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(180, 125))
        painter.drawLine(QPoint(180, 10), QPoint(180, 125))
        painter.drawLine(QPoint(120, 10), QPoint(180, 10))
        painter.drawLine(QPoint(5, 10), QPoint(7, 10))	
        painter.end()
        
        painter = QPainter(self.labelC2.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 10), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(175, 125))
        painter.drawLine(QPoint(175, 10), QPoint(175, 125))
        painter.drawLine(QPoint(138, 10), QPoint(175, 10))
        painter.drawLine(QPoint(5, 10), QPoint(7, 10))	
        painter.end()
        
        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(120, 170, 90, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)
        
        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(210, 170, 90, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)
        
        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(300, 170, 90, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)
        
        self.linecolor = QColor('red');
        self.edgecolor = QColor('black');
        self.facecolor = QColor('red');
        
    def applyBtnAction(self):#Callback function to change plot properties
        if self.combo1.currentText()!= '':
            linePropSelect = self.combo1.currentText()
            selIndexL = mainWin.YCols.indexFromItem(mainWin.YCols.findItems(linePropSelect,Qt.MatchContains)[0])
            selIndex = int(selIndexL.row())
            mainWin.colPlotObject[selIndex].setLineStyle(self.combo2.currentText())
            mainWin.colPlotObject[selIndex].setDrawStyle(self.combo3.currentText())
            mainWin.colPlotObject[selIndex].setWidth(float(self.wdBtn.text()))
            mainWin.colPlotObject[selIndex].setMarker(self.combo4.currentText())
            mainWin.colPlotObject[selIndex].setLineColor(self.linecolor.name())
            mainWin.colPlotObject[selIndex].setSize(float(self.sizeBtn.text()))
            mainWin.colPlotObject[selIndex].setFaceColor(self.facecolor.name())
            mainWin.colPlotObject[selIndex].setEdgeColor(self.edgecolor.name())
            mainWin.colPlotObject[selIndex].setLabel(self.leglabel.text())
            mainWin.plotDataWithChangedOptions()
	
    def yLineProp(self):
        linePropSelect = self.combo1.currentText()    
        selIndexL = mainWin.YCols.indexFromItem(mainWin.YCols.findItems(linePropSelect,Qt.MatchContains)[0])	   
        selIndex = int(selIndexL.row())
        self.combo2.setCurrentText(mainWin.colPlotObject[selIndex].lineStyle)
        self.combo3.setCurrentText(mainWin.colPlotObject[selIndex].drawStyle)
        self.wdBtn.setText(str(mainWin.colPlotObject[selIndex].width))
        self.sizeBtn.setText(str(mainWin.colPlotObject[selIndex].size))
        self.pixmap.fill(QColor(mainWin.colPlotObject[selIndex].lineColor));
        self.redIcon= QIcon(self.pixmap);
        self.lnBtn.setIcon(self.redIcon);  
        self.combo4.setCurrentText(mainWin.colPlotObject[selIndex].marker)
        self.pixmap.fill(QColor(mainWin.colPlotObject[selIndex].faceColor));
        self.redIcon= QIcon(self.pixmap);
        self.fcBtn.setIcon(self.redIcon);
        self.pixmap.fill(QColor(mainWin.colPlotObject[selIndex].edgeColor));
        self.redIcon= QIcon(self.pixmap);
        self.edBtn.setIcon(self.redIcon);  
        self.leglabel.setText(str(mainWin.colPlotObject[selIndex].label))
        self.linecolor = QColor(mainWin.colPlotObject[selIndex].lineColor);
        self.edgecolor = QColor(mainWin.colPlotObject[selIndex].edgeColor);
        self.facecolor = QColor(mainWin.colPlotObject[selIndex].faceColor);
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
  
    def dafaultLineProp(self):#callback function to change plot properties to default
        linePropSelect = self.combo1.currentText()    
        selIndexL = mainWin.YCols.indexFromItem(mainWin.YCols.findItems(linePropSelect,Qt.MatchContains)[0])	   
        selIndex = int(selIndexL.row())
        mainWin.colPlotObject[selIndex] = PlotObject(label = linePropSelect, lineColor = mainWin.colorSet[selIndex])
        self.yLineProp()
		
    def cancelBtnAction(self):
        self.close();
    def okBtnAction(self):	    
        self.close();
    def openFcColorDlg(self):#callback function to get changed facecolor of marker
        self.facecolor = QColorDialog.getColor()
        self.pixmap.fill(self.facecolor);
        self.redIcon= QIcon(self.pixmap);
        self.fcBtn.setIcon(self.redIcon);
    def openEdColorDlg(self):#Callback function to get changed edgecolor of marker
        self.edgecolor = QColorDialog.getColor()
        self.pixmap.fill(self.edgecolor);
        self.edCIcon= QIcon(self.pixmap);
        self.edBtn.setIcon(self.edCIcon); 
    def openlnColorDlg(self):
        self.linecolor = QColorDialog.getColor()#callback function to get changed linecolor 
        self.pixmap.fill(self.linecolor);
        self.lnCIcon= QIcon(self.pixmap);
        self.lnBtn.setIcon(self.lnCIcon);
	    
class Header(QMainWindow):

	def __init__(self):
		QMainWindow.__init__(self)
		self.widget();

	def widget(self):
	    self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 25, 150, 25))
	    self.def1 = QLabel("No of lines in Header:",self.frameD);
	    self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(200, 25, 75, 25))
	    self.hBtn = QLineEdit("0",self.frame2);
	    self.hBtn.setFixedWidth(75)
	    self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(200, 70, 90, 25))
	    self.okBtn = QPushButton("Ok",self.frame22)
	    self.okBtn.clicked.connect(self.okBtnAction)

	def okBtnAction(self):
	    self.close();
	    mainWin.header = int(self.hBtn.text())
	    mainWin.readFile();  	    
        
	
class GridPopup(QMainWindow):
    """
    class to create window for grid properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();
        
    def widget(self):
        canvas = QPixmap(380, 130)
        canvas.fill(QColor("#FFFFFF"));
        myFont = QFont(); myFont.setBold(True);
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 20, 380, 130))
        self.labelC = QLabel(self.frame18)      
        self.labelC.setPixmap(canvas)
        
        self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 175, 50, 25))
        self.def1 = QLabel("Default:",self.frameD);self.def1.setFont(myFont)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(65, 175, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.cb1.stateChanged.connect(self.dafaultLineProp)
        
        self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(20, 25, 250, 25))
        self.Label1 = QLabel("Grid:",self.frame2);
        myFont = QFont(); myFont.setBold(True);self.Label1.setFont(myFont)
        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 50, 250, 25))
        self.Label3 = QLabel("Grid on-off:",self.frame4)
        self.frameCB2 = QFrame(self);self.frameCB2.setGeometry(QRect(90, 50, 25, 25))
        self.cb2 = QCheckBox(self.frameCB2)
        self.cb2.setCheckState(QtCore.Qt.Checked)
        
        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 85, 250, 25))
        self.Label2 = QLabel("Line Style:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(90, 85, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("solid");self.combo2.addItem("None");self.combo2.addItem("dotted")
        self.combo2.addItem("dashed");self.combo2.addItem("dashdot");		
        
        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(20, 120, 250, 25))
        self.Label5 = QLabel("Color:",self.frame6)
        self.frame25 = QFrame(self);self.frame25.setGeometry(QRect(100,120,30,25))
        self.lnBtn = QPushButton(self.frame25);self.lnBtn.clicked.connect(self.openlnColorDlg)
        self.pixmap = QPixmap(10,10);self.pixmap.fill(QColor("red"));
        self.lnCIcon= QIcon(self.pixmap);self.lnBtn.setIcon(self.lnCIcon);

        self.frame12 = QFrame(self);self.frame12.setGeometry(QRect(220, 50, 250, 25))
        self.Label7 = QLabel("Which:",self.frame12)
        self.frame13 = QFrame(self);self.frame13.setGeometry(QRect(300, 50, 250, 25))
        self.combo4 = QComboBox(self.frame13)
        self.combo4.addItem("major");self.combo4.addItem("minor");self.combo4.addItem("both");

        self.frame14 = QFrame(self);self.frame14.setGeometry(QRect(220, 85, 250, 25))
        self.Label8 = QLabel("Width:",self.frame14)
        self.frame27 = QFrame(self);self.frame27.setGeometry(QRect(300,85,115,25))
        self.sizeBtn = QLineEdit("0.5",self.frame27);
        self.sizeBtn.setFixedWidth(75)
        validator = QDoubleValidator()
        self.sizeBtn.setValidator(validator)

        self.frame16 = QFrame(self);self.frame16.setGeometry(QRect(220, 120, 250, 25))
        self.Label9 = QLabel("Axis:",self.frame16)
        self.frame24 = QFrame(self);self.frame24.setGeometry(QRect(300,120,150,25))
        self.combo3 = QComboBox(self.frame24)
        self.combo3.addItem("both");self.combo3.addItem("x");self.combo3.addItem("y");

        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 10), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(375, 125))
        painter.drawLine(QPoint(375, 10), QPoint(375, 125))
        painter.drawLine(QPoint(50, 10), QPoint(375, 10))
        painter.drawLine(QPoint(5, 10), QPoint(7, 10))
        painter.end()

        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(120, 170, 90, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)

        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(210, 170, 90, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)

        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(300, 170, 90, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)
        self.linecolor = QColor('black');

    def applyBtnAction(self):#callback function to apply changes in grid properties
        mainWin.gridObject.setLineStyle(self.combo2.currentText())
        mainWin.gridObject.setAxis(self.combo3.currentText())
        mainWin.gridObject.setWidth(float(self.sizeBtn.text()))
        mainWin.gridObject.setWhich(self.combo4.currentText())
        mainWin.gridObject.setLineColor(self.linecolor.name())
        mainWin.gridObject.gridEnable = self.cb2.isChecked()
        mainWin.m.changeGridProps()
        mainWin.plotW.changeGridProps()
    def GridPropShow(self):
        self.combo2.setCurrentText(mainWin.gridObject.lineStyle)
        self.combo3.setCurrentText(mainWin.gridObject.axis)
        self.sizeBtn.setText(str(mainWin.gridObject.width))

        self.pixmap.fill(QColor(mainWin.gridObject.lineColor));
        self.redIcon= QIcon(self.pixmap);
        self.lnBtn.setIcon(self.redIcon);

        self.combo4.setCurrentText(mainWin.gridObject.which)
        self.linecolor = QColor(mainWin.gridObject.lineColor);
        self.cb1.setCheckState(QtCore.Qt.Unchecked)

        bs = QtCore.Qt.Unchecked
        if mainWin.gridObject.gridEnable:
            bs = QtCore.Qt.Checked
        self.cb2.setCheckState(bs)

    def dafaultLineProp(self):
        mainWin.gridObject = GridObject()
        self.GridPropShow()

    def cancelBtnAction(self):
        self.close();

    def okBtnAction(self):
        self.close();

    def openlnColorDlg(self):#callback function to get changed color of grid lines
        self.linecolor = QColorDialog.getColor()
        self.pixmap.fill(self.linecolor);
        self.lnCIcon= QIcon(self.pixmap);
        self.lnBtn.setIcon(self.lnCIcon);

class AxesPopup(QMainWindow):
    """
    class to create window for axes properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();
    def widget(self):
        canvas = QPixmap(185, 130)
        canvas.fill(QColor("#FFFFFF"));
        myFont = QFont(); myFont.setBold(True);
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 10, 185, 130))
        self.labelC = QLabel(self.frame18)
        self.labelC.setPixmap(canvas)
        self.frame19 = QFrame(self);self.frame19.setGeometry(QRect(210, 10, 185, 130))
        self.labelC2 = QLabel(self.frame19)
        self.labelC2.setPixmap(canvas)

        self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 145, 50, 25))
        self.def1 = QLabel("Default:",self.frameD);self.def1.setFont(myFont)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(65, 145, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.cb1.stateChanged.connect(self.dafaultLineProp)

        self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(20, 15, 250, 25))
        self.Label1 = QLabel("X-Axis:",self.frame2);self.Label1.setFont(myFont)
        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 35, 250, 25))
        self.Label2 = QLabel("Scale:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(60, 35, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("linear");self.combo2.addItem("log");self.combo2.addItem("logit")

        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 60, 250, 25))
        self.Label3 = QLabel("Label:",self.frame4)
        self.frame8 = QFrame(self);self.frame8.setGeometry(QRect(60, 60, 250, 25))
        self.labelEdit = QLineEdit("X-Axis",self.frame8);
        self.labelEdit.setFixedWidth(120)

        self.frame5 = QFrame(self);self.frame5.setGeometry(QRect(20, 85, 250, 25))
        self.Label4 = QLabel("Left:",self.frame5)
        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(60, 85, 250, 25))
        self.XLimL = QLineEdit("X-Lim",self.frame6);
        self.XLimL.setFixedWidth(120)
        validator = QDoubleValidator()
        self.XLimL.setValidator(validator)

        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(20, 110, 250, 25))
        self.Label5 = QLabel("Right:",self.frame6)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(60, 110, 250, 25))
        self.XLimR = QLineEdit("X-Lim",self.frame7);
        self.XLimR.setFixedWidth(120)
        validator = QDoubleValidator()
        self.XLimR.setValidator(validator)

        self.frame11 = QFrame(self);self.frame11.setGeometry(QRect(220, 15, 250, 25))
        self.Label6 = QLabel("Y-Axis:",self.frame11);self.Label6.setFont(myFont)

        self.frame12 = QFrame(self);self.frame12.setGeometry(QRect(220, 35, 250, 25))
        self.Label7 = QLabel("Scale:",self.frame12)
        self.frame13 = QFrame(self);self.frame13.setGeometry(QRect(270, 35, 250, 25))
        self.combo4 = QComboBox(self.frame13)
        self.combo4.addItem("linear");self.combo4.addItem("log");self.combo4.addItem("logit")

        self.frame14 = QFrame(self);self.frame14.setGeometry(QRect(220, 60, 250, 25))
        self.Label8 = QLabel("Label:",self.frame14)
        self.frame15 = QFrame(self);self.frame15.setGeometry(QRect(270, 60, 250, 25))
        self.YlabelEdit = QLineEdit("Y-Axis",self.frame15);
        self.YlabelEdit.setFixedWidth(120)

        self.frame16 = QFrame(self);self.frame16.setGeometry(QRect(220, 85, 250, 25))
        self.Label9 = QLabel("Bottom:",self.frame16)
        self.frame24 = QFrame(self);self.frame24.setGeometry(QRect(270,85,250,25))
        self.YlimB = QLineEdit("0",self.frame24);
        self.YlimB.setFixedWidth(120)
        validator = QDoubleValidator()
        self.YlimB.setValidator(validator)

        self.frame17 = QFrame(self);self.frame17.setGeometry(QRect(220, 110, 250, 25))
        self.Label10 = QLabel("Top:",self.frame17)
        self.frame23 = QFrame(self);self.frame23.setGeometry(QRect(270,110,250,25))
        self.YlimT = QLineEdit("10",self.frame23);
        self.YlimT.setFixedWidth(120)
        validator = QDoubleValidator()
        self.YlimT.setValidator(validator)	

        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 10), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(180, 125))
        painter.drawLine(QPoint(180, 10), QPoint(180, 125))
        painter.drawLine(QPoint(60, 10), QPoint(180, 10))
        painter.drawLine(QPoint(5, 10), QPoint(7, 10))
        painter.end()

        painter = QPainter(self.labelC2.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 10), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(180, 125))
        painter.drawLine(QPoint(180, 10), QPoint(180, 125))
        painter.drawLine(QPoint(60, 10), QPoint(180, 10))
        painter.drawLine(QPoint(5, 10), QPoint(7, 10))
        painter.end()

        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(120, 140, 90, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)

        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(210, 140, 90, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)

        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(300, 140, 90, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)

    def applyBtnAction(self):#callback function to apply changes in axes properties
        if self.combo2.currentText()!='None':
            mainWin.plotAxesProp.setxScale(self.combo2.currentText())
        if self.labelEdit.text() !='None':
            mainWin.plotAxesProp.setxLabel(self.labelEdit.text())
        if self.XLimL.text()!='None':
            mainWin.plotAxesProp.setxMin(float(self.XLimL.text()))
        if self.XLimR.text() !='None':
            mainWin.plotAxesProp.setxMax(float(self.XLimR.text()))
        if self.combo4.currentText()!='None':
            mainWin.plotAxesProp.setyScale(self.combo4.currentText())
        if self.YlabelEdit.text()!='None':
            mainWin.plotAxesProp.setyLabel(self.YlabelEdit.text())
        if self.YlimB.text()!='None':
            mainWin.plotAxesProp.setyMin(float(self.YlimB.text()))
        if self.YlimT.text()!='None':
            mainWin.plotAxesProp.setyMax(float(self.YlimT.text()))
        mainWin.m.changeAxesProps()
        mainWin.plotW.changeAxesProps()

    def AxesPropShow(self):
        self.combo2.setCurrentText(str(mainWin.plotAxesProp.xScale))
        self.combo4.setCurrentText(mainWin.plotAxesProp.yScale)
        self.labelEdit.setText(str(mainWin.plotAxesProp.xLabel))
        if mainWin.plotAxesProp.xMin!= None:
            self.XLimL.setText(str(format(mainWin.plotAxesProp.xMin,'.2f')))
        else:
            self.XLimL.setText(str(mainWin.plotAxesProp.xMin))

        if mainWin.plotAxesProp.xMax!= None:
            self.XLimR.setText(str(format(mainWin.plotAxesProp.xMax,'.2f')))
        else:
            self.XLimR.setText(str(mainWin.plotAxesProp.xMax))

        self.YlabelEdit.setText(str(mainWin.plotAxesProp.yLabel))

        if mainWin.plotAxesProp.yMin != None:
            self.YlimB.setText(str(format(mainWin.plotAxesProp.yMin,'.2f')))
        else:
            self.YlimB.setText(str(mainWin.plotAxesProp.yMin))

        if mainWin.plotAxesProp.yMax != None:
            self.YlimT.setText(str(format(mainWin.plotAxesProp.yMax,'.2f')))
        else:
            self.YlimT.setText(str(mainWin.plotAxesProp.yMax))

        self.cb1.setCheckState(QtCore.Qt.Unchecked)
    def dafaultLineProp(self):
        mainWin.plotAxesProp = AxesPropObject()
        self.AxesPropShow()
    def cancelBtnAction(self):
        self.close();
    def okBtnAction(self):
        self.close();  
		   
class TitlePopup(QMainWindow):
    """
    class to create window for title properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();

    def widget(self):
        canvas = QPixmap(250, 100)
        canvas.fill(QColor("#FFFFFF"));
        myFont = QFont(); myFont.setBold(True);
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 10, 250, 100))
        self.labelC = QLabel(self.frame18)
        self.labelC.setPixmap(canvas)

        self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 145, 50, 25))
        self.def1 = QLabel("Default:",self.frameD);self.def1.setFont(myFont)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(65, 145, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.cb1.stateChanged.connect(self.dafaultLineProp)

        self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(20, 15, 250, 25))
        self.Label1 = QLabel("Title:",self.frame2);self.Label1.setFont(myFont)

        self.frameT = QFrame(self);self.frameT.setGeometry(QRect(20, 30, 50, 25))
        self.def1 = QLabel("Title:",self.frameT);
        self.frameTE = QFrame(self);self.frameTE.setGeometry(QRect(80, 30, 25, 25))
        self.cb3 = QCheckBox(self.frameTE)
        self.cb3.setCheckState(QtCore.Qt.Checked)

        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 55, 250, 25))
        self.Label2 = QLabel("Position:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(80, 55, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("left");self.combo2.addItem("center");self.combo2.addItem("right")

        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 80, 250, 25))
        self.Label3 = QLabel("Label:",self.frame4)
        self.frame8 = QFrame(self);self.frame8.setGeometry(QRect(80, 80, 250, 25))
        self.labelEdit = QLineEdit("",self.frame8);
        self.labelEdit.setFixedWidth(175)

        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 5), QPoint(5, 95))
        painter.drawLine(QPoint(5, 95), QPoint(245, 95))
        painter.drawLine(QPoint(245, 5), QPoint(245, 95))
        painter.drawLine(QPoint(5, 5), QPoint(245, 5))
        painter.end()

        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(20, 170, 80, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)

        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(120, 170,80, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)

        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(220, 170, 80, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)
    def applyBtnAction(self):#callback function to apply the changed properties of title
        mainWin.titleObject.setLoc(self.combo2.currentText())
        mainWin.titleObject.setLabel(self.labelEdit.text())
        mainWin.titleObject.setTitleEnable(self.cb3.isChecked())
        mainWin.m.changeTitle()
        mainWin.plotW.changeTitle()

    def TitlePropShow(self):
        self.combo2.setCurrentText(str(mainWin.titleObject.loc))
        self.labelEdit.setText(str(mainWin.titleObject.label))
        bs = QtCore.Qt.Unchecked
        if mainWin.titleObject.titleEnable:
            bs = QtCore.Qt.Checked
        self.cb3.setCheckState(bs)

    def dafaultLineProp(self):
        mainWin.titleObject = TitleObject()
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.TitlePropShow()

    def cancelBtnAction(self):
        self.close();

    def okBtnAction(self):
        self.close();

class xTicksPopup(QMainWindow):
    """
    class to create window for x-ticks properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();

    def widget(self):
        canvas = QPixmap(460, 130)
        canvas.fill(QColor("#FFFFFF"));
        myFont = QFont(); myFont.setBold(True);
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 10, 460, 130))
        self.labelC = QLabel(self.frame18)
        self.labelC.setPixmap(canvas)

        self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 145, 50, 25))
        self.def1 = QLabel("Default:",self.frameD);self.def1.setFont(myFont)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(65, 145, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.cb1.stateChanged.connect(self.dafaultLineProp)

        self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(20, 15, 250, 25))
        self.Label1 = QLabel("x-Ticks:",self.frame2);self.Label1.setFont(myFont)

        self.frameT = QFrame(self);self.frameT.setGeometry(QRect(20, 30, 50, 25))
        self.def1 = QLabel("x-Ticks:",self.frameT);
        self.frameTE = QFrame(self);self.frameTE.setGeometry(QRect(105, 30, 25, 25))
        self.cb3 = QCheckBox(self.frameTE)
        self.cb3.setCheckState(QtCore.Qt.Checked)

        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 55, 250, 25))
        self.Label2 = QLabel("Direction:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(105, 55, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("in");self.combo2.addItem("out");self.combo2.addItem("inout")

        self.frame5 = QFrame(self);self.frame5.setGeometry(QRect(210, 55, 250, 25))
        self.Label4 = QLabel("Rotation:",self.frame5)
        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(270, 55, 50, 25))
        self.rotEdit = QLineEdit("0",self.frame6)
        self.rotEdit.setFixedWidth(50)
        self.frame25 = QFrame(self);self.frame25.setGeometry(QRect(320, 58, 250, 25))
        self.Label7 = QLabel("(in degrees:)",self.frame25)

        self.frame9 = QFrame(self);self.frame9.setGeometry(QRect(20, 80, 280, 25))
        self.Label5 = QLabel("xTicks:",self.frame9)
        self.frame10 = QFrame(self);self.frame10.setGeometry(QRect(105, 80, 280, 25))
        self.ticksEdit = QLineEdit("",self.frame10);
        self.ticksEdit.setFixedWidth(280)

        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 105, 280, 25))
        self.Label3 = QLabel("xTicksLabels:",self.frame4)
        self.frame8 = QFrame(self);self.frame8.setGeometry(QRect(105, 105, 280, 25))
        self.labelEdit = QLineEdit("",self.frame8);
        self.labelEdit.setFixedWidth(280)		

        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 5), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(455, 125))
        painter.drawLine(QPoint(455, 5), QPoint(455, 125))
        painter.drawLine(QPoint(5, 5), QPoint(455, 5))
        painter.end()

        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(385, 80, 80, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)

        self.frame23 =  QFrame(self);self.frame23.setGeometry(QRect(385, 105, 80, 25))
        self.applyBtn = QPushButton("Apply",self.frame23);
        self.applyBtn.clicked.connect(self.applyBtnAction2)

        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(120, 170,80, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)

        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(220, 170, 80, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)

    def applyBtnAction(self):#callback function to apply changes in x-ticks properies
        mainWin.xTicksObject.setDirection(self.combo2.currentText())
        mainWin.xTicksObject.setRotation(self.rotEdit.text())
        mainWin.xTicksObject.setxTicksEnable(self.cb3.isChecked())
        if self.ticksEdit.text() != 'None':
            xticklist = []
            xtickl = self.ticksEdit.text();
            xtickstr = xtickl[1:len(xtickl)-1]
            if xtickstr.find(",")>=0:
                for item in xtickstr.split(","):
                    xticklist.append(float(item))
            else:
                for item in xtickstr.split():
                    xticklist.append(float(item))

            mainWin.xTicksObject.setXTicks(xticklist)
            if self.labelEdit.text() != 'None':
                xticklabel = self.labelEdit.text();
                xticklabelstr = xticklabel[1:len(xticklabel)-1]
                xticklabelstr = xticklabelstr.replace("'","")
                mainWin.xTicksObject.setXTicksLabels(list(xticklabelstr.split(", ")))
		#print(mainWin.xTicksObject.xticks)
                mainWin.m.changeXTicks()
                mainWin.plotW.changeXTicks()
    def applyBtnAction2(self):
        mainWin.xTicksObject.setDirection(self.combo2.currentText())
        mainWin.xTicksObject.setRotation(self.rotEdit.text())
        mainWin.xTicksObject.setxTicksEnable(self.cb3.isChecked())
        if self.labelEdit.text() != 'None':
            xticklabel = self.labelEdit.text();
            xticklabelstr = xticklabel[1:len(xticklabel)-1]
            xticklabelstr = xticklabelstr.replace("'","")
            mainWin.xTicksObject.setXTicksLabels(list(xticklabelstr.split(", ")))
            mainWin.m.changeXTicksLabels()
            mainWin.plotW.changeXTicksLabels()

    def xTicksPropShow(self):
        self.combo2.setCurrentText(str(mainWin.xTicksObject.direction))
        self.rotEdit.setText(str(mainWin.xTicksObject.rotation))
        self.ticksEdit.setText(str(mainWin.xTicksObject.xticks))
        self.labelEdit.setText(str(mainWin.xTicksObject.xtickslabels))
        bs = QtCore.Qt.Unchecked

        if mainWin.xTicksObject.xTicksEnable:
            bs = QtCore.Qt.Checked
        self.cb3.setCheckState(bs)

    def dafaultLineProp(self):
        mainWin.xTicksObject.direction = 'inout'
        mainWin.xTicksObject.rotation = 0
        self.xTicksPropShow()

    def cancelBtnAction(self):
        self.close();

    def okBtnAction(self):
        self.close();

class yTicksPopup(QMainWindow):
    """
    class to create window for y-ticks properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();

    def widget(self):
        canvas = QPixmap(460, 130)
        canvas.fill(QColor("#FFFFFF"));
        myFont = QFont(); myFont.setBold(True);
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 10, 460, 130))
        self.labelC = QLabel(self.frame18)
        self.labelC.setPixmap(canvas)


        self.frameD = QFrame(self);self.frameD.setGeometry(QRect(10, 145, 50, 25))
        self.def1 = QLabel("Default:",self.frameD);self.def1.setFont(myFont)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(65, 145, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Unchecked)
        self.cb1.stateChanged.connect(self.dafaultLineProp)

        self.frame2 = QFrame(self);self.frame2.setGeometry(QRect(20, 15, 250, 25))
        self.Label1 = QLabel("y-Ticks:",self.frame2);self.Label1.setFont(myFont)

        self.frameT = QFrame(self);self.frameT.setGeometry(QRect(20, 30, 50, 25))
        self.def1 = QLabel("y-Ticks:",self.frameT);
        self.frameTE = QFrame(self);self.frameTE.setGeometry(QRect(105, 30, 25, 25))
        self.cb3 = QCheckBox(self.frameTE)
        self.cb3.setCheckState(QtCore.Qt.Checked)

        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 55, 250, 25))
        self.Label2 = QLabel("Direction:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(105, 55, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("in");self.combo2.addItem("out");self.combo2.addItem("inout")

        self.frame5 = QFrame(self);self.frame5.setGeometry(QRect(210, 55, 250, 25))
        self.Label4 = QLabel("Rotation:",self.frame5)
        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(270, 55, 50, 25))
        self.rotEdit = QLineEdit("0",self.frame6)
        self.rotEdit.setFixedWidth(50)
        self.frame25 = QFrame(self);self.frame25.setGeometry(QRect(320, 58, 250, 25))
        self.Label7 = QLabel("(in degrees:)",self.frame25)

        self.frame9 = QFrame(self);self.frame9.setGeometry(QRect(20, 80, 280, 25))
        self.Label5 = QLabel("yTicks:",self.frame9)
        self.frame10 = QFrame(self);self.frame10.setGeometry(QRect(105, 80, 280, 25))
        self.ticksEdit = QLineEdit("",self.frame10);
        self.ticksEdit.setFixedWidth(280)

        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 105, 280, 25))
        self.Label3 = QLabel("yTicksLabels:",self.frame4)
        self.frame8 = QFrame(self);self.frame8.setGeometry(QRect(105, 105, 280, 25))
        self.labelEdit = QLineEdit("",self.frame8);
        self.labelEdit.setFixedWidth(280)

        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 5), QPoint(5, 125))
        painter.drawLine(QPoint(5, 125), QPoint(455, 125))
        painter.drawLine(QPoint(455, 5), QPoint(455, 125))
        painter.drawLine(QPoint(5, 5), QPoint(455, 5))
        painter.end()

        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(385, 80, 80, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)

        self.frame23 =  QFrame(self);self.frame23.setGeometry(QRect(385, 105, 80, 25))
        self.applyBtn = QPushButton("Apply",self.frame23);
        self.applyBtn.clicked.connect(self.applyBtnAction2)

        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(120, 170,80, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)

        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(220, 170, 80, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)

    def applyBtnAction(self):
        mainWin.yTicksObject.setDirection(self.combo2.currentText())
        mainWin.yTicksObject.setRotation(self.rotEdit.text())
        mainWin.yTicksObject.setxTicksEnable(self.cb3.isChecked())
        if self.ticksEdit.text() != 'None':
            xticklist = []
            xtickl = self.ticksEdit.text();
            xtickstr = xtickl[1:len(xtickl)-1]
            if xtickstr.find(",")>=0:
                for item in xtickstr.split(","):
                    xticklist.append(float(item))
            else:
                for item in xtickstr.split():
                    xticklist.append(float(item))

            mainWin.yTicksObject.setXTicks(list(xticklist))
            if self.labelEdit.text() != 'None':
                xticklabel = self.labelEdit.text();
                xticklabelstr = xticklabel[1:len(xticklabel)-1]
                xticklabelstr = xticklabelstr.replace("'","")
                mainWin.yTicksObject.setXTicksLabels(list(xticklabelstr.split(", ")))
		#print(mainWin.xTicksObject.xticks)
                mainWin.m.changeYTicks()
                mainWin.plotW.changeYTicks()
    def applyBtnAction2(self):
        mainWin.yTicksObject.setDirection(self.combo2.currentText())
        mainWin.yTicksObject.setRotation(self.rotEdit.text())
        mainWin.yTicksObject.setxTicksEnable(self.cb3.isChecked())
        if self.labelEdit.text() != 'None':
            xticklabel = self.labelEdit.text();
            xticklabelstr = xticklabel[1:len(xticklabel)-1]
            xticklabelstr = xticklabelstr.replace("'","")
            mainWin.yTicksObject.setXTicksLabels(list(xticklabelstr.split(", ")))

        mainWin.m.changeYTicksLabels()
        mainWin.plotW.changeYTicksLabels()
    def yTicksPropShow(self):
        self.combo2.setCurrentText(str(mainWin.yTicksObject.direction))
        self.rotEdit.setText(str(mainWin.yTicksObject.rotation))
        self.ticksEdit.setText(str(mainWin.yTicksObject.xticks))
        self.labelEdit.setText(str(mainWin.yTicksObject.xtickslabels))
        bs = QtCore.Qt.Unchecked
        if mainWin.yTicksObject.xTicksEnable:
            bs = QtCore.Qt.Checked
            self.cb3.setCheckState(bs)

    def dafaultLineProp(self):
        mainWin.yTicksObject.direction = 'inout'
        mainWin.yTicksObject.rotation = 0
        self.yTicksPropShow()

    def cancelBtnAction(self):
        self.close();

    def okBtnAction(self):
        self.close();

class LegendPopup(QMainWindow):
    """
    class to create window for legend properties and 
    options to change them 
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.widget();

    def widget(self):
        canvas = QPixmap(380, 125)
        canvas.fill(QColor("#FFFFFF"));
        self.frame18 = QFrame(self);self.frame18.setGeometry(QRect(10, 30, 380, 125))
        self.labelC = QLabel(self.frame18)
        self.labelC.setPixmap(canvas)

        self.frame1 = QFrame(self);self.frame1.setGeometry(QRect(20, 10, 250, 25))
        self.combo1 = QLabel("Show Legend",self.frame1)
        self.frameCB1 = QFrame(self);self.frameCB1.setGeometry(QRect(150, 10, 25, 25))
        self.cb1 = QCheckBox(self.frameCB1)
        self.cb1.setCheckState(QtCore.Qt.Checked)

        myFont = QFont(); myFont.setBold(True);
        self.frame3 = QFrame(self);self.frame3.setGeometry(QRect(20, 40, 250, 25))
        self.Label2 = QLabel("Location:",self.frame3)
        self.frame7 = QFrame(self);self.frame7.setGeometry(QRect(90, 40, 250, 25))
        self.combo2 = QComboBox(self.frame7)
        self.combo2.addItem("best");self.combo2.addItem("upper right");self.combo2.addItem("upper left")
        self.combo2.addItem("lower left");self.combo2.addItem("lower right");
        self.combo2.addItem("lower center");self.combo2.addItem("upper center");
        self.combo2.addItem("center left");self.combo2.addItem("center right");self.combo2.addItem("center");

        self.frame4 = QFrame(self);self.frame4.setGeometry(QRect(20, 70, 250, 25))
        self.Label3 = QLabel("Font Size:",self.frame4)
        self.frame8 = QFrame(self);self.frame8.setGeometry(QRect(90, 70, 250, 25))
        self.fSize = QLineEdit("10",self.frame8);
        self.fSize.setFixedWidth(75)
        validator = QDoubleValidator()
        self.fSize.setValidator(validator)

        self.frame5 = QFrame(self);self.frame5.setGeometry(QRect(20, 100, 250, 25))
        self.Label4 = QLabel("Title:",self.frame5)
        self.frame26 = QFrame(self);self.frame26.setGeometry(QRect(90,100,115,25))
        self.legTitle = QLineEdit(None,self.frame26);
        self.legTitle.setFixedWidth(95)
        self.frame6 = QFrame(self);self.frame6.setGeometry(QRect(20, 130, 250, 25))
        self.Label5 = QLabel("Frame:",self.frame6)
        self.frame25 = QFrame(self);self.frame25.setGeometry(QRect(100,130,30,25))
        self.fr1 = QCheckBox(self.frame25)
        self.fr1.setCheckState(QtCore.Qt.Checked)

        self.frame12 = QFrame(self);self.frame12.setGeometry(QRect(205, 40, 250, 25))
        self.Label7 = QLabel("Label Spacing:",self.frame12)
        self.frame13 = QFrame(self);self.frame13.setGeometry(QRect(308, 40, 250, 25))
        self.lblSpc = QLineEdit("0.5",self.frame13);
        self.lblSpc.setFixedWidth(75)
        validator = QDoubleValidator()
        self.lblSpc.setValidator(validator)
        self.frame14 = QFrame(self);self.frame14.setGeometry(QRect(205, 70, 250, 25))
        self.Label8 = QLabel("Marker Scale:",self.frame14)
        self.frame27 = QFrame(self);self.frame27.setGeometry(QRect(308,70,115,25))
        self.mscale = QLineEdit("1.0",self.frame27);
        self.mscale.setFixedWidth(75)
        validator = QDoubleValidator()
        self.mscale.setValidator(validator)
        self.frame16 = QFrame(self);self.frame16.setGeometry(QRect(205, 100, 250, 25))
        self.Label9 = QLabel("Marker First:",self.frame16)
        self.frame24 = QFrame(self);self.frame24.setGeometry(QRect(308,100,30,25))
        self.m1 = QCheckBox(self.frame24)
        self.m1.setCheckState(QtCore.Qt.Checked)
        self.frame17 = QFrame(self);self.frame17.setGeometry(QRect(205, 130, 250, 25))
        self.Label10 = QLabel("Column Spacing:",self.frame17)
        self.frame23 = QFrame(self);self.frame23.setGeometry(QRect(308,125,250,25))
        self.clmSpc = QLineEdit("2.0",self.frame23);
        self.clmSpc.setFixedWidth(75)
        validator = QDoubleValidator()
        self.clmSpc.setValidator(validator)

        painter = QPainter(self.labelC.pixmap())
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(QPoint(5, 5), QPoint(5, 120))
        painter.drawLine(QPoint(5, 120), QPoint(375, 120))
        painter.drawLine(QPoint(375, 120), QPoint(375, 5))
        painter.drawLine(QPoint(375, 5), QPoint(5, 5))
        painter.end()

        self.frame20 =  QFrame(self);self.frame20.setGeometry(QRect(120, 170, 90, 25))
        self.applyBtn = QPushButton("Apply",self.frame20);
        self.applyBtn.clicked.connect(self.applyBtnAction)
        self.frame21 =  QFrame(self);self.frame21.setGeometry(QRect(210, 170, 90, 25))
        self.cancelBtn = QPushButton("Cancel",self.frame21)
        self.cancelBtn.clicked.connect(self.cancelBtnAction)
        self.frame22 =  QFrame(self);self.frame22.setGeometry(QRect(300, 170, 90, 25))
        self.okBtn = QPushButton("Ok",self.frame22)
        self.okBtn.clicked.connect(self.okBtnAction)
        self.linecolor = QColor('red');
        self.edgecolor = QColor('black');
        self.facecolor = QColor('red');

    def applyBtnAction(self):
        mainWin.legProp.setlocation(self.combo2.currentText())
        mainWin.legProp.setfontsize(float(self.fSize.text()))
        mainWin.legProp.settitle((self.legTitle.text()))
        mainWin.legProp.setlabelspacing(float(self.lblSpc.text()))
        mainWin.legProp.setmarkerscale(float(self.mscale.text()))
        mainWin.legProp.setcolumnspacing(float(self.clmSpc.text()))
        mainWin.legProp.setmarkerfirst(self.m1.isChecked())
        mainWin.legProp.setframeon(self.fr1.isChecked())
        mainWin.legendEnable = self.cb1.isChecked()
        if mainWin.legendEnable:
            mainWin.m.showLegend();
            mainWin.plotW.showLegend();
        else:
            mainWin.m.removeLegend()
            mainWin.plotW.removeLegend()

    def LegendPropShow(self):
        self.combo2.setCurrentText(mainWin.legProp.location)
        self.fSize.setText(str(mainWin.legProp.fontsize))
        self.legTitle.setText(mainWin.legProp.title)
        self.lblSpc.setText(str(mainWin.legProp.labelspacing))
        self.mscale.setText(str(mainWin.legProp.markerscale))
        self.clmSpc.setText(str(mainWin.legProp.columnspacing))
        bs = QtCore.Qt.Unchecked
        if mainWin.legProp.markerfirst :
            bs = QtCore.Qt.Checked
        self.m1.setCheckState(bs)
        bs = QtCore.Qt.Unchecked
        if mainWin.legProp.frameon:
            bs = QtCore.Qt.Checked
        self.fr1.setCheckState(bs)
        bs = QtCore.Qt.Unchecked
        if mainWin.legendEnable:
            bs = QtCore.Qt.Checked
        self.cb1.setCheckState(bs)

    def cancelBtnAction(self):
        self.close();

    def okBtnAction(self):	    
        self.close();

class ApplicationWindow(QMainWindow):
    """
    class to create main window for gui which has
    options to browse the data file, 
    a canvas to show plot, 
    and other options- to change plot properties, save figure, generate script
    """    
    NoOfCol = 0;total_rows=0;
    
    def __init__(self):
        print('App')
        super().__init__()
        self.title = "Demo"
        self.left = 400
        self.top = 100
        self.width = 800
        self.height = 600
        self.resize(self.width, self.height)
        self.move(self.left, self.top)
        
        self.widgetR();
        
    def widgetR(self):       
        self.colorSet = ["red","green","blue","magenta","black","orange","violet","brown"]
        self._main = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()#._main)     
            
        self.frame1 = QFrame(self)
        self.frame1.setGeometry(QRect(10, 40, 100, 25))
        self.LegBtn1 = QPushButton("BrowseFile",self.frame1)
        self.LegBtn1.setChecked(True)
        self.LegBtn1.clicked.connect(self.openFileNameDialog)
        layout.addWidget(self.LegBtn1)
        
        self.frame6 = QFrame(self)
        self.frame6.setGeometry(QRect(10, 70, 400, 30))
        self.labelFile = QLabel("File: Placeholder for file path and file name ",self.frame6)
        
        self.frame2 = QFrame(self)
        self.frame2.setGeometry(QRect(10, 90, 350, 30))
        self.label = QLabel("Number of columns:     ",self.frame2)
        layout.addWidget(self.label)
        self.label.setEnabled(0)

        self.frame5 = QFrame(self)
        self.frame5.setGeometry(QRect(10, 110, 350, 30))
        self.labelR = QLabel("Number of rows:                ",self.frame5)
        layout.addWidget(self.labelR)
        self.labelR.setEnabled(0)
        
        layout.addWidget(self.labelFile)
        self.labelFile.setEnabled(0)    
        self.frame3 = QFrame(self)
        self.frame3.setGeometry(QRect(10, 130, 250, 30))
        self.LabelX = QLabel("X-axis:",self.frame3)
        layout.addWidget(self.LabelX)
        
        self.frame7 = QFrame(self)
        self.frame7.setGeometry(QRect(10, 150, 200, 200))    
        self.senList = QListWidget(self.frame7)
        self.senList.clicked.connect(self.XSelectionChange)

        self.senList.setSelectionMode(QAbstractItemView.NoSelection)
        layout.addWidget(self.senList)
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.senList)
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedHeight(150)
        self.scroll.setFixedWidth(150)
        layout.addWidget(self.scroll)
        self.scroll.move(10,150)
        self.XIndex = None;
        
        self.frame8 = QFrame(self)
        self.frame8.setGeometry(QRect(10, 320, 250, 30))
        self.LabelY = QLabel("Y-axis:",self.frame8)
        layout.addWidget(self.LabelY)
        
        self.frame9 = QFrame(self)
        self.frame9.setGeometry(QRect(10, 360, 200, 200))    
        self.YCols = QListWidget(self.frame9)
        self.YCols.clicked.connect(self.YSelectionChange)
        self.YCols.setSelectionMode(QAbstractItemView.NoSelection)
        layout.addWidget(self.YCols)
        self.scroll2 = QScrollArea(self)
        self.scroll2.setWidget(self.YCols)
        self.scroll2.setWidgetResizable(True)
        self.scroll2.setFixedHeight(150)
        self.scroll2.setFixedWidth(150)
        layout.addWidget(self.scroll2)
        self.scroll2.move(10,360)
        self.YIndex = None;
        
        self.frame10 = QFrame(self)
        self.frame10.setGeometry(QRect(170, 100, 100, 25))
        self.linePropBtn = QPushButton("Plot Properties",self.frame10)
        self.linePropBtn.setChecked(True)
        self.linePropBtn.clicked.connect(self.plotProp)
        layout.addWidget(self.linePropBtn)
        #self.linePropBtn.setEnabled(0)
        
        self.frame11 = QFrame(self)
        self.frame11.setGeometry(QRect(170,125,100,25))
        self.axesBtn = QPushButton("Axes",self.frame11)
        self.axesBtn.clicked.connect(self.axesProp)
        layout.addWidget(self.axesBtn)
        #self.axesBtn.setEnabled(0)

        self.frame12 = QFrame(self)
        self.frame12.setGeometry(QRect(170,150,100,25))
        self.legendBtn = QPushButton("Legend",self.frame12)
        layout.addWidget(self.legendBtn)
        self.legendBtn.clicked.connect(self.legendProp)
        #self.legendBtn.setEnabled(0)
        
        self.frame15 = QFrame(self)
        self.frame15.setGeometry(QRect(170,175,100,25))
        self.gridBtn = QPushButton("Grid",self.frame15)
        layout.addWidget(self.gridBtn)
        self.gridBtn.clicked.connect(self.gridProp)
        #self.gridBtn.setEnabled(0)
        
        self.frame16 = QFrame(self)
        self.frame16.setGeometry(QRect(170,300,100,25))
        self.saveBtn = QPushButton("Save Figure",self.frame16)
        layout.addWidget(self.saveBtn)
        self.saveBtn.clicked.connect(self.openFileSaveDialog)
        self.saveBtn.setEnabled(0)
        
        self.frame17 = QFrame(self)
        self.frame17.setGeometry(QRect(170,200,100,25))
        self.titleBtn = QPushButton("Title",self.frame17)
        layout.addWidget(self.titleBtn)
        self.titleBtn.clicked.connect(self.titleProp)
        #self.titleBtn.setEnabled(0)
        
        self.framexTicks = QFrame(self)
        self.framexTicks.setGeometry(QRect(170,225,100,25))
        self.xTicksBtn = QPushButton("xTicks",self.framexTicks)
        layout.addWidget(self.xTicksBtn)
        self.xTicksBtn.clicked.connect(self.xTicksWProp)

        self.frameyTicks = QFrame(self)
        self.frameyTicks.setGeometry(QRect(170,250,100,25))
        self.yTicksBtn = QPushButton("yTicks",self.frameyTicks)
        layout.addWidget(self.yTicksBtn)
        self.yTicksBtn.clicked.connect(self.yTicksWProp)
        
        self.m = PlotCanvas(self, width=5, height=3)
        self.m.move(270,40)
        self.navi = self.addToolBar(NavigationToolbar(self.m,self))
        #self.navi.move(280,10)
        
        self.plotW = PlotWindow()#self, width=5, height=3)
        self.plotW.move(1,1)
        
        
        self.frame13 = QFrame(self)
        self.frame13.setGeometry(QRect(600,520,120,25))
        self.scriptBtn = QPushButton("Generate Script",self.frame13)
        layout.addWidget(self.scriptBtn)
        self.scriptBtn.clicked.connect(self.genScript)
        self.scriptBtn.setEnabled(0)
        
        self.frame14 = QFrame(self)
        self.frame14.setGeometry(QRect(400,520,120,25))
        self.pltBtn = QPushButton("Plot Data",self.frame14)
        layout.addWidget(self.pltBtn)
        self.pltBtn.clicked.connect(self.plotWindow)
        self.pltBtn.setEnabled(0)
        self.header = 0
        self.legendEnable = True
        #Initialize popup windows 
        self.w=LinePropPopup();  
        self.w.setGeometry(QRect(700,530,400,200)) 
        self.plotAxesProp = AxesPropObject()           
        self.axesW = AxesPopup()
        self.axesW.setGeometry(QRect(700,550,400,180))  
        self.legProp = LegendObject();             
        self.legendW = LegendPopup();
        self.legendW.setGeometry(QRect(700,530,400,200))
        self.gridObject = GridObject();             
        self.gridW = GridPopup();
        self.gridW.setGeometry(QRect(700,530,400,200))
        self.titleObject = TitleObject();             
        self.titleW = TitlePopup();
        self.titleW.setGeometry(QRect(700,530,300,200))
        
        self.headerW = Header();
        self.headerW.setGeometry(QRect(200,200,300,100))
        self.xTicksObject = xTicksPropObject();
        self.yTicksObject = xTicksPropObject();
        self.xTicksW =  xTicksPopup();
        self.xTicksW.setGeometry(QRect(700,530,480,200))
        self.yTicksW =  yTicksPopup();
        self.yTicksW.setGeometry(QRect(700,530,480,200))
    def plotWindow(self):#Callback function to show plot
        self.navi2 = self.plotW.addToolBar(NavigationToolbar(self.plotW,self.plotW))
        self.plotW.setGeometry(QRect(10,10,600,300))
        self.plotW.show()       
    def titleProp(self):#callback function to show title properties window 
        self.titleW.TitlePropShow()
        self.titleW.show();       
    def yTicksWProp(self):#callback function to show y-ticks properties window
        self.yTicksW.yTicksPropShow()        
        self.yTicksW.show();
    def xTicksWProp(self):#callback function to show x-ticks properties window
        self.xTicksW.xTicksPropShow()        
        self.xTicksW.show();
    def genScript(self):#callback function to show generated script window
        self.scriptW = ScriptObject()
        self.scriptW.setGeometry(QRect(10,10,600,300))
        self.scriptW.show()

    def legendProp(self):#callback function to show legend properties window
        self.legendW.LegendPropShow();
        self.legendW.show();
    def axesProp(self):#callback function to show axes properties window
        self.axesW.AxesPropShow();	
        self.axesW.show();
    def gridProp(self):#callback function to show grid properties window
        self.gridW.GridPropShow();	
        self.gridW.show();
    def plotProp(self):#callback function to show line properties window
        self.w.show() 
    def plotDataWithChangedOptions(self):#callback function when the selection of columns is changed
        self.m.clearPlot();self.plotW.clearPlot()
        yColor = []
        self.w.combo1.clear()
        if self.ext == '.csv':
            x = self.d.iloc[:,self.XIndex]
        if (self.ext == '.dat') | (self.ext == '.txt'):
            x = self.d[:,self.XIndex] 
        for i in range(0,len(self.YIndex)):
            pltColor = self.colorSet[(self.YIndex[i])%8]
            if self.colPlotObject[self.YIndex[i]].lineStyle == None: 
                self.colPlotObject[self.YIndex[i]].setLineStyle('solid')
            if self.colPlotObject[self.YIndex[i]].lineColor == None:
                self.colPlotObject[self.YIndex[i]].setLineColor(pltColor) 
                #self.colPlotObject[self.YIndex[i]].setLineStyle('dotted')     
            yColor.insert(i,(pltColor))
            if self.ext == '.csv':
                y = self.d.iloc[:,self.YIndex[i]]
            if (self.ext == '.dat') | (self.ext == '.txt'):
                y = self.d[:,self.YIndex[i]]
            self.m.plotData(x,y,self.colPlotObject[self.YIndex[i]].lineColor,
                                    self.colPlotObject[self.YIndex[i]].lineStyle,
                                    self.colPlotObject[self.YIndex[i]].width,
                                    self.colPlotObject[self.YIndex[i]].drawStyle,
                                    self.colPlotObject[self.YIndex[i]].label,
                                    self.colPlotObject[self.YIndex[i]].marker,
                                    self.colPlotObject[self.YIndex[i]].size, 
                                    self.colPlotObject[self.YIndex[i]].edgeColor,
                                    self.colPlotObject[self.YIndex[i]].faceColor);
            self.plotW.plotData(x,y,self.colPlotObject[self.YIndex[i]].lineColor,
                                    self.colPlotObject[self.YIndex[i]].lineStyle,
                                    self.colPlotObject[self.YIndex[i]].width,
                                    self.colPlotObject[self.YIndex[i]].drawStyle,
                                    self.colPlotObject[self.YIndex[i]].label,
                                    self.colPlotObject[self.YIndex[i]].marker,
                                    self.colPlotObject[self.YIndex[i]].size, 
                                    self.colPlotObject[self.YIndex[i]].edgeColor,
                                    self.colPlotObject[self.YIndex[i]].faceColor);
            self.w.combo1.addItem(self.YCols.item(self.YIndex[i]).text())
            pixmap = QPixmap(10,10);
            pixmap.fill(QColor(self.colPlotObject[self.YIndex[i]].lineColor));
            self.redIcon= QIcon(pixmap);
            self.YCols.item(self.YIndex[i]).setIcon(QIcon(self.redIcon))
        
        if self.legendEnable:
            self.m.showLegend();
            self.plotW.showLegend();
        self.plotAxesProp.setxLabel(self.senList.item(self.XIndex).text())
        
        self.m.getAxesProps();
        self.m.changeAxesProps();
        self.plotW.changeAxesProps();
        self.linePropBtn.setEnabled(1)               
        self.axesBtn.setEnabled(1)
        self.legendBtn.setEnabled(1)
        self.gridBtn.setEnabled(1)
        self.saveBtn.setEnabled(1)
        self.m.changeGridProps();
        self.plotW.changeGridProps();
        self.titleBtn.setEnabled(1)
        self.m.changeTitle()
        self.plotW.changeTitle(); 
        self.m.getxTicks();  
    def XSelectionChange(self):
        #print("Sel change",self.senList.count())
        NoOfItems = self.senList.count()
        #print([self.senList.currentItem().text()])
        prev = self.XIndex;
        listOfXIndex = []
        for i in range(0,NoOfItems):
            item=self.senList.item(i) 
            if item.checkState():
                listOfXIndex.append(i)
        #print(listOfXIndex)
        if len(listOfXIndex)>1:
            for i in range(0,len(listOfXIndex)):
                #print("Loop:",listOfXIndex[i],prev)
                if self.XIndex == listOfXIndex[i]:
                    self.senList.item(listOfXIndex[i]).setCheckState(QtCore.Qt.Unchecked)
                    #print("Unchecked ",listOfXIndex[i])
                else:
                    prev = listOfXIndex[i]
        else:
            if len(listOfXIndex) ==0:
                prev = None
            else:
                prev = listOfXIndex[0]
        
        if self.XIndex != prev:
            self.XIndex = prev
            #print("Changed X:",self.XIndex)
            if self.XIndex == None:
                #print("Cleared Plot")
                self.m.clearPlot()
                self.plotW.clearPlot()
            else:
                self.plotDataWithChangedOptions();
    def YSelectionChange(self):
        NoOfItems = self.YCols.count()
        prev = self.YIndex;
        listOfYIndex = []
        #for i in range(0,len(prev)):
        #    print("rem")
        #    self.w.combo1.removeItem(0)
        for i in range(0,NoOfItems):
            item=self.YCols.item(i) 
            pixmap = QPixmap(10,10);
            pixmap.fill(QColor("white"));
            self.redIcon= QIcon(pixmap);
            self.YCols.item(i).setIcon(QIcon(self.redIcon))
            if item.checkState():
                listOfYIndex.append(i)

        if self.YIndex != listOfYIndex:
            self.YIndex = listOfYIndex	
            yColor = []
            if self.XIndex == None:
                #print("Cleared Plot")
                self.m.clearPlot()
                self.plotW.clearPlot()
                yColor = []
                self.w.combo1.clear()
            else:
                self.plotDataWithChangedOptions();

    def openFileNameDialog(self):#callback function to get browsed data file
        
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog#"All Files (*);;Python Files (*.py)"*.xlsx *.csv
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", ""," *.dat  *.txt", options=options)
        if self.fileName:
            self.ext = self.fileName[self.fileName.rindex('.'):]
            if self.ext =='.csv':
                import pandas as pd
                self.headerW.show();  
        #self.header = int(self.headerW.hBtn.text())
            else:
                self.readFile();
        
    def openFileSaveDialog(self):#callback function to save generated figure
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName1, _ = QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()", 
                            "","*.eps *.dat *.pgf *.pdf *.ps *.raw *.svg *.tiff", options=options)
        print(self.fileName1)
        ax = self.m.fig.axes;
#       added by mbp:
        self.m.fig.tight_layout()

        self.m.fig.savefig(self.fileName1)
    
    def readFile(self):
        NoOfItem =self.senList.count()
        for ic in range(0,NoOfItem):
            #print(ic)
            self.senList.takeItem(0)#self.senList.item(ic));
            self.YCols.takeItem(0);
 
        if self.fileName:
            self.m.clearPlot()
            self.plotW.clearPlot()
            print(self.fileName)
            self.scriptBtn.setEnabled(1)
            self.ext = self.fileName[self.fileName.rindex('.'):]
            self.colPlotObject = [];
            if (self.ext == '.dat') | (self.ext == '.txt'):
                self.d = np.loadtxt(self.fileName)
            if self.ext == '.csv':
                #if self.header == 0:
                self.d = pd.read_csv(self.fileName, header = self.header);
                print( self.d.columns) 
            self.NoOfCol = self.d.shape[1]
            self.total_rows = self.d.shape[0]
                                
                
                          
            for cln in range(0,self.NoOfCol):#self.d.columns:
                if (self.ext == '.dat') | (self.ext == '.txt') | (self.header == 0):  
                    cl = "x"+str(cln)
                else:
                    cl = self.d.columns[cln]
                    print(cl)
                self.colPlotObject.append(PlotObject(cl))
                itm = QListWidgetItem()
                itm.setText(cl)
                itm.setFlags(itm.flags() | QtCore.Qt.ItemIsUserCheckable)
                itm.setCheckState(QtCore.Qt.Unchecked)
                self.senList.addItem(itm)
                itm = QListWidgetItem()
                itm.setText(cl)
                itm.setFlags(itm.flags() | QtCore.Qt.ItemIsUserCheckable)
                itm.setCheckState(QtCore.Qt.Unchecked)
                pixmap = QPixmap(10,10);
                pixmap.fill(QColor("white"));
                self.redIcon= QIcon(pixmap);
                itm.setIcon(self.redIcon)
                self.YCols.addItem(itm)
                 
                
            texC = "Number of columns:"+str(self.NoOfCol)                
            texR = "Number of Rows:"+str(self.total_rows) 
            self.label.setText(texC)
            self.label.setEnabled(1)
            self.labelR.setText(texR)
            self.labelR.setEnabled(1)
            #self.combo.addItem(d.columns[0])
            self.labelFile.setText('File: ...'+self.fileName[len(self.fileName)-25:])
            self.labelFile.setEnabled(1)
            if (self.NoOfCol) >=2:
                self.XIndex = 0;
                self.YIndex = [1];
                self.senList.item(0).setCheckState(QtCore.Qt.Checked)
                self.YCols.item(1).setCheckState(QtCore.Qt.Checked)
                self.colPlotObject[1].setLineColor(self.colorSet[1]) 
                self.pltBtn.setEnabled(1)               
                self.plotDataWithChangedOptions()
                #self.w.combo1.addItem(self.senList.item(1).text())

            

class PlotCanvas(FigureCanvas):
    """
    class to create plot 
    """
    def __init__(self, parent=None, width=5, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height))#, dpi=dpi)     	
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.setGeometry(self,QRect(700,200,525,400))#self)
        FigureCanvas.updateGeometry(self)
        #FigureCanvas.__init__(self, self.fig)
        self.plot()

    def plot(self):
        data = [random.random() for i in range(250)]
        ax = self.fig.add_subplot(111)
        ax.grid()
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")
        self.draw()
    def clearPlot(self):
        ax = self.fig.axes
        for i in range(0,len(ax)):
            axs = ax[i]
            axs.cla()
            axs.grid()
        self.draw()
        
    def plotData(self,x,y,pltColor='red',lineStyle='solid',lineWidth=0.7,drawStyle="default",
                 pltLabel = '',markerStyle ='',markerSize = 7, markerEdgeColor = 'black',markerFaceColor='red'):
        #print("Plotting Data")
        ax = self.fig.axes
        ax =ax[0]
        ax.plot(x,y, color = pltColor,linestyle=lineStyle,linewidth=lineWidth,drawstyle=drawStyle,
                label=pltLabel, marker = markerStyle, markersize = markerSize,
                markeredgecolor = markerEdgeColor,markerfacecolor = markerFaceColor)
        #ax.set_title('PyQt Matplotlib Example ')
        self.draw()
    def showLegend(self):
        ax = self.fig.axes
        ax = ax[0]
        ax.legend(loc = mainWin.legProp.location,frameon = mainWin.legProp.frameon, 
                    fontsize = mainWin.legProp.fontsize, title = mainWin.legProp.title,
                    markerfirst = mainWin.legProp.markerfirst, markerscale = mainWin.legProp.markerscale, 
                    labelspacing = mainWin.legProp.labelspacing, columnspacing = mainWin.legProp.columnspacing)
        self.draw()
        
    def removeLegend(self):
        ax = self.fig.axes
        ax = ax[0]
        ax.get_legend().remove()
        self.draw()
        
    def changeAxesProps(self):
        ax = self.fig.axes
        ax = ax[0]
        #print("changed ax")
        if mainWin.plotAxesProp.xScale != None:
            ax.set_xscale(mainWin.plotAxesProp.xScale)
        if mainWin.plotAxesProp.yScale != None:
            ax.set_yscale(mainWin.plotAxesProp.yScale)
            
        if mainWin.plotAxesProp.xLabel != None:
            ax.set_xlabel(mainWin.plotAxesProp.xLabel)
        if mainWin.plotAxesProp.yLabel != None:
            ax.set_ylabel(mainWin.plotAxesProp.yLabel)
            
        if (mainWin.plotAxesProp.xMin != None) & (mainWin.plotAxesProp.xMax != None):
            ax.set_xlim(left = mainWin.plotAxesProp.xMin, right = mainWin.plotAxesProp.xMax)

        if (mainWin.plotAxesProp.yMin != None) & (mainWin.plotAxesProp.yMax != None):
            ax.set_ylim(bottom = mainWin.plotAxesProp.yMin, top = mainWin.plotAxesProp.yMax)
        
        self.draw()
            
    def getAxesProps(self):
        ax = self.fig.axes
        ax = ax[0]        
        xMin, xMax = ax.get_xlim()
        yMin, yMax = ax.get_ylim()
        
        mainWin.plotAxesProp.setxMin(xMin); 
        mainWin.plotAxesProp.setxMax(xMax);
        mainWin.plotAxesProp.setyMin(yMin);
        mainWin.plotAxesProp.setyMax(yMax);
        
    def changeGridProps(self):
        ax = self.fig.axes
        ax = ax[0]
        #print("changeGridProps") 
        if mainWin.gridObject.gridEnable:
            #ax.grid(b=None)
            ax.grid(b=True,color = mainWin.gridObject.lineColor,
                    linestyle = mainWin.gridObject.lineStyle,
                    axis = mainWin.gridObject.axis,
                    which = mainWin.gridObject.which,
                    linewidth = mainWin.gridObject.width)
        else:
            ax.grid(b=None)

        self.draw()

    def changeTitle(self):
        #print("title",mainWin.titleObject.label)
        ax = self.fig.axes
        ax = ax[0]
        if mainWin.titleObject.titleEnable:
            ax.set_title(label='')
            ax.set_title(label='',loc='left')
            ax.set_title(label='', loc='right')
            ax.set_title(label=mainWin.titleObject.label,loc=mainWin.titleObject.loc)
        else:
            ax.set_title(label='')
        
        self.draw()
        
    def getxTicks(self):
        ax = self.fig.axes
        ax = ax[0]
        mainWin.xTicksObject.setXTicks(list(ax.get_xticks()))
        mainWin.yTicksObject.setXTicks(list(ax.get_yticks()))
        #print(type(ax.get_yticks()),list(ax.get_yticks()))
        bn = []
        for tick in ax.get_xticklabels():
 
            bn+= [str(tick.get_text())]
  
        mainWin.xTicksObject.setXTicksLabels(bn)
        bn = []
        for tick in ax.get_yticklabels():
 
            bn+= [str(tick.get_text())]
        mainWin.yTicksObject.setXTicksLabels(bn)
    def changeXTicks(self):
        ax = self.fig.axes
        ax = ax[0]
        if mainWin.xTicksObject.xTicksEnable:
            ax.set_xticks(mainWin.xTicksObject.xticks)#,mainWin.xTicksObject.direction)
            ax.tick_params(axis='x',direction=mainWin.xTicksObject.direction)
        else:
            ax.set_xticks([])
        self.draw()
    def changeXTicksLabels(self):
        ax = self.fig.axes
        ax = ax[0]
        if mainWin.xTicksObject.xTicksEnable:
            ax.set_xticks(mainWin.xTicksObject.xticks)
            ax.tick_params(axis='x',direction=mainWin.xTicksObject.direction)
            ax.set_xticklabels(mainWin.xTicksObject.xtickslabels,rotation = mainWin.xTicksObject.rotation)
        else:
            ax.set_xticks([])
        self.draw()
    def changeYTicks(self):
        ax = self.fig.axes
        ax = ax[0]
        if mainWin.yTicksObject.xTicksEnable:
            ax.set_yticks(mainWin.yTicksObject.xticks)#,mainWin.xTicksObject.direction)
            ax.tick_params(axis='y',direction=mainWin.yTicksObject.direction)
        else:
            ax.set_yticks([])
        self.draw()
    def changeYTicksLabels(self):
        ax = self.fig.axes
        ax = ax[0]
        if mainWin.yTicksObject.xTicksEnable:
            ax.set_yticks(mainWin.yTicksObject.xticks)
            ax.tick_params(axis='y',direction=mainWin.yTicksObject.direction)
            ax.set_yticklabels(mainWin.yTicksObject.xtickslabels,rotation = mainWin.yTicksObject.rotation)
        else:
            ax.set_yticks([])
        self.draw()    
class PlotWindow(QMainWindow, PlotCanvas):
    def __init__(self):
        super().__init__()
        #self._main = QtWidgets.QWidget()
        #self.setCentralWidget(self._main)
        #layout = QtWidgets.QVBoxLayout(self._main)

        #self.static_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #layout.addWidget(self.static_canvas)
        #self.addToolBar(NavigationToolbar(self.static_canvas, self))

        #dynamic_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        #layout.addWidget(dynamic_canvas)
        #self.addToolBar(QtCore.Qt.BottomToolBarArea,
        #                NavigationToolbar(dynamic_canvas, self))
        #ax = mainWin.m.fig.axes
        #ax = ax[0]
        #self._static_ax = self.static_canvas.figure.subplots()
        #self._static_ax = ax
        #self.static_canvas.draw()
        #static_canvas.draw()
        #t = np.linspace(0, 10, 501)
        #self._static_ax.plot(t, np.tan(t), ".")
    #def InitWindow(self):       
if __name__ == "__main__":
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ApplicationWindow()
    mainWin.show()
    sys.exit( app.exec_())
