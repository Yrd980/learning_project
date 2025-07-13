#ifndef IDE_MAIN_WINDOW_H
#define IDE_MAIN_WINDOW_H

#include <QMainWindow>
#include <qmainwindow.h>
#include <qtmetamacros.h>

#include "../ide/ide.h"
#include "aiAssistant.h"
#include "code.h"
#include "fileTree.h"
#include "footer.h"
#include "iconNav.h"
#include "menu.h"
#include "preview.h"
#include "terminal.h"

class IDEMainWindow : public QMainWindow {
    Q_OBJECT

    IDE *ide;

    LeftIconNavigateWidget *leftNav;
    RightIconNavigateWidget *rightNav;
    FileTreeWidget *fileTree;
    TerminalWidget *terminal;
    CodeTabWidget *codeTab;
    MenuBarWidget *menuBar;
    OpenJudgePreviewWidget *ojPreview;
    FooterWidget *footer;
    AIAssistantWidget *aiAssistant;

    void setup();
    void connectSignals();

public:
    explicit IDEMainWindow(QWidget *parent = nullptr);

public slots:
    void openFolder(const QString &folder) const;
    void openSettings();
    void runCurrentCode() const;
    void submitCurrentCode() const;
    void openPersonalSettings();
};

#endif // IDE_MAIN_WINDOW_H
