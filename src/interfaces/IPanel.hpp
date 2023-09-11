//
// Created by Maciek on 10.09.2023.
//

#ifndef DESKPOE_IPANEL_HPP
#define DESKPOE_IPANEL_HPP

#include <QString>
#include <QQmlContext>

class IPanel
{
public:
    IPanel() = default;
    explicit IPanel(QQmlContext* context);
    virtual ~IPanel() {}

    virtual QString getLayout() const = 0;
    virtual QQmlContext* getContext() const = 0;
    virtual QString getTitle() const = 0;
};

#endif //DESKPOE_IPANEL_HPP
