#ifndef FILETREE_H
#define FILETREE_H

#include <QFileSystemModel>
#include <QLabel>
#include <QTreeView>

enum FileOperation { OPEN, OPEN_LOCALLY, RENAME, DELETE };

class FileTreeWidget : public QWidget {
    Q_OBJECT

    QTreeView *treeView;
    QFileSystemModel *model;
    QLabel *headerLabel;

    void setup();
    void addFileOperationToMenu(QMenu &menu, const QString &file, const QString &label,
                                FileOperation operation);

signals:
    void rawOperateFile(const QString &filename, FileOperation operation);
    void operateFile(const QString &filename, FileOperation operation);

private slots:
    void clickFile(const QModelIndex &index);
    void handleRawFileOperation(const QString &filename, FileOperation operation);

public slots:
    void createNewFile(const QString &dir);
    void createNewFolder(const QString &dir);

protected:
    void contextMenuEvent(QContextMenuEvent *event) override;
    void keyPressEvent(QKeyEvent *event) override;

public:
    static QMap<Qt::Key, FileOperation> opShortcuts;

    explicit FileTreeWidget(QWidget *parent = nullptr);
    void setRoot(const QString &root);
};


#endif // FILETREE_H
