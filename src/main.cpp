#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include "panels/WindowBuilder.hpp"
#include "panels/examplePanel1/examplePanel1Creator.hpp"
#include <memory>


int main(int argc, char *argv[])
{
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

    QGuiApplication app(argc, argv);
    Q_INIT_RESOURCE(qml);


    QQmlApplicationEngine engine;

    auto globalContext = QQmlContext(&engine);
    globalContext.setContextProperty("AppName","DeskPoe");

    QCoreApplication::setOrganizationName("DeskPoE");
    QCoreApplication::setOrganizationDomain("DeskPoE");
    QCoreApplication::setApplicationName("DeskPoE");

    WindowCreator builder;
    ExamplePanel1Creator panel;

    engine.rootContext()->setContextProperty("windowBuilder", &builder);
    engine.rootContext()->setContextProperty("globalContext", &globalContext);
    engine.rootContext()->setContextProperty("engine", &engine);
    engine.rootContext()->setContextProperty("panel", &panel);

    qmlRegisterType<WindowCreator>("com.example", 1, 0, "ICreator");

    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}