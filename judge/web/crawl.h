#ifndef CRAWL_H
#define CRAWL_H

#include <expected>
#include <qcontainerfwd.h>
#include <qcoro/qcoronetworkreply.h>
#include <qcorotask.h>
#include <qmap.h>
#include <qnetworkaccessmanager.h>
#include <qurl.h>

#include "oj.h"

class Crawler {
    QNetworkAccessManager nam;

    QString email;
    QString password;

    explicit Crawler();

public:
    static Crawler &instance();
    bool hasLogin() const;

    template<class T>
    using WebResponse = QCoro::Task<std::expected<T, QString>>;

    WebResponse<QByteArray> get(const QUrl &url) const;
    WebResponse<QByteArray> post(const QUrl &url, QMap<QString, QString> params) const;
    WebResponse<QByteArray> login(const QString &email, const QString &password);
    WebResponse<QUrl> submit(OJSubmitForm form);
    WebResponse<QByteArray> personalize(OJPersonalizationForm form);
};


#endif // CRAWL_H
