Sensor System
=========

Sensor System is a distributed time series database. It has three following components:

  - [OpenTSDB][opentsdb] on top of Hadoop and HBase
  - [ZeroMQ][zeromq] for Messaging
  - Clients



Dependence
----

```sh
pyzmq >= 2.0.10.1
requests >= 2.3.0
OpenTSDB >= 2.1
MySQL-Python >= 1.2.3
```


Installation
--------------

BeofreMake sure that OpenTSDB can run on the cluter

```sh
git clone https://github.com/Kuree/SensorSystem
cd SensorSystem

# for ZeroMQ Queue
cd SensorAPI/
python ZeroMQLayer/ZeroMQQueue.py &

# for ZeroMQ Worker
cd SensorAPI/
python ZeroMQLayer/ZeroMQWorker.py &

```
Configuration
-----------
```sh
ZeroMQ Client: client.conf
ZeroMQ Queue ZeroMQQueue.conf
ZeroMQ Worker ZeroMQWorker.conf
```

[opentsdb]:http://opentsdb.net
[zeromq]:http://zeromq.org/
