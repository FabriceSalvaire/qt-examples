# Qt and Input Devices

* [Item — Event Handling](https://doc.qt.io/qt-6/qml-qtquick-item.html#event-handling)

## Handlers

* [Qt Quick Input Handlers](https://doc.qt.io/qt-6/qtquickhandlers-index.html)
* [Input Events in Qt 6](https://www.qt.io/blog/input-events-in-qt-6)
* [Say hello to Qt Quick Pointer Hand](https://www.qt.io/blog/2017/11/23/say-hello-qt-quick-pointer-handlers)

Qt Quick Input Handlers are a set of QML types used to handle events from keyboard, touch, mouse,
and stylus devices.

* an handler manipulates a target item
* each item can have unlimited handlers

* [Keys]()          Provides key handling to Items
* [KeyNavigation]() Supports key navigation by arrow keys

* [DragHandler]()   for dragging
* [HoverHandler]()  for mouse and tablet hover
* [PinchHandler]()  for pinch gestures
* [PointHandler]()  for reacting to a single touchpoint
* [TapHandler]()    for taps and clicks
* [WheelHandler]()  for the mouse wheel

**Base Classes**

```
PointerHandler
    PointerDeviceHandler
        SinglePointHandler
            HoverHandler
            PointHandler
            TapHandler
            WheelHandler
        MultiPointHandler
            DragHandler
            PinchHandler
```

* [PointerHandler](https://doc.qt.io/qt-6/qml-qtquick-pointerhandler.html)
* [PointerDeviceHandler](https://doc.qt.io/qt-6/qml-qtquick-pointerdevicehandler.html)
* [SinglePointHandler](https://doc.qt.io/qt-6/qml-qtquick-singlepointhandler.html)
* [MultiPointHandler](https://doc.qt.io/qt-6/qml-qtquick-multipointhandler.html)

## Linux QPA

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

---

**Map Events**
* double click / tape : zoom aka `TapeHandler`
* Drag / Pan : pan
* Pinch: zoom in/out aka `PinchHandler`
* Flick : animated pan aka `Flickable`

* https://www.qt.io/blog/2017/11/23/say-hello-qt-quick-pointer-handlers

* [Qt Quick Test](https://doc.qt.io/qt-6/qtquicktest-index.html)
* [TestCase](https://doc.qt.io/qt-6/qml-qttest-testcase.html)
* [TouchEventSequence](https://doc.qt.io/qt-6/qml-qttest-toucheventsequence.html)
* https://doc.qt.io/qt-6/qml-qttest-testcase.html#touchEvent-method

* [QPointerEvent](https://doc.qt.io/qt-6/qpointerevent.html)
  A base class for pointer events.
  [QSinglePointEvent](https://doc.qt.io/qt-6/qsinglepointevent.html)
  [QTouchEvent](https://doc.qt.io/qt-6/qtouchevent.html)
* [QNativeGestureEvent](https://doc-snapshots.qt.io/qt6-6.3/qnativegestureevent.html)
  The QNativeGestureEvent class contains parameters that describe a gesture event. 
  `#if QT_CONFIG(gestures)` ???

* [TouchPoint](https://doc.qt.io/qt-6/qml-qtquick-touchpoint.html)

**Event Classes**
* [DragEvent](https://doc.qt.io/qt-6/qml-qtquick-dragevent.html) Provides information about a drag event
* [GestureEvent](https://doc.qt.io/qt-6/qml-qtquick-gestureevent.html) Parameter given with the gestureStarted signal
* [MouseEvent](https://doc.qt.io/qt-6/qml-qtquick-mouseevent.html) Provides information about a mouse event
* [PinchEvent](https://doc.qt.io/qt-6/qml-qtquick-pinchevent.html) For specifying information about a pinch event
* [KeyEvent](https://doc.qt.io/qt-6/qml-qtquick-keyevent.html) Provides information about a key event

**Abstract Handlers**
* [MultiPointHandler](https://doc.qt.io/qt-6/qml-qtquick-multipointhandler.html) Abstract handler for multi-point Pointer Events
  MultiPointHandler > PointerHandler
* [PointerHandler](https://doc.qt.io/qt-6/qml-qtquick-pointerhandler.html) Abstract handler for pointer events
* [PointerDeviceHandler](https://doc.qt.io/qt-6/qml-qtquick-pointerdevicehandler.html) Abstract handler for pointer events with device-specific constraints

**Handlers**
* [DragHandler](https://doc.qt.io/qt-6/qml-qtquick-draghandler.html)
  Handler for dragging an item.
  DragHandler > MultiPointHandler > PointerHandler
* [HoverHandler](https://doc.qt.io/qt-6/qml-qtquick-hoverhandler.html)
  Handler for mouse and tablet hover.
* [PinchHandler](https://doc.qt.io/qt-6/qml-qtquick-pinchhandler.html)
  Handler for pinch gestures.
  PinchHandler is a handler that interprets a multi-finger gesture to interactively rotate, zoom,
  and drag an Item. Like other Input Handlers, by default it is fully functional, and manipulates
  its target, which is the Item within which it is declared.
  PinchHandler > MultiPointHandler > PointerHandler
* [PointHandler](https://doc.qt.io/qt-6/qml-qtquick-pointhandler.html)
  Handler for reacting to a single touchpoint.
  Unlike the others, it doesn't manipulate its target Item: it exists only to expose the point
  property.  It's similar to an individual TouchPoint in MultiPointTouchArea, and can be used for
  the same purpose: to provide interactive feedback as touchpoints and the mouse cursor move around
  the scene.  Unlike MultiPointTouchArea, it does not exclusively grab the touchpoints or the mouse,
  so having this interactive feedback does not prevent interacting with other handlers in other
  Items at the same time.
* [TapHandler](https://doc.qt.io/qt-6/qml-qtquick-taphandler.html )
  Handler for taps on a touchscreen or clicks on a mouse.
* [WheelHandler](https://doc.qt.io/qt-6/qml-qtquick-wheelhandler.html)
  Handler for the mouse wheel.

**Area Items**
* [MouseArea](https://doc.qt.io/qt-6/qml-qtquick-mouseevent.html)
  Enables simple mouse handling
* [MultiPointTouchArea](https://doc.qt.io/qt-6/qml-qtquick-multipointtoucharea.html)
  to show some sort of interactive feedback for the touchpoints
* [PinchArea](https://doc.qt.io/qt-6/qml-qtquick-pincharea.html)
  to handle two-finger scaling, rotation and dragging

**Sources**
`/home/scratch/sources/qt-sources/qt6/qtdeclarative/src/`
* `quick/items/qquickflickable.cpp`
* `quick/handlers/qquickpinchhandler.cpp`
