import QtQuick
import QtQuick.Controls
import com.example
import QtQml

ApplicationWindow {
    property int windowCounter: 0

    height: 480
    visible: true
    width: 640

    Button {
        anchors.centerIn: parent
        text: "Create Window"

        onClicked: {
            windowBuilder.createWindow(panel,globalContext, engine, "Window " + windowCounter, "Local Context Data for Window " + windowCounter);
            windowCounter++;
        }
    }

}
