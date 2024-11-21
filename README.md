# Electronic Marketplace Simulation

This project is a simple localhost simulation of an electronic marketplace for selling items.

This project is built with python and it uses system design of a client/server architecture with the use of sockets. It also utilises the use of threads and concurrency.

## Features

`marketplace_server.py`

- Client Connection Handling
- Item Selling
- Countdown Timer
- Client Commands
- Concurrency
- Notifications

`marketplace_client.py`

- Server Connection
- Message Recieving
- User Commands (buy, list, exit)
- Server Disconnect

## Setup

To run this project, you will need to run `marketplace_server.py` first, and then `marketplace_client.py`in their own seperate terminals.

When `marketplace_server.py` is run, it will set up a locally hosted server, that awaits connections.

When `marketplace_client.py` is run, it will automatically connect to the locally hosted `marketplace_server.py` server. A list of commands will be shown, as to what the user can execute.

## Acknowledgements

Distibuted Systems Labs
