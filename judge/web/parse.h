#ifndef PARSE_H
#define PARSE_H

#include <QObject>
#include <QString>
#include <QUrl>
#include <expected>
#include <qcoro/qcoronetworkreply.h>
#include <qcorotask.h>
#include <qobject.h>
#include <qstringview.h>
#include <qtmetamacros.h>
#include "oj.h"

class OJParser : public QObject {
    Q_OBJECT

public:
    template<class T>
    using ParseResult = QCoro::Task<std::expected<T, QString>>;

    static ParseResult<OJProblem> parseProblem(const QByteArray &html);
    static ParseResult<OJMatch> parseMatch(const QByteArray &html);
    static ParseResult<OJSubmitForm> parseProblemSubmitForm(const QByteArray &html);
    static ParseResult<OJSubmitResponse> parseProblemSubmitResponse(const QByteArray &html);
    static ParseResult<OJProblemDetail> parseProblemDetail(const QByteArray &html);
    static ParseResult<OJPersonalizationForm> parsePersonalizationForm(const QByteArray &html);
};


#endif // PARSE_H
