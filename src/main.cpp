#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQuickView>
#include "spdlog/spdlog.h"

#include "userSettings/SettingsManager.hpp"

#include "authorization/redditmodel.hpp"

#include <QtCore>
#include <QtWidgets>

int main(int argc, char* argv[]) {
    QApplication app(argc, argv);
    QCommandLineParser parser;
    const QCommandLineOption clientId(QStringList() << "i"
                                                    << "client-id",
                                      "Specifies the application client id",
                                      "client_id");

    parser.addOptions({clientId});
    parser.process(app);

    if (parser.isSet(clientId)) {
        QListView view;
        RedditModel model(parser.value(clientId));
        view.setModel(&model);
        view.show();
    } else {
        parser.showHelp();
    }


    ///////
    QCoreApplication::setOrganizationName("DeskPoE");
    QCoreApplication::setOrganizationDomain("DeskPoE");
    QCoreApplication::setApplicationName("DeskPoE");
    QSettings::setDefaultFormat(QSettings::IniFormat);
    QSettings qsettings;  //default constructor


    SettingsManager* settings = new SettingsManager(&qsettings);
    settings->initToDefaults();
    settings->loadDefaultSettings("defaults.json");

    settings->setValue("name", "Ma Ryan");

    Q_INIT_RESOURCE(qml);

    QQmlApplicationEngine engine;
    const QUrl url(QStringLiteral("qrc:/main.qml"));

    spdlog::info(
        "main Settings val name {}",
        settings->settings.value("name", "default").toString().toStdString());

    spdlog::info(
        "main Settings val testo {}",
        settings->settings.value("testo", "default").toString().toStdString());


    engine.rootContext()->setContextProperty("settings", settings);


    QObject::connect(
        &engine, &QQmlApplicationEngine::objectCreated, &app,
        [url](QObject* obj, const QUrl& objUrl) {
            if (!obj && url == objUrl)
                QCoreApplication::exit(-1);
        },
        Qt::QueuedConnection);
    engine.load(url);


    // QQuickView view;
    // view.rootContext()->setContextProperty("currentDateTime",
    //                                        QDateTime::currentDateTime());
    // view.setSource(QStringLiteral("qrc:/item.qml"));
    // view.show();


    return QGuiApplication::exec();
}
