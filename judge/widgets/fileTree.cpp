#include "fileTree.h"

#include <QContextMenuEvent>
#include <QDesktopServices>
#include <QHeaderView>
#include <QInputDialog>
#include <QMenu>
#include <QMessageBox>
#include <QUrl>
#include <QVBoxLayout>
#include <qabstractitemmodel.h>
#include <qaction.h>
#include <qboxlayout.h>
#include <qdesktopservices.h>
#include <qdir.h>
#include <qevent.h>
#include <qfilesystemmodel.h>
#include <qinputdialog.h>
#include <qlabel.h>
#include <qlineedit.h>
#include <qmessagebox.h>
#include <qtmetamacros.h>
#include <qtreeview.h>
#include <qwidget.h>

#include "../ide/project.h"
#include "../util/file.h"

FileTreeWidget::FileTreeWidget(QWidget *parent) : QWidget(parent) {
    model = new QFileSystemModel(this);
    headerLabel = new QLabel(this);
    treeView = new QTreeView(this);
    treeView->setModel(model);
    setup();
    connect(treeView, &QTreeView::clicked, this, &FileTreeWidget::clickFile);
    connect(this, &FileTreeWidget::rawOperateFile, this, &FileTreeWidget::handleRawFileOperation);
}

void FileTreeWidget::setRoot(const QString &root) {
    model->setRootPath(root);
    treeView->setRootIndex(model->index(root));

    QString lastDirName = root.split("/").last();
    headerLabel->setText(lastDirName);
}

void FileTreeWidget::addFileOperationToMenu(QMenu &menu, const QString &file, const QString &label,
                                            FileOperation operation) {

    QAction *action = menu.addAction(label);
    for (const auto &shortcut: opShortcuts.keys()) {
        if (operation == opShortcuts.value(shortcut)) {
            action->setShortcut(shortcut);
            break;
        }
    }
    connect(action, &QAction::trigger, this,
            [this, file, operation] { emit rawOperateFile(file, operation); });
}

void FileTreeWidget::setup() {
    treeView->header()->hide();

    for (int i = 1; i < model->columnCount(); ++i) {
        treeView->hideColumn(i);
    }

    headerLabel->setObjectName("headerLabel");

    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(0);

    mainLayout->addWidget(headerLabel);
    mainLayout->addWidget(treeView);

    setLayout(mainLayout);
    setStyleSheet(loadText("qss/fileTree.css"));
}

void FileTreeWidget::contextMenuEvent(QContextMenuEvent *event) {
    QModelIndex index = treeView->currentIndex();
    if (!index.isValid()) {
        return;
    }
    QString filePath = model->filePath(index);
    QMenu menu(this);

    addFileOperationToMenu(menu, filePath, tr("open"), OPEN);
    addFileOperationToMenu(menu, filePath, tr("open locally"), OPEN_LOCALLY);
    addFileOperationToMenu(menu, filePath, tr("rename"), RENAME);
    addFileOperationToMenu(menu, filePath, tr("delete"), DELETE);

    menu.addSeparator();

    if (model->isDir(index)) {
        QAction *newFileAction = menu.addAction(tr("create new file"));
        connect(newFileAction, &QAction::trigger, this,
                [this, filePath] { createNewFile(filePath); });

        QAction *newFolderAction = menu.addAction(tr("create new folder"));
        connect(newFileAction, &QAction::trigger, this,
                [this, filePath] { createNewFolder(filePath); });
    }

    menu.exec(event->globalPos());
}

QMap<Qt::Key, FileOperation> FileTreeWidget::opShortcuts = {
        {Qt::Key_Enter, OPEN},
        {Qt::Key_F1, OPEN_LOCALLY},
        {Qt::Key_F2, RENAME},
        {Qt::Key_Delete, DELETE},
};

