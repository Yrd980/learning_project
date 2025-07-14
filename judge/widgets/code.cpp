#include <QFile>
#include <QMessageBox>
#include <QPainter>
#include <QVBoxLayout>

#include "../ide/lsp.h"
#include "../util/file.h"
#include "code.h"

#include <QThread>
#include <QTimer>
#include <qabstractitemview.h>
#include <qboxlayout.h>
#include <qcolor.h>
#include <qevent.h>
#include <qlabel.h>
#include <qlistwidget.h>
#include <qminmax.h>
#include <qnamespace.h>
#include <qobject.h>
#include <qpainter.h>
#include <qplaintextedit.h>
#include <qtextformat.h>
#include <qtextobject.h>
#include <qtmetamacros.h>
#include <qwidget.h>
#include <qwindowdefs.h>
#include <unistd.h>

#include "footer.h"
#include "icon.h"

CompletionList::CompletionList(CodeEditWidget *codeEdit) :
    QListWidget(codeEdit), codeEdit(codeEdit) {
    setWindowFlags(Qt::Popup);
    setSelectionMode(SingleSelection);
    setFocusPolicy(Qt::StrongFocus);
    setHorizontalScrollBarPolicy(Qt::ScrollBarAlwaysOff);
    setVerticalScrollBarPolicy(Qt::ScrollBarAsNeeded);
    hide();

    connect(this, &QListWidget::itemClicked, this, &CompletionList::onItemClicked);
}

void CompletionList::updateHeight() {
    const int itemHeight = sizeHintForRow(0);
    const int visiableItems = qMin(count(), 8);

    int totalHeight = visiableItems * itemHeight + 2 * frameWidth();

    setFixedHeight(totalHeight);
    setFixedWidth(400);
}

void CompletionList::onItemClicked(const QListWidgetItem *item) {
    emit completionSelected(item->data(Qt::UserRole).toString());
}

void CompletionList::keyPressEvent(QKeyEvent *e) {
    if (e->key() == Qt::Key_Up || e->key() == Qt::Key_Down) {
        QListWidget::keyPressEvent(e);
    } else if (e->key() == Qt::Key_Tab) {
        if (currentItem()) {
            emit completionSelected(currentItem()->data(Qt::UserRole).toString());
            hide();
        }
    } else if (e->key() == Qt::Key_Escape) {
        hide();
    } else {
        if (e->key() == Qt::Key_Return) {
            hide();
        }
        codeEdit->keyPressEvent(e);
    }
}

void CompletionList::readCompletions(const CompletionResponse &response) {
    codeEdit->requireCompletion = response.incomplete;
    completions = response.items;
}

void CompletionList::update(const QString &curWord) {
    clear();
    for (const auto &item: completions) {
        if (item.insertText == curWord) {
            return;
        }
    }
    for (const auto &item: completions) {
        if (item.insertText.startsWith(curWord)) {
            addCompletionItem(item);
        }
    }
}

void CompletionList::addCompletionItem(const CompletionItem &item) {
    auto *listItem = new QListWidgetItem(this);
    auto *widget = new QWidget(this);
    auto *layout = new QHBoxLayout(widget);
    layout->setContentsMargins(5, 2, 5, 2);
    auto *textLabel = new QLabel(item.label, this);
    textLabel->setMaximumWidth(300);
    textLabel->setFont(font());
    layout->addWidget(textLabel);
    layout->addStretch();


    static const QMap<CompletionItem::ItemKind, QString> kindIconMap = {
            {CompletionItem::Class, "code/class"},
            {CompletionItem::Function, "code/function"},
            {CompletionItem::Interface, "code/class"},
            {CompletionItem::Field, "code/variable"},
            {CompletionItem::Variable, "code/variable"},
            {CompletionItem::Module, "code/module"},
            {CompletionItem::Function, "code/function"},
            {CompletionItem::Keyword, "code/keyword"},
            {CompletionItem::File, "code/file"},
            {CompletionItem::Struct, "code/class"},
            {CompletionItem::Enum, "code/enum"},
            {CompletionItem::Reference, "code/variable"},
            {CompletionItem::Property, "code/variable"},
    };

    auto *iconBtn = new IconPushButton(this);
    auto iconPath = kindIconMap.value(item.kind, "code/text");
    iconBtn->setIconFromResName(iconPath);
    iconBtn->setDisabled(true);
    iconBtn->setStyleSheet(loadText("qss/completion.css"));
    layout->addWidget(iconBtn);

    widget->setLayout(layout);

    listItem->setSizeHint(widget->sizeHint());
    setItemWidget(listItem, widget);

    listItem->setData(Qt::UserRole, item.insertText);
}

