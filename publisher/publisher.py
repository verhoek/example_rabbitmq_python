#!/usr/bin/env python
#
# Simple RabbitMQ publisher.

import os
import pika
import time

from threading import Timer
from functools import partial

EXCHANGE = 'exchange'

DELAY = 0.01

def main():
    """Main entry point to the program."""

    # Get the location of the AMQP broker (RabbitMQ server) from
    # an environment variable
    amqp_url = os.environ['AMQP_URL']
    print('URL: %s' % (amqp_url,))

    # Actually connect
    parameters = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(parameters, on_open_callback=on_open)

    # Main loop.  This will run forever, or until we get killed.
    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.start()


def on_open(connection):
    """Callback when we have connected to the AMQP broker."""
    print('Connected')
    connection.channel(on_open_callback=on_channel_open)


def on_channel_open(channel):
    """Callback when we have opened a channel on the connection."""
    print('Have channel')
    channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout',
                             durable=True,
                             callback=partial(on_exchange, channel))


def on_exchange(channel, frame):
    """Callback when we have successfully declared the exchange."""
    print('Have exchange')
    send_message(channel, 0)



def send_message(channel, i):
    """Send a message to the queue.

    This function also registers itself as a timeout function, so the
    main :mod:`pika` loop will call this function again every 5 seconds.

    """
    msg = 'Message %d' % (i,)
    print(msg)
    channel.basic_publish(EXCHANGE, '', msg,
                          properties=pika.BasicProperties(content_type='text/plain',
                                               delivery_mode=2))

    Timer(DELAY, send_message, [channel, i+1]).start()

if __name__ == '__main__':
    main()
