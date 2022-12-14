// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#include "tabletcanvas.h"

#include <QtMath>
#include <QCursor>
#include <QPainter>
#include <QDebug>
#include <QTime>

//! [0]
TabletCanvas::TabletCanvas(QQuickItem *parent)
  : QQuickItem (parent)
  , m_alphaChannelValuator(TangentialPressureValuator)
  , m_colorSaturationValuator(NoValuator)
  , m_lineWidthValuator(PressureValuator)
  , m_color(Qt::red)
  , m_brush(m_color)
  , m_pen(m_brush, 1.0, Qt::SolidLine, Qt::RoundCap, Qt::RoundJoin)
  , m_deviceDown(false)
{
    initPixmap();

    m_canvasWidth = 1404 / m_columns;
    m_canvasHeight = 1872 / m_rows;
    for (int i = 0; i < m_rows; i++) {
        m_paintedCanvasMap.append(QVector<PaintedCanvas*>());
        for (int j = 0; j < m_columns; j++) {
            qreal x = j * m_canvasWidth;
            qreal y = i * m_canvasHeight;
            PaintedCanvas *canvas = new PaintedCanvas(QRectF(x, y, m_canvasWidth, m_canvasHeight), &m_pixmap, this);
            m_paintedCanvases.append(canvas);
            m_paintedCanvasMap[i].append(canvas);
        }
    }
}

void TabletCanvas::initPixmap()
{
    QPixmap newPixmap = QPixmap(1404, 1872);
    newPixmap.fill(Qt::white);
    QPainter painter(&newPixmap);
    if (!m_pixmap.isNull())
        painter.drawPixmap(0, 0, m_pixmap);
    painter.end();
    m_pixmap = newPixmap;
}
//! [0]

//! [3]
void TabletCanvas::tabletEvent(QTabletEvent *event)
{
    // https://doc.qt.io/qt-6/qpointingdevice.html
    // https://doc.qt.io/qt-6/qinputdevice.html
    auto device = event->pointingDevice();
    qInfo() << "TabletEvent "
            << " type:" << event->pointerType()
            << " name:" << device->name()
            << " seat:" << device->seatName()
            << " id:" << device->systemId() // xinput ID
        ;

    switch (event->type()) {
        case QEvent::TabletPress:
            if (!m_deviceDown) {
                m_deviceDown = true;
                lastPoint.pos = event->position();
                lastPoint.rotation = event->rotation();
            }
            break;
        case QEvent::TabletMove:
#ifndef Q_OS_IOS
            if (event->pointingDevice() && event->pointingDevice()->capabilities().testFlag(QPointingDevice::Capability::Rotation))
              updateCursor(event);
#endif
            if (m_deviceDown) {
                updateBrush(event);
                QPainter painter(&m_pixmap);
                paintPixmap(painter, event);
                lastPoint.pos = event->position();
                lastPoint.rotation = event->rotation();
            }
            break;
        case QEvent::TabletRelease:
            if (m_deviceDown && event->buttons() == Qt::NoButton)
                m_deviceDown = false;
            break;
        default:
            break;
    }
    int i = event->position().y() / m_canvasHeight;
    int j = event->position().x() / m_canvasWidth;

    if (m_paintedCanvasMap.size() < 1) {
        qWarning() << "Error: no canvases in map" << event->position();
        return;
    }
    if (i >= m_paintedCanvasMap.size()) {
        qWarning() << "Error: event outside all canvases" << event->position();
        return;
    }
    if (j >= m_paintedCanvasMap[i].size()) {
        qWarning() << "Error: event outside all canvases" << event->position();
        return;
    }

    PaintedCanvas *canvas = m_paintedCanvasMap[i][j];
    canvas->update();
}

void TabletCanvas::paintPixmap(QPainter &painter, QTabletEvent *event)
{
    painter.setRenderHint(QPainter::Antialiasing);

    switch (event->deviceType()) {
//! [6]
        case QInputDevice::DeviceType::Airbrush:
            {
                painter.setPen(Qt::NoPen);
                QRadialGradient grad(lastPoint.pos, m_pen.widthF() * 10.0);
                QColor color = m_brush.color();
                color.setAlphaF(color.alphaF() * 0.25);
                grad.setColorAt(0, m_brush.color());
                grad.setColorAt(0.5, Qt::transparent);
                painter.setBrush(grad);
                qreal radius = grad.radius();
                painter.drawEllipse(event->position(), radius, radius);
            }
            break;
        case QInputDevice::DeviceType::Stylus:
            if (event->pointingDevice()->capabilities().testFlag(QPointingDevice::Capability::Rotation)) {
                m_brush.setStyle(Qt::SolidPattern);
                painter.setPen(Qt::NoPen);
                painter.setBrush(m_brush);
                QPolygonF poly;
                qreal halfWidth = m_pen.widthF();
                QPointF brushAdjust(qSin(qDegreesToRadians(lastPoint.rotation)) * halfWidth,
                                    qCos(qDegreesToRadians(lastPoint.rotation)) * halfWidth);
                poly << lastPoint.pos + brushAdjust;
                poly << lastPoint.pos - brushAdjust;
                brushAdjust = QPointF(qSin(qDegreesToRadians(event->rotation())) * halfWidth,
                                      qCos(qDegreesToRadians(event->rotation())) * halfWidth);
                poly << event->position() - brushAdjust;
                poly << event->position() + brushAdjust;
                painter.drawConvexPolygon(poly);
            } else {
                painter.setPen(m_pen);
                painter.drawLine(lastPoint.pos, event->position());
            }
            break;
        default:
            {
                const QString error(tr("Unknown tablet device - treating as stylus"));
            }
            // FALL-THROUGH
    }
}
//! [5]

