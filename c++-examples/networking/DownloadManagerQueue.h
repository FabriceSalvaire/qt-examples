// Copyright (C) 2022 Fabrice Salvaire
// from https://code.qt.io/cgit/qt/qtbase.git/tree/examples/network/download?h=6.4
//   Copyright (C) 2017 The Qt Company Ltd.
//   SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

/**************************************************************************************************/

#ifndef DOWNLOADMANAGERQUEUE_H
#define DOWNLOADMANAGERQUEUE_H

/**************************************************************************************************/

#include <QtNetwork>
#include <QtCore>

/**************************************************************************************************/

class DownloadManagerQueue: public QObject
{
  Q_OBJECT

 public:
  explicit DownloadManagerQueue(QObject *parent = nullptr);

  void append(const QUrl &url);

 signals:
  void finished();

  private slots:
  void start_next_download();
  void download_progress(qint64 bytesReceived, qint64 bytesTotal);
  void download_finished();
  void download_ready_read();

 private:
  bool is_http_redirect() const;
  void report_redirect();

 private:
  QNetworkAccessManager m_manager;
  QQueue<QUrl> m_download_queue;
  QNetworkReply *m_current_download = nullptr;
  QElapsedTimer m_download_timer;

  int m_downloaded_count = 0;
  int m_total_count = 0;
};

#endif
