#include "SettingsManager.hpp"
#include <QCoreApplication>
#include <QDebug>
#include <QFile>
#include <QJsonDocument>
#include <QJsonParseError>
#include <QObject>
#include "spdlog/spdlog.h"

SettingsManager::SettingsManager(QObject* parent) : QSettings(parent) {}
SettingsManager::~SettingsManager() {}


void SettingsManager::loadDefaultSettings(const QString& defaultSettingsFile) {
    QFile file(defaultSettingsFile);

    if (file.open(QIODevice::ReadOnly | QIODevice::Text)) {
        QByteArray data = file.readAll();
        QJsonParseError parseError;
        QJsonDocument doc = QJsonDocument::fromJson(data, &parseError);

        if (parseError.error == QJsonParseError::NoError && doc.isObject()) {
            defaultSettings = doc.object();
        } else {
            qDebug() << "Error parsing default settings file:"
                     << parseError.errorString();
            qDebug() << "File path:" << defaultSettingsFile;
        }

        spdlog::info(
            "Default keys {} {}",
            defaultSettings.keys().toList()[0].toStdString(),
            defaultSettings.value("General/Theme").toString().toStdString());

        file.close();
    } else {
        qDebug() << "Error opening default settings file:"
                 << file.errorString();
        qDebug() << "File path:" << defaultSettingsFile;
    }
}

QVariant SettingsManager::getValue2(const QString& key,
                                    const QVariant& defaultValue) const {
    // Check if the key exists in default settings, if not, return the default value
    if (defaultSettings.contains(key)) {
        return settings.value(key, defaultSettings.value(key));
    } else {
        return defaultValue;
    }
}

void SettingsManager::setValue2(const QString& key, const QVariant& value) {
    // Write a setting value to QSettings
    settings.setValue(key, value);
}


QVariant SettingsManager::value(const QString& key,
                                const QVariant& defaultValue = QVariant()) {
    return QSettings::value(key, defaultValue);
}

bool SettingsManager::boolValue(const QString& key, bool defaultValue) {
    return QSettings::value(key, defaultValue).toBool();
}

void SettingsManager::setValue(const QString& key, const QVariant& value) {
    // change the setting and emit a changed signal
    // (we are not checking if the value really changed before emitting for simplicity)
    spdlog::info("Value {} was set to {}", key.toStdString(),
                 value.toStringList().toList()[0].toStdString());
    QSettings::setValue(key, value);
    emit settingChanged(key);
}

void SettingsManager::setValueIfNotSet(const QString& key,
                                       const QVariant& value) {
    // change the setting and emit a changed signal
    if (!QSettings::contains(key)) {
        QSettings::setValue(key, value);
        // (we are not checking if the value really changed before emitting for simplicity)
        emit settingChanged(key);
    }
}

void SettingsManager::initToDefaults() {
    setValueIfNotSet("test", true);
}
