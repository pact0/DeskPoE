import QtQuick
import QtQuick.Controls

ApplicationWindow {
    height: 480

    title: qsTr("Hello World")
    visible: true
    width: 640

    visibility: Window.Windowed



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

            MenuItem {
                text: qsTr(settings.value("test", "ayyayaya"))

                onTriggered: settings.setValue("1","test")
            }
        }
    }

    Button {
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("Hello World")

        onClicked:{
                console.log("Open action triggered")
        }
    }

        Button {
        anchors.horizontalCenter: parent.horizontalTop
        anchors.verticalCenter: parent.verticalCenter
        text: qsTr("Hello World")
    }
}
