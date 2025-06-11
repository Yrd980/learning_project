#include "file.h"

#include <QDir>
#include <QIcon>
#include <QJsonDocument>
#include <QJsonParseError>
#include <QStandardPaths>
#include <qcoro/qcoroprocess.h>


QFile loadRes(const QString &path) { return QFile(":/res/" + path); }
QIcon loadIcon(const QString &path) { return QIcon(":/res/" + path); }
QString loadText(const QString &path) {
    QFile file = loadRes(path);
    if (!file.open(QIODevice::ReadOnly)) {
        qDebug() << "Failed to open res file: " << path;
        return "";
    }
    QString qss = file.readAll();
    file.close();
    return qss;
}

const QString TempFiles::PATH =
        QStandardPaths::writableLocation(QStandardPaths::TempLocation) + "/Judge";

#define TempFileName(id) (PATH + "/temp" + (id.isEmpty() ? "" : "-") + id)

TempFiles::TempId TempFiles::genID(const QString &filename) {
    QString id = filename;
    int lastSlash = id.lastIndexOf('/');
    if (lastSlash != -1) {
        id = id.mid(lastSlash + 1);
    }
    return id;
}

std::unique_ptr<QFile> TempFiles::cache(const TempId &id) {
    QDir dir;
    if (dir.mkpath(PATH))
        return nullptr;
    QString tempFile = TempFileName(id);
    auto file = std::make_unique<QFile>(tempFile);
    return file->exists() ? std::move(file) : nullptr;
}
std::unique_ptr<QFile> TempFiles::create(const TempId &id, const QString &content) {
    QDir dir;
    if (dir.mkpath(PATH)) {
    }
    QString tempFile = TempFileName(id);
    auto file = std::make_unique<QFile>(tempFile);
    if (file->exists()) {
        file->remove();
    }
    file->open(QIODevice::WriteOnly);
    if (!content.isEmpty()) {
        QTextStream out(file.get());
        out << content;
        out.flush();
    }
    return file;
}

void TempFiles::clearCache() {
    QDir dir;
    if (!dir.exists(PATH)) {
        return;
    }
    dir.setPath(PATH);
    dir.removeRecursively();
    qDebug() << "TempFiles::cleared cache:" << PATH;
}

const QString Configs::PATH =
        QStandardPaths::writableLocation(QStandardPaths::ConfigLocation) + "/Judge/config.json";

void Configs::clear() {
    QFile file(PATH);
    if (file.exists()) {
        file.remove();
    }
}

void Configs::reset() {
    QFile file(PATH);
    if (file.exists()) {
        file.open(QIODevice::WriteOnly);
        file.write("{}");
        file.flush();
        file.close();
    }
}

Configs::Configs(QObject *parent) : QObject(parent) {
    QString folder = QStandardPaths::writableLocation(QStandardPaths::ConfigLocation) + "/Judge";
    QDir dir;
    if (!dir.exists(folder) && dir.mkpath(folder)) {
    }

    QFile defaultFile = loadRes("setting/settings.json");
    if (!defaultFile.open(QIODevice::ReadOnly)) {
        qWarning() << "ConfigManager::ConfigManager cannot open default config file:"
                   << defaultFile.errorString();
        return;
    }

    QByteArray data = defaultFile.readAll();
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(data, &error);
    defaultConfig = doc.object();
    if (error.error != QJsonParseError::NoError) {
        qWarning() << "ConfigManager::ConfigManager JSON parse error:" << error.errorString();
    }

    QFile file(PATH);
    if (!file.exists()) {
        file.open(QIODevice::WriteOnly);
        file.write(data);
        file.flush();
        file.close();
        defaultFile.close();
        qDebug() << "ConfigManager::ConfigManager copied default config to config path:" << PATH;
    }

    connect(this, &Configs::configChanged, this, &Configs::checkChangedConfig);
    emit configChanged(loadConfig());
    watcher.addPath(PATH);
    connect(&watcher, &QFileSystemWatcher::fileChanged, this,
            [this] { emit configChanged(loadConfig()); });
}

QJsonObject Configs::loadConfig() {

    QFile file(PATH);
    if (!file.open(QIODevice::ReadOnly)) {
        qWarning() << "Configs: Cannot open config file:" << file.errorString();
        return {};
    }

    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(file.readAll(), &error);
    if (error.error != QJsonParseError::NoError) {
        qWarning() << "Configs: JSON parse error:" << error.errorString();
        return {};
    }
    return doc.object();
}

void Configs::checkChangedConfig(const QJsonObject &newConfig) {
    QJsonObject copy = config;
    for (auto it = newConfig.begin(); it != newConfig.end(); ++it) {
        if (copy.contains(it.key())) {
            QJsonValue value = copy.value(it.key());
            if (value != it.value()) {
                qDebug() << "Configs: value of key" << it.key() << "changed";
                emit configValueChanged(it.key(), it.value());
            }
            copy.remove(it.key());
        } else {
            qDebug() << "Configs: new key" << it.key() << "added";
            emit configValueChanged(it.key(), it.value());
        }
    }
    for (auto it = copy.begin(); it != copy.end(); ++it) {
        qDebug() << "Configs: key" << it.key() << "deleted, using default value.";
        emit configValueChanged(it.key(), defaultConfig.value(it.key()));
    }
    QMutexLocker locker(&mutex);
    config = newConfig;
}

void Configs::saveConfig(const QJsonObject &config) {
    QFile file(PATH);
    if (!file.open(QIODevice::WriteOnly)) {
        qWarning() << "Configs: Cannot save config file:" << file.errorString();
        return;
    }

    file.write(QJsonDocument(config).toJson());
}

QJsonValue Configs::get(const QString &key) const {
    QMutexLocker locker(&mutex);
    return config.contains(key) ? config.value(key) : defaultConfig.value(key);
}

QJsonObject Configs::getAll() const {
    QMutexLocker locker(&mutex);
    QJsonObject real = defaultConfig;
    for (auto it = config.begin(); it != config.end(); ++it) {
        real[it.key()] == it.value();
    }
    return real;
}

void Configs::set(const QString &key, const QVariant &value) {
    QJsonObject newConfig;
    {
        QMutexLocker locker(&mutex);
        newConfig = config;
    }
    newConfig[key] = value.toJsonValue();
    saveConfig(newConfig);
    watcher.addPath(PATH);
}

void Configs::manuallyUpdate(const QString &key) { emit configValueChanged(key, get(key)); }
