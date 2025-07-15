# TUTORIAL STEP BY STEP
This tutorial is for helping you to construct a OAI-based Unique Decentrailzed Identifiers local large scale experiment
- Of course, these code also can deploy for cloud based experiment.

# UERANSIM_withDID ERA

## Prerequisite
### 1. VPN
- If you need VPN to download or connet to docker hub, you need to adjust the configuration.
```
allow-lan: true

bind-address: '*'  ##if you don't have this item, just increase it. 
```
- Terminal proxy configuration
```
export http_proxy=http://127.0.0.1:7890

export https_proxy=http://127.0.0.1:7890

export ALL_PROXY=socks5://127.0.0.1:7891

```
- Clash activate
```
# new terminal
chmod +rwx -R clash/

cd clash/

./clash -d .
```


### 2. docker and others
| Software                   | Version                                 |
|:-------------------------- |:----------------------------------------|
| docker engine              | 19.03.6, build 369ce74a3c               |
| docker-compose             | 1.27.4, build 40524192                  |
| Host operating system      | Ubuntu 18.04.4 LTS                      |
| Container operating system | Ubuntu 18.04                            |
| tshark                     | Minimum 3.4.4 (Git commit c33f6306cbb2) |
| wireshark                  | Minimum 3.4.4 (Git commit c33f6306cbb2) |

- docker engine installation
```
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# add key 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg    

curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo systemctl start docker

sudo systemctl enable docker

sudo docker --version

# add user to docker group
sudo usermod -aG docker $USER

newgrp docker

```
- docker-compose installation
```
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

```
- wireshark installation
```
sudo apt-get install wireshark

sudo usermod -aG wireshark $USER

wireshark --version
```

- tshark installation
```
sudo apt-get install tshark

sudo usermod -aG wireshark $USER

tshark --version
```



### 3. docker proxy configuration
```
sudo mkdir -p /etc/systemd/system/docker.service.d

sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```
- Add proxy
```
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
```

- reload docker
```
sudo systemctl daemon-reload

sudo systemctl restart docker
```

### 4. git clone
- pre-config
```
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```
- then git

```
git clone https://github.com/SuperGaric/Unique-Decentralized-Identifiers-Experiments.git
```

### 5. go instrument configuration
```
sudo apt update
sudo apt upgrade

wget https://go.dev/dl/go1.20.1.linux-amd64.tar.gz

sudo tar -C /usr/local -xzf go1.20.1.linux-amd64.tar.gz

```
- config the go PATH
```
vim ~/.bashrc

## add this sentence
export PATH=$PATH:/usr/local/go/bin

## save the vim

source ~/.bashrc

go version
```

### 6. cmake configuration
```
sudo apt update

sudo apt install cmake

cmake --version

sudo apt install ninja-build

sudo apt install build-essential

sudo apt install ccache

sudo apt install libtool pkg-config

git clone https://github.com/velichkov/asn1c.git

cd asn1c
git checkout aper-prefix

autoreconf -iv
./configure
make
sudo make install

asn1c -v
```


## 1. Build core network function: oai-amf and oai-smf
- UlNasTransport.cpp in oai-cn5g-fed/component/oai-amf/src/nas/msgs/UlNasTransport.cpp
- Line 435, change the network address to yours
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/oai-cn5g-fed/component/oai-amf/src/nas/msgs/
vim UlNasTransport.cpp

curl_easy_setopt(curl, CURLOPT_URL, "http://172.17.0.1:8004/dper/setdid");

```
#### NOTE: ####
UERANSIM currently does not support integraty and ciphering algorithm NIA0, NEA0 repectively. Hence we have to update AMF config in the docker-compose as below -

##### IMPORTANT: Add following parameters in oai-amf service of docker-compose, before deploying core network. #####

```bash
** component/oai-amf/etc/amf.conf

            - INT_ALGO_LIST=["NIA1" , "NIA2"]
            - CIPH_ALGO_LIST=["NEA1" , "NEA2"]
```


```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/oai-cn5g-fed

docker pull mikefarah/yq:latest
docker pull ubuntu:focal


