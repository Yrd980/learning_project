#ifndef FILE_H
#define FILE_H

#include <QFile>
#include <QFileSystemWatcher>
#include <QJsonObject>
#include <QMutex>

QFile loadRes(const QString &path);
QIcon loadIcon(const QString &path);
QString loadText(const QString &path);

class TempFiles {
public:
    static const QString PATH;

    using TempId = QString;

    static TempId genID(const QString &filename);
    static void clearCache();
    static std::unique_ptr<QFile> cache(const TempId &id);
    static std::unique_ptr<QFile> create(const TempId &id = "", const QString &content = "");
};

class Configs : public QObject {
    Q_OBJECT

    explicit Configs(QObject *parents = nullptr);
    static QJsonObject loadConfig();
    static void saveConfig(const QJsonObject &config);

    QJsonObject config;
    QJsonObject defaultConfig;

    mutable QMutex mutex;
    QFileSystemWatcher watcher;
    static const QString PATH;

public:
    static Configs &instance();
    static void clear();
    static void reset();
    QJsonObject get(const QString &key) const;
    QJsonObject getAll() const;
    void set(const QString &key, const QVariant &value);

    void manuallyUpdate(const QString &key);
    template<class W, class V>
    static void bindHotUpdateOn(W *widget, const QString &key, void (W::*slot)(const V &value));

public slots:
    void checkChangedConfig(const QJsonObject &newConfig);

signals:
    void configChanged(const QJsonObject &newConfig);
    void configValueChanged(const QString &key, const QJsonValue &value);
};

template<class W, class V>
void Configs::bindHotUpdateOn(W *widget, const QString &key, void (W::*slot)(const V &)) {
    QObject::connect(&instance(), &Configs::configValueChanged, widget,
                     [key, widget, slot](const QString &k, const QJsonValue &v) {
                         if (k == key) {
                             (widget->*slot)(v.toVariant().value<V>());
                         }
                     });
}

#endif
