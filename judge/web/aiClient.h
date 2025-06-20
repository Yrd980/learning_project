#ifndef AICLIENT_H
#define AICLIENT_H

#include <QJsonDocument>
#include <QJsonObject>
#include <QObject>
#include <QString>
#include <expected>
#include <qcontainerfwd.h>
#include <qcoro/qcoronetworkreply.h>
#include <qcorotask.h>
#include <qjsonobject.h>
#include <qnetworkaccessmanager.h>
#include <qobject.h>
#include <qtmetamacros.h>

class AIClient : public QObject {
    Q_OBJECT

    QString apiKey;
    QString apiEndpoint;
    QNetworkAccessManager nam;

    explicit AIClient(QObject *parent = nullptr);
    static AIClient *instance;

public:
    static AIClient &getInstance();

    void setApiKey(const QString &key);
    bool hasApiKey() const;

    QCoro::Task<std::expected<QString, QString>>
    sendRequest(const QString &prompt, int maxTokens = 1024 * 2, double temperature = 0.7);

    static QJsonObject buildRequestJson(const QString &prompt, int maxTokens, double temperature);

signals:
    void requestCompleted(bool success, const QString &response);
};


#endif // AICLIENT_H