sudo docker build --target oai-amf --tag bc-amf:v1.5.7 \
               --file component/oai-amf/docker/Dockerfile.amf.ubuntu \
               --build-arg BASE_IMAGE=ubuntu:focal \
               component/oai-amf

sudo docker build --target oai-smf --tag bc-smf:v1.5.5 \
               --file component/oai-smf/docker/Dockerfile.smf.ubuntu \
               --build-arg BASE_IMAGE=ubuntu:focal \
               component/oai-smf

```

- For convenient, mirrors from aliyun is used in component/oai-amf/docker/Dockerfile.amf.ubuntu. You can change if neccessary. 



## 2.Deploying OAI 5g Core Network

```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/oai-cn5g-fed/docker-compose/

mkdir -p /tmp/oai/vpp-upf-gnbsim

chmod 777 /tmp/oai/vpp-upf-gnbsim

python3 ./core-network.py --type start-basic-vpp --scenario 1
```


## 3. Activate the P3-Chain
- If you want to change the partitions and blockchain node counts:
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/Lee-P3chainforOai-main/dper/client/auto/

## stop use ./stopAll.sh
./startAll.sh

cd ..

cd register/
python3 core-network.py --type start-basic
```



## 4. Building the 'UERANSIM_withDID' and 'UERANSIM_withoutDID' docker image

```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/UERANSIM_withDID/

docker build --target ueransim --tag ueransim:DID -f docker/Dockerfile.ubuntu.18.04 .

cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/UERANSIM_withoutDID/

docker build --target ueransim --tag ueransim:withoutDID -f docker/Dockerfile.ubuntu.18.04 .
```


## 5. build U-DID initialization procedure
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/didserver_local/

vim Changeport.py

### change the count
num_versions = 100
###

python3 ChangePort.py

or nohup python3 ChangePort.py
tail -f nohup.logs
```

## 6. Activate U-DID initialization procedure
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/didserver_local/

###
vim startdidserver_withoutbash.py
count = 100 # change the count
###

python3 startdidserver_withoutbash.py


```

## 7. Activate UE_withU-DID or UE_without-DID

```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/

python3 ueransim_start_withDID_withoutbash.py

```

or 

```
python3 ueransim_start_withoutDID_withoutbash.py
```

- And you can catch the overload of the system, and see the U-DID registrated in p3-Chain.


# Multiple UE with U-DID through openairinterface5g ERA

## Prerequisite
### 1. VPN
- If you need VPN to download or connet to docker hub, you need to adjust the configuration.
```
allow-lan: true

bind-address: '*'  ##if you don't have this item, just increase it. 
```
- Terminal proxy configuration
```
export http_proxy=http://127.0.0.1:7890

export https_proxy=http://127.0.0.1:7890

export ALL_PROXY=socks5://127.0.0.1:7891

```
- Clash activate
```
# new terminal
chmod +rwx -R clash/

cd clash/

./clash -d .
```


### 2. docker and others
| Software                   | Version                                 |
|:-------------------------- |:----------------------------------------|
| docker engine              | 19.03.6, build 369ce74a3c               |
| docker-compose             | 1.27.4, build 40524192                  |
| Host operating system      | Ubuntu 18.04.4 LTS                      |
| Container operating system | Ubuntu 18.04                            |
| tshark                     | Minimum 3.4.4 (Git commit c33f6306cbb2) |
| wireshark                  | Minimum 3.4.4 (Git commit c33f6306cbb2) |

- docker engine installation
```
sudo apt-get update

sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# add key 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg    

curl -fsSL https://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://mirrors.aliyun.com/docker-ce/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

sudo systemctl start docker

sudo systemctl enable docker

sudo docker --version

# add user to docker group
sudo usermod -aG docker $USER

newgrp docker

```
- docker-compose installation
```
DOCKER_COMPOSE_VERSION=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')

sudo curl -L "https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

sudo chmod +x /usr/local/bin/docker-compose

docker-compose --version

sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

```
- wireshark installation
```
sudo apt-get install wireshark

sudo usermod -aG wireshark $USER

wireshark --version
```

- tshark installation
```
sudo apt-get install tshark

sudo usermod -aG wireshark $USER

tshark --version
```



