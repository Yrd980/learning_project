#include "crawl.h"

#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonParseError>
#include <QNetworkCookieJar>
#include <QUrlQuery>
#include <qcontainerfwd.h>
#include <qfileinfo.h>
#include <qnetworkcookiejar.h>


#include "../util/file.h"
#include "../util/script.h"

Crawler::Crawler() { nam.setCookieJar(new QNetworkCookieJar()); };

Crawler &Crawler::instance() {
    static Crawler instance;
    return instance;
}

bool Crawler::hasLogin() const { return !email.isEmpty() && !password.isEmpty(); }

Crawler::WebResponse<QByteArray> Crawler::get(const QUrl &url) const {
    QStringList args = {"-u", url.toString()};
    if (hasLogin()) {
        args << "-e" << email << "-p" << password;
    }
    QFile crawl = loadRes("script/crawl.py");
    auto res = co_await runPythonScript(crawl, args);
}


Crawler::WebResponse<QByteArray> Crawler::post(const QUrl &url,
                                               QMap<QString, QString> params) const {

    QStringList args = {"-u", url.toString(), "-m", "post"};

    QString paramsList = "{";
    for (auto it = params.begin(); it != params.end(); ++it) {
        paramsList += "'" + it.key() + "': '" + it.value() + "', ";
    }
    paramsList += "}";
    args << "-a" << paramsList;

    if (hasLogin()) {
        args << "-e" << email << "-p" << password;
    }

    QFile crawl = loadRes("script/crawl.py");
    auto res = co_await runPythonScript(crawl, args);
    if (!res.success || res.exitCode != 0) {
        co_return std::unexpected(res.stdErr);
    }
    co_return res.stdOut.toUtf8();
}

Crawler::WebResponse<QByteArray> Crawler::login(const QString &email, const QString &password) {
    this->email = email;
    this->password = password;
    return get(QUrl("http://openjudge.cn/"));
}
Crawler::WebResponse<QUrl> Crawler::submit(OJSubmitForm form) {
    QUrl url = form.problemUrl.resolved(QUrl("/api/solution/submitv2/"));
    QByteArray encodedCode = form.code.toUtf8().toBase64();
    QMap<QString, QString> params = {
            {"contestId", form.contestId},
            {"problemNumber", form.problemNumber},
            {"sourceEncode", "base64"},
            {"language", form.checked},
            {"source", QString::fromUtf8(encodedCode)},
    };

    auto response = co_await post(url, params);
    if (!response.has_value()) {
        co_return std::unexpected(response.error());
    }
    QJsonParseError error;
    QJsonDocument doc = QJsonDocument::fromJson(response.value(), &error);
    if (error.error != QJsonParseError::NoError) {
        co_return std::unexpected("JSON parse error: " + error.errorString());
    }
    QJsonObject obj = doc.object();
    if (obj["result"].toString() == "SUCCESS") {
        co_return obj["redirect"].toString();
    }
    QString message = obj["message"].toString();
    co_return std::unexpected(message);
}

Crawler::WebResponse<QByteArray> Crawler::personalize(OJPersonalizationForm form) {
    QUrl url("http://openjudge.cn/api/user/modify-profile/");
    QMap<QString, QString> params{
            {"name", form.nickname},
            {"realname", form.name},
            {"description", form.description},
            {"gender", form.gender == OJPersonalizationForm::Male ? "male" : "female"},
            {"birthday", form.birthday},
            {"city", form.city},
            {"school", form.school},
    };
    auto response = co_await post(url, params);
    if (!response.has_value()) {
        co_return std::unexpected(response.error());
    }
    QJsonParseError jpError;
    QJsonDocument doc = QJsonDocument::fromJson(response.value(), &jpError);
    if (jpError.error != QJsonParseError::NoError) {
        co_return std::unexpected("JSON parse error: " + jpError.errorString());
    }
    QJsonObject obj = doc.object();
    if (obj.value("result").toString() == "SUCCESS") {
        co_return response.value();
    }
    QString message = obj.value("message").toString();
    co_return std::unexpected(message);
}
