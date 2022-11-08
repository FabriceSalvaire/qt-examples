# Qt and Input Devices

## Test

* https://doc.qt.io/qt-6/qml-qttest-testcase.html

## Linux

On **Linux**, the **xcb QPA** (Qt Platform Abstraction) platform plugin is used.

XCB means X protocol C-language Binding.

* https://doc.qt.io/qt-6/linux-requirements.html
* https://doc.qt.io/qt-6/wayland-and-qt.html
* https://doc.qt.io/qt-6/inputs-linux-device.html
* https://doc.qt.io/qt-6/embedded-linux.html

**Stack**
```
kernel
  → libevdev : Generic input event interface in the Linux kernel
    → libinput
      → Wayland compositor             → Wayland client
      → xf86-input-libinput → X server → X client
```

```
QT_QPA_PLATFORM="wayland;xcb"
```

```
-platform
```

## Tablet Support

* [QTabletEvent](https://doc.qt.io/qt-6/qtabletevent.html)
* [QQuickWindow::tabletEvent](https://doc.qt.io/qt-6/qquickwindow.html#tabletEvent)
  see https://github.com/dragly/hello-remarkable for example
  subclass `class TabletWindow : public QQuickWindow`
  register `qmlRegisterType<TabletWindow>("Test", 1, 0, "TabletWindow");`
  use `TabletWindow` in QML
* [PointHandler](https://doc.qt.io/qt-6/qml-qtquick-pointhandler.html)
  [PointHandler point property](https://doc.qt.io/qt-6/qml-qtquick-pointhandler.html#point-prop)
  [HandlerPoint](https://doc.qt.io/qt-6/qml-qtquick-handlerpoint.html)

* QML ???

```
qtbase/src/
  corelib/kernel/
    qcoreevent.cpp
    qcoreevent.h

  gui/kernel/
    qevent.cpp
    qinputdevice.cpp
    qpointingdevice.cpp
    qpointingdevice_p.h

  gui/util/qedidvendortable_p.h

  platformsupport/input/evdevtablet
    qevdevtablethandler.cpp
    qevdevtabletmanager_p.h
    qevdevtablethandler_p.h
    qevdevtabletmanager.cpp

  plugins/generic/evdevtablet
    main.cpp

  plugins/platforms/cocoa/
    qcocoahelpers.mm
    qnsview_tablet.mm

  plugins/platforms/windows/
    qwindowstabletsupport.cpp

  plugins/platforms/xcb/
    qxcbatom.cpp
    qxcbatom.h
    qxcbconnection.cpp
    qxcbconnection_xi2.cpp
```
