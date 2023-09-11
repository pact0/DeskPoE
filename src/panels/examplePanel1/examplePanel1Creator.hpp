//
// Created by Maciek on 10.09.2023.
//

#ifndef DESKPOE_EXAMPLEPANEL1CREATOR_HPP
#define DESKPOE_EXAMPLEPANEL1CREATOR_HPP

#include "interfaces/ICreator.h"
#include "panels/examplePanel1/examplePanel1.hpp"


class ExamplePanel1Creator : public ICreator {
public:
    IPanel* FactoryMethod(QQmlContext* context) const override {
        return new ExamplePanel1(context);
    }
};


#endif //DESKPOE_EXAMPLEPANEL1CREATOR_HPP
