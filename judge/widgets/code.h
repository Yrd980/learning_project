#ifndef CODE_EDIT_H
#define CODE_EDIT_H

#include <QListWidget>
#include <QPlainTextEdit>
#include <qcorotask.h>
#include <qlistwidget.h>
#include <qtmetamacros.h>

#include "../ide/highlighter.h"
#include "../ide/lsp.h"
#include "../ide/project.h"
#include "fileTree.h"

class CodeEditWidget;

class CompletionList : public QListWidget {

    CodeEditWidget *codeEdit;
    QList<CompletionItem> completions;

    Q_OBJECT

    void onItemClicked(const QListWidgetItem *item);
    void updateHeight();
    void addCompletionItem(const CompletionItem &item);

protected:
    void keyPressEvent(QKeyEvent *e) override;

private slots:

signals:
    void completionSelected(const QString &completion);

public:
    explicit CompletionList(CodeEditWidget *codeEdit);
    void readCompletions(const CompletionResponse &response);
    void update(const QString &curWord);
    void display();
};

class LineNumberArea : public QWidget {
    CodeEditWidget *codeEdit;

public:
    static const int L_MARGIN;
    static const int R_MARGIN;

    explicit LineNumberArea(CodeEditWidget *codeEdit);
    int getWidth() const;
    QSize sizeHint() const override;

protected:
    void paintEvent(QPaintEvent *event) override;
};

class WelcomeWidget : public QWidget {
    Q_OBJECT
    void setup();

public:
    explicit WelcomeWidget(QWidget *parent);
};

class CodeEditWidget : public QPlainTextEdit {
    Q_OBJECT

    friend class LineNumberArea;
    friend class CompletionList;

    LangFileInfo file;
    Highlighter *highlighter;
    LanguageServer *server;
    CompletionList *cl;
    LineNumberArea *lna;

    bool modified;
    bool requireCompletion;

    void setup();

private slots:

    QCoro::Task<> onSetupFinished();

    void onSetFont(const QJsonValue &value);

    void adaptViewport();

    void updateLineNumberArea(const QRect &rect, int dy);

    void highlightLine();

    void updateCursorPosition() const;

    QCoro::Task<> askForCompletion() const;

    void updateCompletionList();

    void insertCompletion(const QString &completion);

    void onToggleComment();

    QCoro::Task<> askForDefinition();

signals:
    void setupFinished();
    void modify();
    void toggleComment();
    void jumpToDefinition();
    void jumpTo(QUrl url, int startLine, int startChar, int endLine, int endChar);

protected:
    void resizeEvent(QResizeEvent *event) override;
    void keyPressEvent(QKeyEvent *e) override;
    void mousePressEvent(QMouseEvent *event) override;

public:
    explicit CodeEditWidget(const QString &filename, QWidget *parent = nullptr);

    const LangFileInfo &getFile() const;
    QString getTabText() const;
    void readFile();
    void saveFile();
    bool askForSave();
    void cursorMoveTo(int startLine, int startChar, int endLine, int endChar);
};

class CodeTabWidget : public QTabWidget {
    Q_OBJECT

    Project *project = nullptr;
    QMutex tabMutex;

    void setup();
    void welcome();
    CodeEditWidget *addCodeEdit(const QString &filePath);
    void checkRemoveCodeEdit(const QString &filename);

public slots:
    void handleFileOperation(const QString &filename, FileOperation operation);
    void removeCodeEdit(int index);
    void removeCodeEditRequested(int index);
    void widgetModified(int index);
    void onCurrentTabChanged(int index) const;
    void jumpTo(const QUrl &url, int startLine, int startChar, int endLine, int endChar);

public:
    explicit CodeTabWidget(QWidget *parent);
    void setProject(Project *project);
    void clearAll();
    LangFileInfo currentFile() const;
    CodeEditWidget *curEdit() const;
    CodeEditWidget *editAt(int index) const;
    void save();
};


#endif // CODE_EDIT_H
