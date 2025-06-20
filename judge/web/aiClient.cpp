#include "aiClient.h"

#include <QDebug>
#include <QJsonArray>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <expected>
#include <qcontainerfwd.h>
#include <qcorotask.h>
#include <qjsonarray.h>
#include <qjsondocument.h>
#include <qjsonobject.h>
#include <qjsonparseerror.h>
#include <qnetworkreply.h>
#include <qnetworkrequest.h>
#include <qobject.h>
#include <qurl.h>

#include "../util/file.h"

AIClient *AIClient::instance = nullptr;

AIClient::AIClient(QObject *parent) : QObject(parent) {
    apiEndpoint = "https://api.deepseek.com/v1/chat/completions";
    apiKey = Configs::instance().get("aiAssistant.apiKey").toString();
}

AIClient &AIClient::getInstance() {
    if (!instance) {
        instance = new AIClient();
    }
    return *instance;
}

void AIClient::setApiKey(const QString &key) {
    apiKey = key;
    Configs::instance().set("aiAssistant.apiKey", key);
}

bool AIClient::hasApiKey() const { return !apiKey.isEmpty(); }

QJsonObject AIClient::buildRequestJson(const QString &prompt, int maxTokens, double temperature) {
    QJsonObject message;
    message["role"] = "user";
    message["content"] = prompt;

    QJsonArray messages;
    messages.append(message);

    QJsonObject json;
    json["model"] = "deepseek-coder"; // Using DeepSeek Coder model
    json["messages"] = messages;
    json["max_tokens"] = maxTokens;
    json["temperature"] = temperature;

    return json;
}

QCoro::Task<std::expected<QString, QString>>
AIClient::sendRequest(const QString &prompt, int maxTokens, double temperature) {
    if (!hasApiKey()) {
        co_return std::unexpected(tr("not set api key"));
    }

    QNetworkRequest request;
    request.setUrl(QUrl(apiEndpoint));
    request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    request.setRawHeader("Authorization", QString("Bearer %1").arg(apiKey).toUtf8());

    QJsonObject requestJson = buildRequestJson(prompt, maxTokens, temperature);
    QByteArray requestData = QJsonDocument(requestJson).toJson();

    QNetworkReply *reply = co_await nam.post(request, requestData);

    if (reply->error()) {
        QString errorMsg = reply->errorString();
        delete reply;
        co_return std::unexpected(errorMsg);
    }

    QByteArray responseData = reply->readAll();
    delete reply;

    QJsonParseError parseError;
    QJsonDocument doc = QJsonDocument::fromJson(responseData, &parseError);

    if (parseError.error != QJsonParseError::NoError) {
        co_return std::unexpected("JSON parse error: " + parseError.errorString());
    }

    QJsonObject responseJson = doc.object();

    if (responseData.contains("error")) {
        QString errorMsg = responseJson["error"].toObject()["message"].toString();
        co_return std::unexpected(errorMsg);
    }

    QString choices = responseJson["choices"].toArray();
    if (choices.isEmpty()) {
        co_return std::unexpected(tr("api response empty"));
    }

    QString responseText = choices[0].toObject()["message"].toObject()["content"].toString();
    emit requestCompleted(true, responseText);

    co_return responseText;
}
