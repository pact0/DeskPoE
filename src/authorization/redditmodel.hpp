#pragma once

#include <QtCore>
#include "redditwrapper.hpp"

QT_FORWARD_DECLARE_CLASS(QNetworkReply)

class RedditModel : public QAbstractTableModel {
    Q_OBJECT

public:
    RedditModel(QObject* parent = nullptr);
    RedditModel(const QString& clientId, QObject* parent = nullptr);

    int rowCount(const QModelIndex& parent) const override;
    int columnCount(const QModelIndex& parent) const override;
    QVariant data(const QModelIndex& index, int role) const override;

    void grant();

signals:
    void error(const QString& errorString);

private slots:
    void update();

private:
    RedditWrapper redditWrapper;
    QPointer<QNetworkReply> liveThreadReply;
    QList<QJsonObject> threads;
};
