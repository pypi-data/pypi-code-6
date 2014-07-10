'''
MAP Client, a program to generate detailed musculoskeletal models for OpenSim.
    Copyright (C) 2012  University of Auckland
    
This file is part of MAP Client. (http://launchpad.net/mapclient)

    MAP Client is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    MAP Client is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with MAP Client.  If not, see <http://www.gnu.org/licenses/>..
'''
from PySide import QtCore, QtGui
from mapclient.widgets.utils import createDefaultImageIcon

class StepTree(QtGui.QTreeWidget):

    def __init__(self, parent=None):
        super(StepTree, self).__init__(parent)
        self.stepIconSize = 64
        self.setStyleSheet("QTreeWidget::item::has-children { \
            background: lightgray; text-align: center;  \
            color: black; border: 2px solid lightgray; \
            padding-bottom: 4px; padding-top: 4px; \
            border-radius: 4px; } \
            QTreeWidget::item::closed { padding-left: 4px;\
            image: url(':/stepbox/images/branch-closed.png') } \
            QTreeWidget::item::closed::has-children { padding-left: 40px;\
            image: url(':/stepbox/images/branch-closed.png') }")

        size = QtCore.QSize(self.stepIconSize, self.stepIconSize)
        self.setIconSize(size)
        self.setColumnCount(1)
        self.setHeaderHidden(True)
        self.setIndentation(0)

        self.setMinimumWidth(250)

    def findParentItem(self, category):
        parentItem = None
        for index in range(self.topLevelItemCount()):
            item = self.topLevelItem(index)
            if item.text(0) == category:
                parentItem = item
                break

        return parentItem

    def addStep(self, step):

        column = 0
        parentItem = self.findParentItem(step._category)
        if not parentItem:
            parentItem = QtGui.QTreeWidgetItem(self)
            parentItem.setText(column, step._category)
            parentItem.setTextAlignment(column, QtCore.Qt.AlignCenter)
            font = parentItem.font(column)
            font.setPointSize(12)
            font.setWeight(QtGui.QFont.Bold)
            parentItem.setFont(column, font)

        if not parentItem.isExpanded():
            parentItem.setExpanded(True)

        stepItem = QtGui.QTreeWidgetItem(parentItem)
        stepItem.setText(column, step.getName())
        if step._icon:
            stepItem.setIcon(column, QtGui.QIcon(QtGui.QPixmap.fromImage(step._icon)))
        else:
            stepItem.setIcon(column, QtGui.QIcon(QtGui.QPixmap.fromImage(createDefaultImageIcon(step.getName()))))

        stepItem.setData(column, QtCore.Qt.UserRole, step)
        stepItem.setFlags(QtCore.Qt.ItemIsEnabled)

    def mousePressEvent(self, event):
        item = self.itemAt(event.pos())
        if not item:
            return None

        if self.indexOfTopLevelItem(item) >= 0:
            # Item is a top level item and it doesn't have drag and drop abilities
            return QtGui.QTreeWidget.mousePressEvent(self, event)

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        step = item.data(0, QtCore.Qt.UserRole)
        if step._icon:
            pixmap = QtGui.QPixmap(step._icon)
        else:
            icon = createDefaultImageIcon(step.getName())
            pixmap = QtGui.QPixmap()
            pixmap.convertFromImage(icon)

        pixmap = pixmap.scaled(64, 64, aspectRatioMode=QtCore.Qt.KeepAspectRatio, transformMode=QtCore.Qt.FastTransformation)
        hotspot = QtCore.QPoint(pixmap.width() / 2, pixmap.height() / 2)

        name = step.getName()  # bytearray(step.getName(), sys.stdout.encoding)
        dataStream.writeUInt32(len(name))
        dataStream.writeRawData(name)

        dataStream << hotspot

        mimeData = QtCore.QMimeData()
        mimeData.setData('image/x-workflow-step', itemData)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(hotspot)
        drag.setPixmap(pixmap)

        drag.exec_(QtCore.Qt.MoveAction)

        return QtGui.QTreeWidget.mousePressEvent(self, event)
