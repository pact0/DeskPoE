#pragma once

#include <QJsonObject>
#include <QObject>
#include <QSettings>

class SettingsManager : public QSettings {
    Q_OBJECT

public:
    // explicit SettingsManager(const QString& defaultSettingsFile,
    //                          QSettings* parent = nullptr);

    // Define functions to get and set settings
    QVariant getValue2(const QString& key,
                       const QVariant& defaultValue = QVariant()) const;
    void setValue2(const QString& key, const QVariant& value);

    SettingsManager(QObject* parent = 0);
    virtual ~SettingsManager();

    Q_INVOKABLE
    void setValue(const QString& key, const QVariant& value);

    Q_INVOKABLE
    void setValueIfNotSet(const QString& key, const QVariant& value);

    Q_INVOKABLE
    QVariant value(const QString& key, const QVariant& defaultValue);

    Q_INVOKABLE
    bool boolValue(const QString& key, const bool defaultValue);

    Q_INVOKABLE
    void initToDefaults();

    void loadDefaultSettings(const QString& defaultSettingsFile);

    // private:
    QSettings settings;
    QJsonObject defaultSettings;
signals:
    void settingChanged(const QString& key);
};
