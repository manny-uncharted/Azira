## Description

This project is a real-time streaming service that uses WebSockets to stream messages to clients subscribed to specific tokens. It also ensures that connections are kept alive indefinitely until the client disconnects from it.

## Getting Started

### Dependencies

- Python 3.10+
- FastAPI
- Uvicorn
- ZeroMQ

### Installing

- Unzip the file.
- create a virtual environment
- change directory to the demo folder using:
  ```bash
  cd server/
  ```
- Install the required dependencies by running:
  ```bash
  pip install -r requirements.txt
  ```

## Executing program {#excecuting-the-program}

- Start the message bus stream by running zmqREC.py.

  ```bash
  python notifications/messaging_bq.py
  ```
- Launch the WebSocket server.

  ```bash
  uvicorn app.main:app --reload
  ```
- Connect to the WebSocket using a client that supports WebSocket connections or run the test file.

  ```bash
  python tests/test_websocket.py
  ```

## Project Structure

- README.md: This file contains all the information about the project and how to get started.
- requirements.txt: Lists all the Python dependencies required for the project.
- tests/: This module handles the test for the web application.
  - authentication.py: Allows you to interact with the web application from your terminal. allowing you to register, and login in to the application.
  - test_websocket.py: Allows you to subscribe and unsubscribe to tokens present within the message stream from ZeroMQ.
  - test_zmqrec.py: Allows you to run tests to see if the ZeroMQ message bus is functioning, becomes useful when you're having errors connecting to the message stream.
- app/: includes the fastapi main application.
  - main.py: This just has the web application starting point. And it is where the application server is started from.
- crud/: Module that handles the database operations for the application.
- db/: Module that contains the database configuration files.
- middleware/: Module that handles secondary background operations for the application.
- models/: Module that contains all table definitions for the database and their relationships.
- notifications/: Module that handles the functions to subscribe, unsubscribe, disconnect, and get messages to the user based on the tokens they subscribed to.
- routes/: Module that handles the endpoints for user creation, login, and receives requests from the user to subscribe and unsubscribe to a token.
- utils:/ Module that handles background tasks like token refresh and also the authentication.

### Methods

- connect: Accepts a new WebSocket connection and stores it with the associated client ID.
- disconnect: Removes a WebSocket connection based on the client ID.
- send_personal_message: Sends a message to a specific client.
- broadcast_to_subscribers: Broadcasts a message to all clients subscribed to a specific token.

### Features

- Random market data generation.
- Dynamic token subscription.
- Server control via ZeroMQ messages.

## WebSocket Server

The WebSocket server is responsible for creating connections with clients and streaming messages for specific tokens. It uses the ConnectionManager to manage these connections.