### 3. docker proxy configuration
```
sudo mkdir -p /etc/systemd/system/docker.service.d

sudo vim /etc/systemd/system/docker.service.d/http-proxy.conf
```
- Add proxy
```
[Service]
Environment="HTTP_PROXY=http://127.0.0.1:7890"
Environment="HTTPS_PROXY=http://127.0.0.1:7890"
Environment="NO_PROXY=localhost,127.0.0.1"
```

- reload docker
```
sudo systemctl daemon-reload

sudo systemctl restart docker
```

### 4. git clone
- pre-config
```
git config --global http.proxy http://127.0.0.1:7890
git config --global https.proxy http://127.0.0.1:7890
```
- then git

```
git clone https://github.com/SuperGaric/Unique-Decentralized-Identifiers-Experiments.git
```

### 5. go instrument configuration
```
sudo apt update
sudo apt upgrade

wget https://go.dev/dl/go1.20.1.linux-amd64.tar.gz

sudo tar -C /usr/local -xzf go1.20.1.linux-amd64.tar.gz

```
- config the go PATH
```
vim ~/.bashrc

## add this sentence
export PATH=$PATH:/usr/local/go/bin

## save the vim

source ~/.bashrc

go version
```

### 6. cmake configuration
```
sudo apt update

sudo apt install cmake

cmake --version

sudo apt install ninja-build

sudo apt install build-essential

sudo apt install ccache

sudo apt install libtool pkg-config

git clone https://github.com/velichkov/asn1c.git

cd asn1c
git checkout aper-prefix

autoreconf -iv
./configure
make
sudo make install

asn1c -v
```


## 1. Build core network function: oai-amf and oai-smf
- UlNasTransport.cpp in oai-cn5g-fed/component/oai-amf/src/nas/msgs/UlNasTransport.cpp
- Line 435, change the network address to yours
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/oai-cn5g-fed/component/oai-amf/src/nas/msgs/
vim UlNasTransport.cpp

curl_easy_setopt(curl, CURLOPT_URL, "http://172.17.0.1:8004/dper/setdid");

```



```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/oai-cn5g-fed

docker pull mikefarah/yq:latest
docker pull ubuntu:focal


sudo docker build --target oai-amf --tag bc-amf:v1.5.7 \
               --file component/oai-amf/docker/Dockerfile.amf.ubuntu \
               --build-arg BASE_IMAGE=ubuntu:focal \
               component/oai-amf

sudo docker build --target oai-smf --tag bc-smf:v1.5.5 \
               --file component/oai-smf/docker/Dockerfile.smf.ubuntu \
               --build-arg BASE_IMAGE=ubuntu:focal \
               component/oai-smf

```

- For convenient, mirrors from aliyun is used in component/oai-amf/docker/Dockerfile.amf.ubuntu. You can change if neccessary. 

## 2. Pull the rest of the network function and Activate the core network 
- docker-compose-basic-nrf.yaml in docker-compose/docker-compose-basic-nrf.yaml
- The element of environment, can change to your place, and record a correct timeline in network function docker. 


```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/oai-cn5g-fed/docker-compose/

python3 core-network.py --type start-basic
```
- WARM: Must shut down all the VPN instrument.

## 3. Activate the P3-Chain
- If you want to change the partitions and blockchain node counts:
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/Lee-P3chainforOai-main/dper/client/conf/auto/

## stop use ./stopAll.sh
./startAll.sh

cd ..

cd register/
python3 core-network.py --type start-basic
```
- warning: conf/ auto/ register/ suggest to open in defferent terminal

## 4. build UE with U-DID system 
- build UHD from source
```
sudo apt update

sudo apt install -y autoconf automake build-essential ccache cmake cpufrequtils doxygen ethtool g++ git inetutils-tools libboost-all-dev libncurses5 libncurses5-dev libusb-1.0-0 libusb-1.0-0-dev libusb-dev python3-dev python3-mako python3-numpy python3-requests python3-scipy python3-setuptools python3-ruamel.yaml

git clone https://github.com/EttusResearch/uhd.git ~/uhd

cd ~/uhd

git checkout v4.6.0.0

cd host

mkdir build

cd build

cmake ../

make -j $(nproc)

make test # This step is optional

sudo make install

sudo ldconfig

sudo uhd_images_downloader
```
- build oai dependencies
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/01-modified-openairinterface5g_withDID/cmake_targets

