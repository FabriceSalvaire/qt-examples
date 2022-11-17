// Copyright (C) 2022 Fabrice Salvaire
// from https://code.qt.io/cgit/qt/qtbase.git/tree/examples/network/download?h=6.4
//   Copyright (C) 2017 The Qt Company Ltd.
//   SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

/**************************************************************************************************/

#ifndef DOWNLOADMANAGER_H
#define DOWNLOADMANAGER_H

/**************************************************************************************************/

#include <QtCore>
#include <QtNetwork>

// ???
QT_BEGIN_NAMESPACE
class QSslError;
QT_END_NAMESPACE

/**************************************************************************************************/

class DownloadManager: public QObject
{
  Q_OBJECT

public:
  DownloadManager();
  void get(const QUrl &url);
  static bool is_http_redirect(QNetworkReply *reply);

public slots:
  void get_finished(QNetworkReply *reply);
  void ssl_errors(const QList<QSslError> &errors);

private:
  QNetworkAccessManager m_manager;
  QList<QNetworkReply *> m_current_downloads;
};

#endif
