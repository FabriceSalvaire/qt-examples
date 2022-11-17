// Copyright (C) 2022 Fabrice Salvaire
// from https://code.qt.io/cgit/qt/qtbase.git/tree/examples/network/download?h=6.4
//   Copyright (C) 2017 The Qt Company Ltd.
//   SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

/**************************************************************************************************/

#ifndef DOWNLOADMANAGERFUTURE_H
#define DOWNLOADMANAGERFUTURE_H

/**************************************************************************************************/

#include <QtCore>
#include <QtNetwork>

/**************************************************************************************************/

class DownloadManagerFuture: public QObject
{
  Q_OBJECT

 public:
  explicit DownloadManagerFuture();

  void get(const QUrl &url);
  QFuture<QByteArray> download(const QList<QUrl> &urls);
  void run_download(const QList<QUrl> &urls);
  void cancel();

 // signals:
 //  void finished();

 private:
  void update_status(const QString &msg);
  QList<qsizetype> get_size();
  void abort_download();

 private:
  QNetworkAccessManager m_manager;
  QList<QSharedPointer<QNetworkReply>> m_replies;
  QFuture<QByteArray> m_download_future;
};

#endif