//! [7]
void TabletCanvas::updateBrush(const QTabletEvent *event)
{
    int hue, saturation, value, alpha;
    m_color.getHsv(&hue, &saturation, &value, &alpha);

    int vValue = int(((event->yTilt() + 60.0) / 120.0) * 255);
    int hValue = int(((event->xTilt() + 60.0) / 120.0) * 255);
//! [7] //! [8]

    switch (m_alphaChannelValuator) {
        case PressureValuator:
            m_color.setAlphaF(event->pressure());
            break;
        case TangentialPressureValuator:
            if (event->deviceType() == QInputDevice::DeviceType::Airbrush)
                m_color.setAlphaF(qMax(0.01, (event->tangentialPressure() + 1.0) / 2.0));
            else
                m_color.setAlpha(255);
            break;
        case TiltValuator:
          m_color.setAlpha(std::max(std::abs(vValue - 127), std::abs(hValue - 127)));
            break;
        default:
            m_color.setAlpha(255);
    }

//! [8] //! [9]
    switch (m_colorSaturationValuator) {
        case VTiltValuator:
            m_color.setHsv(hue, vValue, value, alpha);
            break;
        case HTiltValuator:
            m_color.setHsv(hue, hValue, value, alpha);
            break;
        case PressureValuator:
            m_color.setHsv(hue, int(event->pressure() * 255.0), value, alpha);
            break;
        default:
            ;
    }

//! [9] //! [10]
    switch (m_lineWidthValuator) {
        case PressureValuator:
            m_pen.setWidthF(event->pressure() * 10 + 1);
            break;
        case TiltValuator:
          m_pen.setWidthF(std::max(std::abs(vValue - 127), std::abs(hValue - 127)) / 12);
            break;
        default:
            m_pen.setWidthF(1);
    }

//! [10] //! [11]
    if (event->pointerType() == QPointingDevice::PointerType::Eraser) {
        m_brush.setColor(Qt::white);
        m_pen.setColor(Qt::white);
        m_pen.setWidthF(event->pressure() * 10 + 1);
    } else {
        m_brush.setColor(m_color);
        m_pen.setColor(m_color);
    }
}
//! [11]

//! [12]
void TabletCanvas::updateCursor(const QTabletEvent *event)
{
    QCursor cursor;
    if (event->type() != QEvent::TabletLeaveProximity) {
        if (event->pointerType() == QPointingDevice::PointerType::Eraser) {
            cursor = QCursor(QPixmap(":/images/cursor-eraser.png"), 3, 28);
        } else {
            switch (event->deviceType()) {
            case QInputDevice::DeviceType::Stylus:
                if (event->pointingDevice()->capabilities().testFlag(QPointingDevice::Capability::Rotation)) {
                   QImage origImg(QLatin1String(":/images/cursor-felt-marker.png"));
                   QImage img(32, 32, QImage::Format_ARGB32);
                   QColor solid = m_color;
                   solid.setAlpha(255);
                   img.fill(solid);
                   QPainter painter(&img);
                   QTransform transform = painter.transform();
                   transform.translate(16, 16);
                   transform.rotate(-event->rotation());
                   painter.setTransform(transform);
                   painter.setCompositionMode(QPainter::CompositionMode_DestinationIn);
                   painter.drawImage(-24, -24, origImg);
                   painter.setCompositionMode(QPainter::CompositionMode_HardLight);
                   painter.drawImage(-24, -24, origImg);
                   painter.end();
                   cursor = QCursor(QPixmap::fromImage(img), 16, 16);
                } else {
                    cursor = QCursor(QPixmap(":/images/cursor-pencil.png"), 0, 0);
                }
                break;
            case QInputDevice::DeviceType::Airbrush:
                cursor = QCursor(QPixmap(":/images/cursor-airbrush.png"), 3, 4);
                break;
            default:
                break;
            }
        }
    }
    setCursor(cursor);
}

PaintedCanvas::PaintedCanvas(QRectF rect, QPixmap *pixmap, QQuickItem *parent)
    : QQuickPaintedItem(parent)
    , m_pixmap(pixmap)
{
    setFillColor(Qt::white);
    setX(rect.x());
    setY(rect.y());
    setWidth(rect.width());
    setHeight(rect.height());
}

void PaintedCanvas::paint(QPainter *painter)
{
    painter->drawPixmap(boundingRect(), *m_pixmap, QRect(x(), y(), width(), height()));
}
