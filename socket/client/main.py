#!/usr/bin/python3

import sys, os

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import threading
from time import sleep
from multiprocessing import Value

from socket import *
from gen import *
from get import *
from put import *
from Client import *

clientDebug = print
tftpSql = None
loginIsSuccess = False
windownName = 'FTFP Super Tools'
defaultLocalDir = '/tmp'
defaultDirName = 'tftpDisk_'

class userInfos:
    def __init__(self, name = '', passWord = ''):
        self.setUserName(name, passWord)
        self.age = 0
        self.sex = 'M'
        self.isLoginSuccess = False

    def getUserName(self):
        return self.name

    def setUserName(self, name, passWord):
        self.name = name
        self.passWord = passWord

# QMainWindow是QWidget的派生类
class loginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # statusBar设置
        self.statusBar().showMessage('All ready')

        # 退出Action设置
        exitAction = QAction(QIcon('1.png'), '&Exit', self)
        exitAction.setShortcut('ctrl+Q')
        exitAction.setStatusTip('Exit app')
        exitAction.triggered.connect(qApp.quit)     # qApp就相当于QCoreApplication.instance()

        # menuBar设置
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # toolBar设置
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        # 确认PushButton设置
        self.btnOK = QPushButton("LogIn")
        self.btnOK.setToolTip("confirm to all right!")
        self.btnOK.setStatusTip("Click to login...")
        self.btnOK.clicked.connect(self.funLogin)
        self.btnOK.resize(self.btnOK.sizeHint())

        # 取消PushButton设置
        btnCancel = QPushButton("Clear")
        btnCancel.setToolTip("Click to change!")
        btnCancel.setStatusTip("Click to give up!")
        btnCancel.clicked.connect(self.funCancel)
        btnCancel.resize(btnCancel.sizeHint())

        # 退出PushButton设置
        btnQuit = QPushButton('Quit')
        btnQuit.setToolTip("Click to quit！")
        btnQuit.setStatusTip("Click to quit App")
        btnQuit.clicked.connect(qApp.quit)
        btnQuit.resize(btnQuit.sizeHint())

        # 更改提示PushButton设置
        btnRegister = QPushButton('Register')
        btnRegister.setToolTip("Click to register!")
        btnRegister.setStatusTip("Click to change!")
        btnRegister.clicked.connect(self.funRegister)
        btnRegister.resize(btnRegister.sizeHint())

        # PushButton布局
        hBox1 = QHBoxLayout()
        hBox1.addStretch(1)
        hBox1.addWidget(btnRegister)
        hBox1.addWidget(self.btnOK)
        hBox1.addWidget(btnCancel)
        # hBox1.addWidget(btnQuit)

        # QTextBrwoser是只读的多行文本框，既可以显示普通文本，又可以显示HTML
        self.textBrowser = QTextBrowser()
        # 提示标签
        self.labTipUname = QLabel("User Name:")
        self.labTipPword = QLabel("Pass Word: ")
        # 单行文本框
        self.userNameEdit = QLineEdit()
        self.userNameEdit.selectAll()
        self.userNameEdit.returnPressed.connect(self.funLogin)

        # Pass word editer
        self.passWordEdit = QLineEdit()
        self.passWordEdit.selectAll()
        # self.passWordEdit.setEchoMode(self, 2)
        self.passWordEdit.returnPressed.connect(self.funLogin)

        # 布局
        hBox2 = QHBoxLayout()
        hBox2.addWidget(self.labTipUname)
        hBox2.addWidget(self.userNameEdit)

        hBox3 = QHBoxLayout()
        hBox3.addWidget(self.labTipPword)
        hBox3.addWidget(self.passWordEdit)

        # 布局
        vBox = QVBoxLayout()
        # vBox.addWidget(self.textBrowser)
        # vBox.addWidget(self.userNameEdit)
        vBox.addLayout(hBox2)
        vBox.addLayout(hBox3)
        vBox.addLayout(hBox1)
        widget = QWidget()
        self.setCentralWidget(widget)  # 建立的widget在窗体的中间位置
        widget.setLayout(vBox)

        # 布局完毕后，才可得到焦点
        self.userNameEdit.setFocus()
        self.passWordEdit.setFocus()

        self.isWantClose = False

        # Window设置
        self.resize(400, 200)
        self.setFixedSize(400, 200)
        self.center()
        self.setFont(QFont('华文楷体', 10))
        self.setWindowTitle(windownName)
        self.setWindowIcon(QIcon('10.png'))

    def center(self):
        # 得到主窗体的框架信息
        qr = self.frameGeometry()
        # 得到桌面的中心
        cp = QDesktopWidget().availableGeometry().center()
        # 框架的中心与桌面中心对齐
        qr.moveCenter(cp)
        # 自身窗体的左上角与框架的左上角对齐
        self.move(qr.topLeft())

    def funLogin(self):
        textUserName = self.userNameEdit.text()
        textPassWord = self.passWordEdit.text()
        clientDebug('funLogin, textUserName = %s' % textUserName)
        clientDebug('funLogin, textPassWord = %s' % textPassWord)

        if not self.sqlObject:
            clientDebug('Not sqlObject, login failed!')
        # Call Msql module
        ret = self.sqlObject.mysqlLogin(textUserName, textPassWord)
        clientDebug('Login ret = %d' % ret)
        if ret:
            self.userInfo.isLoginSuccess = False
        else:
            self.userInfo.setUserName(textUserName, textPassWord)
            self.userInfo.isLoginSuccess = True
            loginIsSuccess = True
            self.isWantClose = True
            self.close()
        clientDebug('loginIsSuccess1 = %d' % self.userInfo.isLoginSuccess)

    def funRegister(self):
        textUserName = self.userNameEdit.text()
        textPassWord = self.passWordEdit.text()
        clientDebug('funRegister, textUserName = %s' % textUserName)
        clientDebug('funRegister, textPassWord = %s' % textPassWord)

        if not self.sqlObject:
            clientDebug('Not sqlObject, register failed!')
        ret = self.sqlObject.mysqlRigester(textUserName, textPassWord)
        clientDebug('Register ret = %d' % (ret))
        if ret:
            clientDebug('Register error, ret = %d' % ret)
        else:
            self.userInfo.setUserName(textUserName, textPassWord)
            self.userInfo.isLoginSuccess = True
            self.isWantClose = True
            self.close()

    def funCancel(self):
        self.userNameEdit.clear()
        self.passWordEdit.clear() 

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()

    def closeEvent(self, QCloseEvent):
        if self.isWantClose:
            QCloseEvent.accept()
            return
        else:
            global loginIsSuccess
            reply = QMessageBox.question(self, windownName,'Do you want to exit?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                QCloseEvent.accept()
            else:
                QCloseEvent.ignore()
            loginIsSuccess = False
        return

    def setUserObject(self, userInfoObject):
        self.userInfo = userInfoObject

    def setSqlObject(self, sqlObject):
        self.sqlObject = sqlObject

def __setPgbarChange(pMemShare, pgbar, button, fileName):
    pbak = -1
    while True:
        p = pMemShare.value
        if pbak != p:
            print('%s __setPgbarChange: %d' % (fileName, p))
            pbak = p
            pgbar.setValue(p)
        if p == 100:
            break

Client = None
def doDownload(fileName, pgbar, button):
    pMemShare = Value('i', 0)
    print(fileName)
    ftp_client.get(fileName, pMemShare)
    th = threading.Thread(target=__setPgbarChange, args=(pMemShare, pgbar, button, fileName))
    th.daemon = True
    th.start()

def dols(fileName, pgbar, button):
    pMemShare = Value('i', 0)
    ftp_client.cd(fileName, pMemShare)
    th = threading.Thread(target=__setPgbarChange, args=(pMemShare, pgbar, button, fileName))
    th.daemon = True
    th.start()

def doupload(fileName, pgbar):
    def pgbarChange(x):
        pgbar.setValue(x)
    ftp_client.put(fileName, pgbarChange)

'''
Add by Huangxiaowen(AID1803)
'''
class MyMainWidget(QMainWindow):
    def __init__(self, parent=None, userInfoObject=None):
        QWidget.__init__(self, parent)
        super().__init__()

        self.setUserObject(userInfoObject)
        self.statusBar().showMessage('Ready...')
        # 退出Action设置
        exitAction = QAction(QIcon('1.png'), '&Exit', self)
        exitAction.setShortcut('ctrl+Q')
        exitAction.setStatusTip('Exit app')
        exitAction.triggered.connect(qApp.quit)     # qApp就相当于QCoreApplication.instance()

        # menuBar设置
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        # toolBar设置
        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        self.setWindowTitle('TreeWidget')
        # 创建一个Qtree部件
        self.fileTree = QTreeWidget()
        # 设置部件的列数为2
        self.rowNum = 4
        self.fileTree.setColumnCount(self.rowNum)
        # 设置头部信息，因为上面设置列数为2，所以要设置两个标识符
        self.fileTree.setHeaderLabels(['Name', 'Size', 'Type', 'Date Modifed'])

        self.fileTree.itemSelectionChanged.connect(self.myItemSelectionChanged)
        self.fileTree.customContextMenuRequested[QPoint].connect(self.myOneItemMenu)
        self.fileTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.fileTree.resizeColumnToContents(1)
        self.fileTree.setSortingEnabled(True)
        # self.fileTree.setHeaderLabel('Remote Disk')

        # 设置root为self.fileTree的子树，所以root就是跟节点
        self.root = QTreeWidgetItem(self.fileTree)
        self.fileTree.addTopLevelItem(self.root)
        # 将fileTree部件设置为该窗口的核心框架
        self.setCentralWidget(self.fileTree)

        # model = QDirModel()
        self.userLocalDir = defaultLocalDir + '/' + defaultDirName + self.userInfosObject.name
        clientDebug('userLocalDir: ', self.userLocalDir)
        if not os.path.exists(self.userLocalDir):
            os.mkdir(self.userLocalDir)

        model = QFileSystemModel()
        model.setRootPath(QDir.currentPath())
        selModel = QItemSelectionModel(model)
        self.dirTree = QTreeView()
        self.dirTree.setModel(model)
        self.dirTree.setSelectionModel(selModel)
        self.dirTree.customContextMenuRequested[QPoint].connect(self.myDirItemMenu)
        self.dirTree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.dirTree.resizeColumnToContents(0)
        self.dirTree.setSortingEnabled(True)
        # self.dirTree.setRootIndex(model.index(self.userLocalDir))

        self.fileTable = QTableWidget(0, 5)
        # self.fileTable.setModel(model)
        self.fileTable.setHorizontalHeaderLabels(['Name', 'Size', 'Time', 'Progress', 'Operation'])
        self.fileTable.horizontalHeader().setStretchLastSection(True)
        self.fileTable.setSelectionBehavior(QAbstractItemView.SelectRows)  # 设置鼠标选择行为：一个单元格/一行/一列
        # self.fileTable.setFrameShape(QFrame.NoFrame)    # 设置无边框
        self.fileTable.verticalHeader().hide()          # 设置垂直的头部隐藏，不隐藏默认会显示列表数字
        self.fileTable.horizontalHeader().resizeSection(0, 150)        # 设置第0列的宽度为150px
        # self.fileTable.setItemDelegate(NoFocusDelegate())          # 设置鼠标行时，不显示单元格虚框，NoFocusDelegate类实现如附录
        self.fileTable.setMouseTracking(True)                          # 设置鼠标捕捉，不设置，如鼠标进入等动作检测不到
        self.fileTable.setStyleSheet("selection-background-color:lightblue;")  # 设置行选中时背景颜色
        self.fileTable.horizontalHeader().setStyleSheet("QHeaderView.section{background:greenyellow;}") # 表头背景颜色
        self.fileTable.horizontalHeader().font().setBold(False)
        self.fileTable.setEditTriggers(QAbstractItemView.NoEditTriggers)    # 设置不可编辑

        self.fileTableColumnName = 0
        self.fileTableColumnSize = 1
        self.fileTableColumnTime = 2
        self.fileTableColumnProgress = 3
        self.fileTableColumnOperation = 4

        self.splitter = QSplitter()
        self.splitter.addWidget(self.dirTree)
        self.splitter.addWidget(self.fileTree)
        self.splitter.addWidget(self.fileTable)
        self.splitter.setWindowTitle(self.splitter.tr("Model/View"))
        self.splitter.resize(1200, 500)
        self.resize(1200, 500)
        # self.splitter.show()

        self.tabWidget = QTabWidget()
        # self.tabWidget.addTab(self.splitter, 'Cloud disk')

        # tftp connect infos
        # self.tftpRemoteLabel = QLabel('IP:')
        # self.tftpPassWordLabel = QLabel('   Pass Word:')
        # self.tftpRemoteEdit = QLineEdit()
        # self.tftpPassWordEdit = QLineEdit()
        # self.tftpConnectButton = QPushButton('Connet')
        self.cloudDiskVBox = QVBoxLayout()
        # self.cloudDiskHBox = QHBoxLayout()
        #
        # self.cloudDiskHBox.addWidget(self.tftpRemoteLabel)
        # self.cloudDiskHBox.addWidget(self.tftpRemoteEdit)
        # self.cloudDiskHBox.addWidget(self.tftpPassWordLabel)
        # self.cloudDiskHBox.addWidget(self.tftpPassWordEdit)
        # self.cloudDiskHBox.addWidget(self.tftpConnectButton)
        # self.cloudDiskVBox.addLayout

        # self.cloudDiskVBox.addLayout(self.cloudDiskHBox)
        self.cloudDiskVBox.addWidget(self.splitter)

        # User informations
        self.userVBox0 = QVBoxLayout()
        self.userHBox0 = QHBoxLayout()
        self.userHBox1 = QHBoxLayout()
        self.userHBox2 = QHBoxLayout()
        self.userHBox3 = QHBoxLayout()

        self.userNameLabel = QLabel('Name:')
        self.userSexLabel = QLabel('Sex:')
        self.userAgeLabel = QLabel('Age:')
        self.userLocalDirLabel = QLabel('Local:')
        self.userNameComment = QLabel(self.userInfosObject.name)
        self.userSexComment = QLabel(self.userInfosObject.sex)
        self.userAgeComment = QLabel(str(self.userInfosObject.age))
        self.userLocalDirComment = QLabel(self.userLocalDir)
        self.userHBox0.addWidget(self.userNameLabel)
        self.userHBox0.addWidget(self.userNameComment)
        self.userHBox0.addStretch()     # 在第一个控件之后添加伸缩，这样所有的控件就会居左显示。

        self.userHBox1.addWidget(self.userSexLabel)
        self.userHBox1.addWidget(self.userSexComment)
        self.userHBox1.addStretch()     # 在第一个控件之后添加伸缩，这样所有的控件就会居左显示。

        self.userHBox2.addWidget(self.userAgeLabel)
        self.userHBox2.addWidget(self.userAgeComment)
        self.userHBox2.addStretch()     # 在第一个控件之后添加伸缩，这样所有的控件就会居左显示。

        self.userHBox3.addWidget(self.userLocalDirLabel)
        self.userHBox3.addWidget(self.userLocalDirComment)
        self.userHBox3.addStretch()     # 在第一个控件之后添加伸缩，这样所有的控件就会居左显示。

        self.userVBox0.addLayout(self.userHBox0)
        self.userVBox0.addLayout(self.userHBox1)
        self.userVBox0.addLayout(self.userHBox2)
        self.userVBox0.addLayout(self.userHBox3)
        self.userVBox0.addStretch()

        # Set splitter to type Widget
        cashUserWidget = QWidget()
        cashUserWidget.setLayout(self.userVBox0)
        cashDiskWidget = QWidget()
        cashDiskWidget.setLayout(self.cloudDiskVBox)

        self.tabWidget.addTab(cashUserWidget, 'User informations')
        self.tabWidget.addTab(cashDiskWidget, 'Cloud Disk')
        self.tabWidget.show()

    def myOneItemMenu(self, point):
        getSelected = self.fileTree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            fileType = baseNode.text(2)
            clientDebug('point = ', point)
            popMenu = QMenu()
            if 'folder' == fileType:
                popMenu.addAction(QAction('Extend', self, triggered=self.mySelectExtend))
            popMenu.addAction(QAction('Download', self, triggered=self.mySelectDownload))
            popMenu.addAction(QAction('Delete', self, triggered=self.mySelectDelete))
            popMenu.addAction(QAction('Rename', self, triggered=self.mySelectRename))
            popMenu.exec_(QCursor.pos())

    def myDirItemMenu(self, point):
        popMenu = QMenu()
        popMenu.addAction(QAction('Upload', self, triggered=self.mySelectUpload))
        popMenu.exec_(QCursor.pos())

    def myItemSelectionChanged(self):
        getSelected = self.fileTree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            clientDebug(getChildNode)

    def mySelectUpload(self):
        getSelected = self.dirTree.currentIndex()
        print("====",getSelected)
        if getSelected:
            # baseNode = getSelected[0]
            # getChildNode = baseNode.text(0)           
            clientDebug('Select to upload: ', str(getSelected.data()))
            file_get = "put %s"%str(getSelected.data())
            print("++++",file_get)
            # item = [baseNode.text(0), baseNode.text(1), baseNode.text(2)]
            # pgbar = self.addDownloadTableWidget(item)
            # doupload(file_get, pgbar)

    def mySelectDownload(self):
        getSelected = self.fileTree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            print('Select to download: ', getChildNode)
            item = [baseNode.text(0), baseNode.text(1), baseNode.text(2)]

            pgbar, button = self.addDownloadTableWidget(item)

            fullPath = ''
            listPath = []
            parenNode = baseNode
            while True:
                listPath.append(parenNode.text(0))
                parenNode = parenNode.parent()
                if not parenNode:
                    break
            for p in listPath[::-1]:
                fullPath += p + '/'
            fileGet = ("get %s" % fullPath)[::-1].split('/', 1)[-1][::-1]
            print(fileGet)
            doDownload(fileGet, pgbar, button)

            # pgbar = self.addDownloadTableWidget(item)
            # doDownload(fileGet, pgbar)


    def mySelectExtend(self):
        getSelected = self.fileTree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            fileType = baseNode.text(2)
            if 'folder' != fileType:
                return

            fullPath = ''
            listPath = []
            parenNode = baseNode

            while True:
                listPath.append(parenNode.text(0))
                parenNode = parenNode.parent()
                if not parenNode:
                    break
            print("listPath",listPath)
            for p in listPath[::-1]:
                fullPath += p + '/'
            print('Want to extand: ', fullPath)
            fileLs = "cd %s" % fullPath
            print(fileLs)
            filels = ftp_client.cd(fileLs)      #corecore/__pycache__

            for l in filels:
                newChild = QTreeWidgetItem(baseNode)
                for i in range(0, self.rowNum):
                    newChild.setText(i, l[i])
        return

    def mySelectDelete(self):
        isDeleteOK = False
        getSelected = self.fileTree.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            clientDebug('Select to Delete: ', getChildNode)
            fileLs = "rm %s" % getChildNode
            reply = QMessageBox.warning(self,
                                        "Warning",
                                        "Do you want to delete file '%s'?" % getChildNode,
                                        QMessageBox.Yes | QMessageBox.No)
            clientDebug('reply = ', reply)
            if reply == 16384:          # QMessageBox.Yes value is 16384
                ret = ftp_client.rm(fileLs)
                clientDebug('ftp_client.rm ret: ', ret)
                if ret:
                    parentNode = baseNode.parent()
                    ret = parentNode.takeChild(parentNode.indexOfChild(baseNode))
                    clientDebug('takeChild ret: ', ret)
        return isDeleteOK

    def mySelectRename(self):
        getSelected = self.fileTree.selectedItems()
        print('sadf: ', getSelected)
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(0)
            clientDebug('Select to Rename: ', getChildNode)
            value, ok = QInputDialog.getText(self, 'Rename', 'Edite new name:', QLineEdit.Normal, getChildNode)
            clientDebug(value, ok)
            if ok:
                baseNode.setText(0, value)

    def myUpdataOneItems(self, childRoot, childList):
        if not childRoot or not childList:
            return

        newChild = None
        for item in childList:
            newChild = QTreeWidgetItem(childRoot)
            clientDebug('newChild: ', type(newChild))
            for i in range(0, self.rowNum):
                newChild.setText(i, item[i])
        return

    def myExtendOneItems(self):
        pass

    def myInitAllItems(self, rootList, childList):
        # 设置根节点的名称
        self.root.setText(0, rootList[0])
        # 为root节点设置子结点
        self.myUpdataOneItems(self.root, childList)

    def setUserObject(self, userInfos):
        self.userInfosObject = userInfos

    def addDownloadTableWidget(self, rowInfoList):
        rowCount = self.fileTable.rowCount()    # 获取表单行数
        clientDebug('rowCount = %d' % rowCount)

        self.fileTable.insertRow(rowCount)     # 插入新行
        item0 = QTableWidgetItem(rowInfoList[self.fileTableColumnName])
        item1 = QTableWidgetItem(rowInfoList[self.fileTableColumnSize])
        item2 = QTableWidgetItem(rowInfoList[self.fileTableColumnTime])
        # item0.setIcon(icon)     # icon为调用系统的图标，以后缀来区分

        self.fileTable.setItem(rowCount, self.fileTableColumnName, item0)
        self.fileTable.setItem(rowCount, self.fileTableColumnSize, item1)
        self.fileTable.setItem(rowCount, self.fileTableColumnTime, item2)

        pgbar = QProgressBar(self)
        # 添加构件到单元格，如按钮，进度条等
        pgbar = QProgressBar(self)
        pgbar.setTextVisible(False)
        pgbar.setMinimum(0)    # 最小值
        pgbar.setMaximum(100)  # 最大值
        pgbar.setValue(0)
        self.fileTable.setCellWidget(rowCount, self.fileTableColumnProgress, pgbar)   # 替换当前widget

        btnOpt = QPushButton()
        btnOpt.setText('Start')
        btnOpt.clicked.connect(self.downloadClickStart)
        self.fileTable.setCellWidget(rowCount, self.fileTableColumnOperation, btnOpt)  # 替换当前widget

        return (pgbar, btnOpt)

    def downloadClickStart(self):
        getSelected = self.fileTable.currentIndex()
        senderObj = QObject.sender(self)
        idx = self.fileTable.indexAt(QPoint(senderObj.frameGeometry().x(), senderObj.frameGeometry().y()))
        print('Row: %d, Column: %d' % (idx.row(), idx.column()))
        button = self.fileTable.cellWidget(idx.row(), idx.column())
        text = button.text()
        changToText = None
        if text == 'Start':
            changToText = 'Stop'
        elif text == 'Stop':
            changToText = 'Start'
        button.setText(changToText)


user = userInfos()
main = None

def main():
    tftpSql = TftpMysql("localhost", 3306, "user", "root", "xiao404040")
    tftpSql.open()

    app = QApplication(sys.argv)
    login = loginWindow()
    login.setUserObject(user)
    login.setSqlObject(tftpSql)
    login.show()
    app.exec_()

    clientDebug('loginIsOK: %d, userName: %s, password: %s' % (loginIsSuccess, user.name, user.passWord))
    if not user.isLoginSuccess:
        tftpSql.close()
        sys.exit()

    global ftp_client
    ftp_client = FtpClient()
    ftp_client.connect("127.0.0.1",8889)
    fileList = ftp_client.list_()
    main = MyMainWidget(userInfoObject = user)
    # ftp_client.setFileRoot(main.userLocalDir)
    main.myInitAllItems(['', '', '', ''], fileList)
    main.tabWidget.show()
    app.exec_()

    tftpSql.close()
    sys.exit()

if __name__ == '__main__':
    main()
