//
// Created by Maciek on 10.09.2023.
//

#ifndef DESKPOE_EXAMPLEPANEL1_HPP
#define DESKPOE_EXAMPLEPANEL1_HPP

#include "interfaces/IPanel.hpp"


class ExamplePanel1 : public IPanel {
public:
    explicit ExamplePanel1(QQmlContext* context) : context{context} {}
    virtual ~ExamplePanel1() { delete context; }

    QString getLayout() const final {return "qrc:/WindowComponent.qml";}
    QString getTitle() const final { return "Example Panel 1"; }
    QQmlContext* getContext() const final { return context; }

private:
    QQmlContext* context;
};


#endif //DESKPOE_EXAMPLEPANEL1_HPP
