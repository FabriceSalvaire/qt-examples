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
