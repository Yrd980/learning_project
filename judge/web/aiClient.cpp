#include "aiClient.h"

#include <QDebug>
#include <QJsonArray>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <qobject.h>

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
