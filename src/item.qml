// MyItem.qml
import QtQuick
import QtQuick.Controls

Text {
     text: qsTr(settings.value("test", "ayyayaya"))
    id: "root"
 }
