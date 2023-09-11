#ifndef DESKPOE_ICREATOR_H
#define DESKPOE_ICREATOR_H

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQmlComponent>
#include <QQuickWindow>
#include "interfaces/IPanel.hpp"

class ICreator : public QObject {
Q_OBJECT
public:
    explicit ICreator(QObject *parent = nullptr) : QObject(parent) {}
    virtual ~ICreator(){};

    virtual IPanel* FactoryMethod(QQmlContext* context) const = 0;

    QObject* createPanel(QQmlContext* context,QQmlEngine* engine) const {
        IPanel* panel = this->FactoryMethod(context);

        QQmlComponent component(engine, QUrl(panel->getLayout()));
        panel->getContext()->setContextProperty("windowTitle", panel->getTitle());
        QObject* window = component.create(panel->getContext());

        if(!window) {
            qWarning() << "Unable to create window";
        }


        return window;

    }
};


#endif //DESKPOE_ICREATOR_H
