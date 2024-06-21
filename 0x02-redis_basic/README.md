# Redis - Remote Dictionary Service

# Introduction
Redis is a type of noSQL database usually used on top of traditional database.
Redis as other databases is used for storing information as any DB would. However, unlike traditional DBs Redis stores information on the RAM (volatile memory). This results in faster READ/WRITE speeds which makes it perfectly suitable for data that is frequently read as the main DB would have less strain on it

## Architecture

Redis operaties in a client-server architecture with a request - response model.

The client requests for data from the server, the server fetches this data and then sends a response to the client