void FileTreeWidget::keyPressEvent(QKeyEvent *event) {
    auto key = static_cast<Qt::Key>(event->key());
    if (opShortcuts.contains(key)) {
        QModelIndex index = treeView->currentIndex();
        if (!index.isValid()) {
            return;
        }
        QString filePath = model->filePath(index);
        emit rawOperateFile(filePath, opShortcuts.value(key));
    } else {
        QWidget::keyPressEvent(event);
    }
}

void FileTreeWidget::clickFile(const QModelIndex &index) {
    if (model->isDir(index)) {
        return;
    }
    QString filePath = model->filePath(index);
    emit rawOperateFile(filePath, OPEN);
}

void FileTreeWidget::createNewFile(const QString &dir) {
    bool ok;
    QString fileName = QInputDialog::getText(
            this, tr("create new file"), tr("please input file name:"), QLineEdit::Normal, "", &ok);

    if (ok && !fileName.isEmpty()) {
        QString newFilePath = dir + (dir.endsWith('/') ? "" : "/") + fileName;

        if (QFile::exists(newFilePath)) {
            QMessageBox::warning(this, tr("error"), tr("file exist: %1").arg(newFilePath));
            return;
        }

        QFile file(newFilePath);
        if (file.open(QIODevice::WriteOnly)) {
            file.close();
        } else {
            QMessageBox::warning(this, tr("error"), tr("can not create file: %1").arg(newFilePath));
        }
    }
}

void FileTreeWidget::createNewFolder(const QString &dir) {
    bool ok;
    QString folderName =
            QInputDialog::getText(this, tr("create new folder"), tr("please input folder name:"),
                                  QLineEdit::Normal, "", &ok);

    if (ok && !folderName.isEmpty()) {
        QString newFolderPath = dir + (dir.endsWith('/') ? "" : "/") + folderName;

        if (QDir(newFolderPath).exists()) {
            QMessageBox::warning(this, tr("error"), tr("folder exist: %1").arg(newFolderPath));
            return;
        }

        QDir qDir;
        if (!qDir.mkdir(newFolderPath)) {
            QMessageBox::warning(this, tr("error"),
                                 tr("can not create folder: %1").arg(newFolderPath));
        }
    }
}

void FileTreeWidget::handleRawFileOperation(const QString &filename,
                                            const FileOperation operation) {
    QFileInfo file(filename);
    bool ok = true;

    if (!file.exists()) {
        QMessageBox::warning(this, tr("error"), tr("file not exist: %1").arg(filename));
        return;
    }

    switch (operation) {
        case OPEN: {
            break;
        }
        case OPEN_LOCALLY: {
            QString folderPath = file.isDir() ? filename : file.path();
            ok = QDesktopServices::openUrl(QUrl::fromLocalFile(folderPath));
            if (!ok) {
                QMessageBox::warning(this, tr("error"), tr("can not open dir: %1").arg(folderPath));
            }
            break;
        }

        case RENAME: {
            QString newName =
                    QInputDialog::getText(this, "rename", tr("please input new file name:"),
                                          QLineEdit::Normal, file.fileName(), &ok);
            if (ok && !newName.isEmpty()) {
                QString newPath = file.path() + "/" + newName;
                ok = QFile::rename(filename, newPath);
                if (!ok) {
                    QMessageBox::warning(this, tr("error"), tr("rename fail: %1").arg(filename));
                }
            }
            break;
        }

        case DELETE: {
            QString fileType = file.isDir() ? tr("folder") : tr("file");
            if (QMessageBox::question(this, tr("confirm delete"),
                                      tr("confirm delete %1 ? \n%2").arg(fileType, filename),
                                      QMessageBox::Yes | QMessageBox::No) != QMessageBox::Yes) {
                break;
            }
            ok = file.isDir() ? QDir(filename).removeRecursively() : QFile::remove(filename);
            if (!ok) {
                QMessageBox::warning(this, tr("error"),
                                     tr("can not delete %1: %2").arg(fileType, filename));
            }
            break;
        }

        default:
            QMessageBox::warning(this, tr("error"), tr("unknown operation type"));
            break;
    }

    if (ok) {
        emit operateFile(filename, operation);
    }
}
