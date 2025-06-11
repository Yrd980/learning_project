#include "language.h"
#include <qfileinfo.h>
#include <qobject.h>

static const QMap<Language, QString> langMap = {
        {Language::C, "c"},
        {Language::CPP, "cpp"},
        {Language::PYTHON, "python"},
        {Language::C_MAKE_LISTS, "cmakelists"},
};

LangFileInfo::LangFileInfo() = default;

LangFileInfo::LangFileInfo(const QString &fileName) : QFileInfo(fileName) {}

LangFileInfo LangFileInfo::empty() { return {}; }

QString langName(Language lang) { return langMap.value(lang, ""); }

Language stringToLang(QString name) {
    for (auto it = langMap.begin(); it != langMap.end(); ++it) {
        if (it.value() == name) {
            return it.key();
        }
    }
    return Language::UNKNOWN;
}

Language LangFileInfo::language() const {
    if (suffix() == "c") {
        return Language::C;
    }
    if (suffix() == "cpp" || suffix() == "h") {
        return Language::CPP;
    }
    if (suffix() == "py" || suffix() == "pyi") {
        return Language::PYTHON;
    }
    if (fileName() == "CMakeLists.txt") {
        return Language::C_MAKE_LISTS;
    }
    return Language::UNKNOWN;
}

bool LangFileInfo::isValid() const { return !filePath().isEmpty(); }
