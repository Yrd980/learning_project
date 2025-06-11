#ifndef LSP_H
#define LSP_H

#include <QJsonObject>
#include <QMutex>
#include <QProcess>
#include <QPromise>
#include <qcorotask.h>
#include <qhashfunctions.h>
#include <qurl.h>

#include "language.h"

enum LSPRequestMethod {
    Initialize,
    Shutdown,
    DidOpen,
    Completion,
    Definition,
    Hover,
    References,
    Formatting,
    Rename,
    PublishDiagnostics,
    DocumentSymbol
};

struct LSPUri {
  QString uri;

  static LSPUri fromQUrl(const QUrl &url);
  QUrl toQUrl() const;
};

#endif // LSP_H
