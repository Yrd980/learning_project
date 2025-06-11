#ifndef AICHAT_H
#define AICHAT_H

#include <QDateTime>
#include <QList>
#include <QObject>
#include <QString>
#include <qdatetime.h>
#include <qhashfunctions.h>
#include <qlist.h>
#include <qobject.h>
#include <qtmetamacros.h>

enum class AIMessageType { USER, ASSISTANT, SYSTEM };

struct AIMessage {
    AIMessageType type;
    QString content;
    QDateTime timestamp;

    AIMessage(AIMessageType type, const QString &content) :
        type(type), content(content), timestamp(QDateTime::currentDateTime()) {};
};

class AIChatManager : public QObject {
    Q_OBJECT

    QList<AIMessage> messages;
    int maxContextLength;

    explicit AIChatManager(QObject *parent = nullptr);
    static AIChatManager *instance;

public:
    static AIChatManager &getInstance();
    void addMessage(AIMessageType type, const QString &content);
    QList<AIMessage> getMessages() const;
    QString getContent(int maxTokens = 4096) const;
    void clearMessages();

signals:
    void messageAdded(const AIMessage &message);
};


#endif // !AICHAT_H
