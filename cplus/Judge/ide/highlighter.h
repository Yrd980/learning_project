#ifndef HIGHLIGHTER_H
#define HIGHLIGHTER_H

#include <QJsonObject>
#include <QSyntaxHighlighter>
#include <QTextCharFormat>
#include <qcorotask.h>
#include <qhashfunctions.h>
#include <qtextformat.h>
#include <tree_sitter/api.h>

#include "language.h"

struct HighlightRule {
    QString pattern = nullptr;
    QTextCharFormat strFormat;
};

struct Query {
    TSQuery *query = nullptr;
    TSQueryCursor *cursor = nullptr;
    QTextCharFormat strFormat;
};


#endif // !HIGHLIGHTER_H
