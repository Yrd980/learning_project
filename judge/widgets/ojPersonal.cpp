#include "ojPersonal.h"

#include <QDate>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QMessageBox>
#include <QPushButton>
#include <QRegularExpression>
#include <QRegularExpressionValidator>
#include <QUrl>
#include <QVBoxLayout>
#include <qcombobox.h>
#include <qcoronetworkreply.h>
#include <qcorotask.h>
#include <qdatetimeedit.h>
#include <qlineedit.h>
#include <qmessagebox.h>
#include <qregularexpression.h>
#include <qstringliteral.h>
#include <qtextedit.h>
#include <qurl.h>
#include <qvalidator.h>

#include "../web/crawl.h"
#include "../web/oj.h"
#include "../web/parse.h"

PersonalSettingsDialog::PersonalSettingsDialog(QWidget *parent) : QDialog(parent) {
    setWindowTitle(tr("OpenJudge personal settings"));
    auto *form = new QFormLayout(this);
    nicknameEdit = new QLineEdit(this);
    QRegularExpression nickRx(QStringLiteral("^[\\p{Han}A-Za-z0-9]{1,15}$"));
    nicknameEdit->setValidator(new QRegularExpressionValidator(nickRx, this));

    nameEdit = new QLineEdit(this);
    descriptionEdit = new QTextEdit(this);

    genderCombo = new QComboBox(this);
    genderCombo->addItems({tr("man"), tr("male")});

    birthdayEdit = new QDateEdit(this);
    birthdayEdit->setDisplayFormat("yyyy-MM-dd");
    birthdayEdit->setCalendarPopup(true);

    cityEdit = new QLineEdit(this);
    schoolEdit = new QLineEdit(this);

    form->addRow(tr("nickname:"), nicknameEdit);
    form->addRow(tr("real name:"), nameEdit);
    form->addRow(tr("personal description:"), descriptionEdit);
    form->addRow(tr("gender:"), genderCombo);
    form->addRow(tr("birthday:"), birthdayEdit);
    form->addRow(tr("city:"), cityEdit);
    form->addRow(tr("school:"), schoolEdit);

    auto *pullBtn = new QPushButton(tr("pull"), this);
    auto *updateBtn = new QPushButton(tr("update"), this);
    auto *cancelBtn = new QPushButton(tr("cancel"), this);
    connect(pullBtn, &QPushButton::clicked, this, &PersonalSettingsDialog::loadExisting);
    connect(updateBtn, &QPushButton::clicked, this, &PersonalSettingsDialog::onSave);
    connect(cancelBtn, &QPushButton::clicked, this, &QDialog::reject);

    auto *btnLay = new QHBoxLayout(this);
    btnLay->addStretch();
    btnLay->addWidget(pullBtn);
    btnLay->addWidget(updateBtn);
    btnLay->addWidget(cancelBtn);
    form->addRow(btnLay);

    setLayout(form);
}

QCoro::Task<> PersonalSettingsDialog::onSave() {
    if (nicknameEdit->text().isEmpty()) {
        QMessageBox::warning(this, tr("form error"), tr("nickname can not empty"));
        co_return;
    }

    OJPersonalizationForm form;
    form.nickname = nicknameEdit->text();
    form.name = nameEdit->text();
    form.description = descriptionEdit->toPlainText();
    form.gender = genderCombo->currentIndex() == 0 ? OJPersonalizationForm::Male
                                                   : OJPersonalizationForm::Female;
    form.birthday = birthdayEdit->date().toString(Qt::ISODate);
    form.city = cityEdit->text();
    form.school = schoolEdit->text();

    auto res = co_await Crawler::instance().personalize(form);
    if (!res.has_value()) {
        QMessageBox::critical(this, tr("save fail"), res.error());
        co_return;
    }

    QMessageBox::information(this, tr("save success"), tr("your personal settings save success"));
    accept();
}

QCoro::Task<> PersonalSettingsDialog::loadExisting() {
    if (!Crawler::instance().hasLogin()) {
        QMessageBox::warning(this, tr("unlogin"), tr("please login OpenJudge"));
        co_return;
    }

    auto response = co_await Crawler::instance().get(QUrl("http://openjudge.cn/settings/"));
    if (!response.has_value()) {
        QMessageBox::warning(this, tr("pull fail"), response.error());
        co_return;
    }

    auto parsed = co_await OJParser::parsePersonalizationForm(response.value());
    if (!parsed.has_value()) {
        QMessageBox::warning(this, tr("pull fail"), parsed.error());
        co_return;
    }

    auto &form = parsed.value();
    nicknameEdit->setText(form.nickname);
    nameEdit->setText(form.name);
    descriptionEdit->setPlainText(form.description);
    genderCombo->setCurrentIndex(form.gender == OJPersonalizationForm::Male ? 0 : 1);
    birthdayEdit->setDate(QDate::fromString(form.birthday, Qt::ISODate));
    cityEdit->setText(form.city);
    schoolEdit->setText(form.school);
}
