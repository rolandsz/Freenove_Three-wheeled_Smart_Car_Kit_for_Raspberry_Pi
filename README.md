# Freenove Three-wheeled Smart Car Kit for Raspberry Pi

## Setup
### SSL
In order to secure the connection between the car and a client of your choice you'll need to generate SSL certificates. An example using [CloudFlare's PKI toolkit](https://blog.cloudflare.com/introducing-cfssl/) is provided below.
#### Certificate Authority
This command creates a self-signed certificate for a certificate authority which is used to sign and validate client and server certificates.
```
cfssl gencert --initca ssl/ca-csr.json | cfssljson --bare ssl/ca
```

#### Server
This command creates a certificate for the server and signs it with the previously generated certificate authority. You might need to change the default hostname from "raspberrypi".
```
cfssl gencert --ca=ssl/ca.pem --ca-key=ssl/ca-key.pem --config=ssl/ca-config.json --hostname=raspberrypi ssl/server-csr.json | cfssljson --bare ssl/server
```

#### Client
This command creates a certificate for a client and signs it with the previously generated certificate authority.
```
cfssl gencert --ca=ssl/ca.pem --ca-key=ssl/ca-key.pem --config=ssl/ca-config.json ssl/client-csr.json | cfssljson --bare ssl/client
```
