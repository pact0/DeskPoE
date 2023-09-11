//
// Created by Maciek on 10.09.2023.
//

#ifndef DESKPOE_WINDOWBUILDER_HPP
#define DESKPOE_WINDOWBUILDER_HPP

#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QQmlComponent>
#include <QQuickWindow>
#include "interfaces/ICreator.h"


class WindowCreator : public QObject {
    Q_OBJECT
public:
    explicit WindowCreator(QObject *parent = nullptr) : QObject(parent) {}

    Q_INVOKABLE QObject* createWindow(ICreator* panelCreator,QQmlContext* context,QQmlEngine* engine,  const QString& title, const QString& localContextData) {

        return panelCreator->createPanel(context,engine);
    }
};

#endif //DESKPOE_WINDOWBUILDER_HPP
