#include <QApplication>
#include <QMainWindow>
#include <boost/core/addressof.hpp>
#include <iostream>
#include "spdlog/spdlog.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    spdlog::info("Witam w spdlogu!");
    std::cout<<boost::addressof(app)<<std::endl;
    QMainWindow mainWindow;
    mainWindow.setWindowTitle("Moje Okno");
    mainWindow.show();

    return app.exec();
}