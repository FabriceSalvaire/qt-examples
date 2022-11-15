// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

#ifndef TABLETCANVAS_H
#define TABLETCANVAS_H

#include <QPixmap>
#include <QPoint>
#include <QTabletEvent>
#include <QColor>
#include <QBrush>
#include <QPen>
#include <QPoint>
#include <QQuickPaintedItem>
#include <QTimer>

QT_BEGIN_NAMESPACE
class QPaintEvent;
class QString;
QT_END_NAMESPACE

class PaintedCanvas : public QQuickPaintedItem
{
    Q_OBJECT

public:
    PaintedCanvas(QRectF rect, QPixmap *pixmap, QQuickItem *parent = nullptr);
    virtual void paint(QPainter *painter) override;
    bool dirty = false;

private:
    QPixmap *m_pixmap;
};

//! [0]
class TabletCanvas : public QQuickItem
{
    Q_OBJECT

public:
    enum Valuator { PressureValuator, TangentialPressureValuator,
                    TiltValuator, VTiltValuator, HTiltValuator, NoValuator };
    Q_ENUM(Valuator)

    TabletCanvas(QQuickItem *parent = nullptr);

    void setAlphaChannelValuator(Valuator type)
        { m_alphaChannelValuator = type; }
    void setColorSaturationValuator(Valuator type)
        { m_colorSaturationValuator = type; }
    void setLineWidthType(Valuator type)
        { m_lineWidthValuator = type; }
    void setColor(const QColor &c)
        { if (c.isValid()) m_color = c; }
    QColor color() const
        { return m_color; }
    void setTabletDevice(QTabletEvent *event)
        { updateCursor(event); }
    void tabletEvent(QTabletEvent *event);

private:
    void initPixmap();
    void paintPixmap(QPainter &painter, QTabletEvent *event);
    Qt::BrushStyle brushPattern(qreal value);
    void updateBrush(const QTabletEvent *event);
    void updateCursor(const QTabletEvent *event);

    Valuator m_alphaChannelValuator;
    Valuator m_colorSaturationValuator;
    Valuator m_lineWidthValuator;
    QColor m_color;
    QPixmap m_pixmap;
    QBrush m_brush;
    QPen m_pen;
    bool m_deviceDown;
    QRect m_latestRect;
    QVector<QVector<PaintedCanvas*>> m_paintedCanvasMap;
    QVector<PaintedCanvas*> m_paintedCanvases;

    int m_rows = 8;
    int m_columns = 6;

    qreal m_canvasWidth = 0.0;
    qreal m_canvasHeight = 0.0;

    struct Point {
        QPointF pos;
        qreal rotation;
    } lastPoint;
};
//! [0]

#endif