./build_oai -I

# nrscope dependencies
sudo apt install -y libforms-dev libforms-bin

cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/openairinterface5g_withoutDID/cmake_targets

./build_oai -I
```

- use UE_copy_build_withDID.py to build n UE
- vim the UE_copy_build_withDID.py
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs

vim UE_copy_build_withDID.py

...
## change the count of UE
count = 100
```
- operate the UE_copy_build_withDID.py
```
python3 UE_copy_build_withDID.py

### if use SSH, can try nuhup
### for example
nohup python3 UE_copy_build_withDID.py

tail -f nohup.out


### if only build one gnb, can use
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/openairinterface5g_withoutDID/cmake_targets
./build_oai -w USRP --ninja --nrUE --gNB --build-lib "nrscope" -C
```

## 4. build UE without U-DID system 
- use UE_copy_build_withDID.py to build n UE without U-DID
- vim the UE_copy_build_withoutDID.py
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs

vim UE_copy_build_withoutDID.py

...
## change the count of UE
count = 100 
```
- operate the UE_copy_build_withoutDID.py
```
python3 UE_copy_build_withoutDID.py

### if use SSH, can try nuhup
### for example
nohup python3 UE_copy_build_withoutDID.py

tail -f nohup.out
```

## 5. build U-DID initialization procedure
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/didserver_local/

vim Changeport.py

### change the count
num_versions = 5
###

python3 ChangePort.py

or nohup python3 ChangePort.py
tail -f nohup.logs
```

## 6. Activate U-DID initialization procedure
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/didserver_local/

###
vim startdidserver_withoutbash.py
count = 5 # change the count
###

python3 startdidserver_withoutbash.py


```
## 7. Activate UE with U-DID system
- This process will activate UE with U-DID system and activate the monitor system of UE, to extract the CPU and MEM cost of UE with U-DID.
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs

pip install psutil
pip install pandas
## If your server did not have these module

python3 multiple_UE_start_withDID_withoutbash.py

```
- If you want to activate gNB first (remember to commont out the gNB activatin code in multiple_UE_start_withDID_withoutbash):
```
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/openairinterface5g_withoutDID/cmake_targets/ran_build/build/

sudo ./nr-softmodem -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf --gNBs.[0].min_rxtxtime 6 --rfsim --sa

cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs

python3 multiple_UE_start_withDID_withoutbash.py


***If u wanna activate only one UE, u can : ***
cd ~/Unique-Decentralized-Identifiers-Experiments/Local_LargeScale_Experiment/multiple_UEs/openairinterface5g_withoutDID/cmake_targets/ran_build/build/

sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --sa --uicc0.imsi 208950000000031 --rfsim


***USRP B210 ***
** gNB **
sudo ./nr-softmodem -O ../../../targets/PROJECTS/GENERIC-NR-5GC/CONF/gnb.sa.band78.fr1.106PRB.usrpb210.conf --gNBs.[0].min_rxtxtime 6 --sa -E --continuous-tx

** UE **
sudo ./nr-uesoftmodem -r 106 --numerology 1 --band 78 -C 3619200000 --ue-fo-compensation --sa -E --uicc0.imsi 208950000000031


```

- The monitor time is set by 60s, thus, the first time monitoring is not accurate.
- After waiting for the initial waiting time to arrive.
```
(new terminal)
docker logs --since 10min oai-smf
### to checkout if the UE finish the PDU session establishment.
```
- If all the UE finished PDU seesion establishment, you can shut down the UE terminal and grep the time cost.
```
python3 timegrep_withDID.py
``` 
- Now, you can obtain corresponding experiment data, MEM, CPU and latency. 
- You neeed to move these file to the 'experimentdata/withDID' folder, with 'xue_withDID', for e"NEA0" , 
## 8. Experiment data arrangement
- We can use scripts to extract the experiment data from folder 'withDID'.
```

```



