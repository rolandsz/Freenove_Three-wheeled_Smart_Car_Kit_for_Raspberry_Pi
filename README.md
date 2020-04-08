
# Freenove Three-wheeled Smart Car Kit for Raspberry Pi

## Setup

In this section you may find detailed instructions about the setup of the project. 

### SSL
In order to secure the connection between the car and the client you'll need to generate SSL certificates. An example using [CloudFlare's PKI toolkit](https://blog.cloudflare.com/introducing-cfssl/) is provided below.
#### Certificate Authority
This command creates a self-signed certificate for a certificate authority which is used to sign and validate client and server certificates.
```
cfssl gencert --initca ssl/ca-csr.json | cfssljson --bare ssl/ca
```
Both the server and the client require this certificate to validate each other. The following commands copy the certificate to the appropriate locations.
```
cp ssl/ca.pem api/ssl/ca.pem
cp ssl/ca.pem client/ssl/ca.pem
```

#### API certificate
This command creates a certificate for the API and signs it with the previously generated certificate authority. You might need to change the default hostname from "raspberrypi".
```
cfssl gencert --ca=ssl/ca.pem --ca-key=ssl/ca-key.pem --config=ssl/ca-config.json --hostname=raspberrypi ssl/api-csr.json | cfssljson --bare api/ssl/api
```

#### Client certificate
This command creates a certificate for the client and signs it with the previously generated certificate authority.
```
cfssl gencert --ca=ssl/ca.pem --ca-key=ssl/ca-key.pem --config=ssl/ca-config.json ssl/client-csr.json | cfssljson --bare client/ssl/client
```

### mjpg-streamer

The mjpg-streamer runs on the Raspberry PI and it is used to live stream what the car sees.

```
sudo apt install cmake libjpeg8-dev

git clone https://github.com/rolandsz/mjpg-streamer.git
cd mjpg-streamer/mjpg-streamer-experimental/
make -j4
sudo make install
```

### API
The gRPC API runs on the Raspberry PI and it is used to control the car remotely. You'll need to copy the *api* and *protos* folders to the Raspberry PI and execute the following commands in order.

```
sudo apt install python3-grpcio python3-grpc-tools

cd ~/Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi/api
python3 -m grpc_tools.protoc -I../protos --python_out=./generated --grpc_python_out=./generated ../protos/buzzer_control.proto ../protos/camera_control.proto ../protos/car_control.proto ../protos/led_control.proto ../protos/ultrasonic_control.proto 
```

You will also need to enable I2C by exeuting the following command and selecting Interfacing Options > I2C.

```
sudo raspi-config
```

### Client
The client is a PyQt5 application that connects to the API running on the Raspberry PI via gRPC, which means you may run the client on an arbitrary device of your choice. You’ll need to setup the environment and generate the interface definitions by executing the following commands in order.

```
cd ~/Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi/client
conda create --name smart-car-client python=3
conda activate smart-car-client
pip install -r requirements.txt

python -m grpc_tools.protoc -I../protos --python_out=./generated --grpc_python_out=./generated ../protos/buzzer_control.proto ../protos/camera_control.proto ../protos/car_control.proto ../protos/led_control.proto ../protos/ultrasonic_control.proto 
```

## Usage
### API
```
cd ~/Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi/api
python3 api.py --port 50051
```

### Client
```
cd ~/Freenove_Three-wheeled_Smart_Car_Kit_for_Raspberry_Pi/client
conda activate smart-car-client
python client.py --address raspberrypi --port 50051 --car-key <your unique car key displayed by the API upon startup>
```
