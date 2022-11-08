#include "tabletwindow.h"
#include "tabletcanvas.h"
#include <QDebug>
#include <QGuiApplication>
#include <QScreen>
#include <QQmlListProperty>

TabletWindow::TabletWindow(QWindow *parent) : QQuickWindow(parent)
{
}

QPointF rotate(QPointF other, qreal width, qreal height)
{
    return QPointF(other.y() / height * width, (1.0 - other.x() / width) * height);
}


void TabletWindow::tabletEvent(QTabletEvent *event)
{
//    qDebug() << event;

    // QPointF rotated = rotate(event->position(), width(), height());
    // QPointF rotatedGlobal(rotate(event->globalPosition(), width(), height()));
    QPointF rotated(event->position());
    QPointF rotatedGlobal(event->globalPosition());
    penEvent(rotated, event->pressure());

    if (m_canvas) {
        QPointF offset = rotated - m_canvas->position();
        QTabletEvent *fakeEvent = new QTabletEvent(event->type(),
                                                   event->pointingDevice(),
                                                   offset,
                                                   rotatedGlobal,
                                                   event->pressure(),
                                                   event->xTilt(),
                                                   event->yTilt(),
                                                   event->tangentialPressure(),
                                                   event->rotation(),
                                                   event->z(),
                                                   event->modifiers(),
                                                   event->button(),
                                                   event->buttons()
                                                   );
        m_canvas->tabletEvent(fakeEvent);
    }
}

TabletCanvas *TabletWindow::canvas() const
{
    return m_canvas;
}

void TabletWindow::setCanvas(TabletCanvas *canvas)
{
    if (m_canvas == canvas)
        return;

    m_canvas = canvas;
    emit canvasChanged(m_canvas);
}
