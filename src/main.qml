import QtQuick
import QtQuick.Controls

ApplicationWindow {
    height: 480

    title: qsTr("Hello World")
    visible: true
    width: 640

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")

            MenuItem {
                text: qsTr("&Open")

                onTriggered: console.log("Open action triggered")
            }
            MenuItem {
                text: qsTr("Exit")

                onTriggered: Qt.quit()
            }
        }
    }

    Button {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("Hello World")
    }
}