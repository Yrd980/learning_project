#include "terminal.h"
#include <qboxlayout.h>
#include <qjsonvalue.h>
#include <qtermwidget.h>
#include <qtermwidget_interface.h>
#include <qtmetamacros.h>
#include <qwidget.h>
#include "../util/file.h"

class MyShell : public QTermWidget {
    Q_OBJECT

private slots:
    void setFont(const QJsonValue &fontJson) {

        QJsonObject obj = fontJson.toObject();
        QFont font;
        font.setFamily(obj["family"].toString());
        font.setPointSize(obj["size"].toInt() - 3); // a little smaller
        setTerminalFont(font);
    }

    void setColorScheme(const QString &name) override { QTermWidget::setColorScheme(name); }

    void setup() {
        Configs::bindHotUpdateOn(this, "codeFont", &MyShell::setFont);
        Configs::instance().manuallyUpdate("codeFont");
        Configs::bindHotUpdateOn(this, "terminalTheme", &MyShell::setColorScheme);
        Configs::instance().manuallyUpdate("terminalTheme");
        setScrollBarPosition(ScrollBarRight);
    }

public:
    explicit MyShell(QWidget *parent = nullptr) : QTermWidget(parent) { setup(); }
};

TerminalWidget::TerminalWidget(QWidget *parent) :
    QWidget(parent), project(nullptr), shell(nullptr) {
    layout = new QVBoxLayout(this);
    this->setLayout(layout);
}

void TerminalWidget::newTerminal() {
    if (shell) {
        layout->removeWidget(shell);
        delete shell;
    }

    shell = new MyShell(this);

    runCmd(Command::changeDirectory(project->getRoot()));
    runCmd(Command::clearScreen());
    layout->addWidget(shell);

    connect(shell, &QTermWidget::finished, this, &TerminalWidget::newTerminal);
}

void TerminalWidget::setProject(const Project *project) {
    this->project = project;
    newTerminal();
}

void TerminalWidget::runCmd(const Command &command) const { shell->sendText(command.text()); }

#include "terminal.moc"