void CompletionList::display() {
    setCurrentRow(0);
    show();
    setFocus();
    updateHeight();
}

LineNumberArea::LineNumberArea(CodeEditWidget *codeEdit) : QWidget(codeEdit), codeEdit(codeEdit) {}

int LineNumberArea::getWidth() const {
    int digits = 1;
    int max = qMax(1, codeEdit->blockCount());
    while (max >= 10) {
        max /= 10;
        ++digits;
    }

    int fontWidth = codeEdit->fontMetrics().horizontalAdvance(QLatin1Char('9')) * qMax(digits, 3);
    int marginWidth = L_MARGIN + R_MARGIN;
    return fontWidth + marginWidth;
}

QSize LineNumberArea::sizeHint() const { return {getWidth(), 0}; }

void LineNumberArea::paintEvent(QPaintEvent *event) {
    QPainter painter(this);
    painter.fillRect(event->rect(), QColor(0x252526));

    QTextBlock block = codeEdit->firstVisibleBlock();
    int blockNumber = block.blockNumber();
    int top = static_cast<int>(
            codeEdit->blockBoundingGeometry(block).translated(codeEdit->contentOffset()).top());
    int bottom = top + static_cast<int>(codeEdit->blockBoundingRect(block).height());

    painter.setFont(codeEdit->font());

    while (block.isValid() && top <= event->rect().bottom()) {
        if (block.isVisible() && bottom >= event->rect().top()) {
            QString number = QString::number(blockNumber + 1);

            if (blockNumber == codeEdit->textCursor().blockNumber()) {
                painter.setPen(QColor(0xFFFFFF));
            } else {
                painter.setPen(QColor(0x858585));
            }
            painter.drawText(0, top, this->width() - R_MARGIN, fontMetrics().height(),
                             Qt::AlignRight, number);
        }
        block = block.next();
        top = bottom;
        bottom = top + static_cast<int>(codeEdit->blockBoundingRect(block).height());
        ++blockNumber;
    }
};

const int LineNumberArea::L_MARGIN = 5;
const int LineNumberArea::R_MARGIN = 5;

WelcomeWidget::WelcomeWidget(QWidget *parent) : QWidget(parent) { setup(); }

void WelcomeWidget::setup() {

    auto *mainLayout = new QVBoxLayout(this);
    mainLayout->setAlignment(Qt::AlignCenter);
    mainLayout->setContentsMargins(0, 0, 0, 0);
    mainLayout->setSpacing(30);

    auto *logoLabel = new QLabel(this);
    logoLabel->setText(loadText("logo.txt"));

    QFont logoFont("Consolas", 9);
    logoLabel->setFont(logoFont);
    logoLabel->setObjectName("logo");

    auto *shortcutLabel = new QLabel(this);
    shortcutLabel->setText("<p style='font-size: 16px; color: #D4D4D4;'>Ctrl+N create new file</p>"
                           "<p style='font-size: 16px; color: #D4D4D4;'>Ctrl+O open project</p>"
                           "<p style='font-size: 16px; color: #D4D4D4;'>Ctrl+S save file</p>"
                           "<p style='font-size: 16px; color: #D4D4D4;'>Ctrl+R run code</p>");
    shortcutLabel->setAlignment(Qt::AlignCenter);

    mainLayout->addStretch();
    mainLayout->addWidget(logoLabel);
    mainLayout->addWidget(shortcutLabel);
    mainLayout->addStretch();

    setLayout(mainLayout);
}

CodeEditWidget::CodeEditWidget(const QString &filename, QWidget *parent) :
    QPlainTextEdit(parent), server(nullptr), modified(false), requireCompletion(true) {
    lna = new LineNumberArea(this);
    cl = new CompletionList(this);
    file = LangFileInfo(filename);
    highlighter = HighlighterFactory::getHighligther(file.language(), document());

    readFile();
    setup();
    adaptViewport();

    connect(this, &CodeEditWidget::setupFinished, this, &CodeEditWidget::onSetupFinished);
    connect(this, &CodeEditWidget::blockCountChanged, this, &CodeEditWidget::adaptViewport);
    connect(this, &CodeEditWidget::updateRequest, this, &CodeEditWidget::highlightLine);
    connect(this, &CodeEditWidget::cursorPositionChanged, this, &CodeEditWidget::highlightLine);
}
