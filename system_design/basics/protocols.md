# System Design: Fundamental - Communication Protocols

[Back](../system_design.md)

- [System Design: Fundamental - Communication Protocols](#system-design-fundamental---communication-protocols)
  - [Long-Polling vs WebSockets vs Server-Sent Events](#long-polling-vs-websockets-vs-server-sent-events)
    - [Ajax Polling](#ajax-polling)
    - [HTTP Long-Polling](#http-long-polling)
    - [WebSockets](#websockets)
    - [Server-Sent Events (SSEs)](#server-sent-events-sses)

---

## Long-Polling vs WebSockets vs Server-Sent Events

- popular communication protocols between a client like a web browser and a web server:
  - Long-Polling, WebSockets, and Server-Sent Events

### Ajax Polling

- `Polling`: a **standard** technique
  - the client **repeatedly polls** (or requests) a server for data at regular intervals
- problem
  - a lot of responses are empty, creating HTTP overhead.

---

### HTTP Long-Polling

- `HTTP Long-Polling`
  - the client **requests** information from the server exactly as in normal polling, but with the **expectation** that the server may **not respond immediately**.
    - the server **holds the request** and waits until some data becomes **available**.
    - Once the data becomes **available**, a full response is **sent** to the client.
      - The client then immediately **re-request** information from the server
    - Each Long-Poll request has a **timeout**.
      - The client has to reconnect **periodically** after the connection is closed due to **timeouts**.

---

### WebSockets

- `WebSocket`:
  - provides **Full duplex communication channels** over a single TCP connection.
    - a persistent connection between a client and a server that **both parties can use to start sending data** at any time.

---

### Server-Sent Events (SSEs)

- `Server-Sent Events (SSE)`
  - a web technology that lets a server **push real-time updates** down to a browser client **over a single, long-lived HTTP connection**.
  - Unidirectional: Data flows in **only one direction**—from the server to the client.

- the best when we **need real-time traffic** from the server to the client or if the server is generating data in a loop and will be **sending multiple events** to the client.
