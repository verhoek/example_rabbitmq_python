Docker RabbitMQ Example
=======================

(based on https://github.com/danellecline/rabbitmqpika)

This is a minimal example that runs [RabbitMQ](http://rabbitmq.com/)
and two small Python messages, all in a single Docker environment.
The `publisher` program publishes a message into RabbitMQ every 5
seconds; the `consumer` program prints every message it recevies to
its stdout.

Once you've brought it all up, you should see the publisher and
consumer printing messages on their stdout.  You can also point a
browser at http://localhost:15672/ (guest/guest) to see the RabbitMQ
management console.  (If you are using a Docker Toolbox or local
Docker Machine environment, try http://192.168.99.100:15672/.)

