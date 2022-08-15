# Run

## wallet mode
> [How do I start only the light wallet in my docker application?](https://developers.chia.net/t/docker-chia-wallet/643)

`docker run -d --rm -e service=wallet -v ~/.chia:/root/.chia -v ~/chia/2483575623.txt:/root/mnemonic-words.txt -e keys="/root/mnemonic-words.txt" --expose=8444 --name wallet-2483575623 ghcr.io/chia-network/chia:latest`

docker run -d --rm -e service=wallet -v ~/.chia:/root/.chia -v ~/chia/2483575623.txt:/root/mnemonic-words.txt -e keys="/root/mnemonic-words.txt" --expose=8444 -e CHIA_ROOT=/root/.chia/testnet10 --expose=58444 -e testnet=true --name wallet-2483575623 ghcr.io/chia-network/chia:latest

`docker exec -it wallet-2483575623 venv/bin/chia wallet show`

## full node (testnet10)
`docker run -d --rm -e CHIA_ROOT=/root/.chia/testnet10 --expose=58444 -e testnet=true -e service=node -v ~/.chia:/root/.chia --name chia ghcr.io/chia-network/chia:latest`

### check status & connection
`docker exec -it chia venv/bin/chia show -sc`

## check running processes
`docker top <CONTAINER_ID>`

## leaflet (x64)
`docker run -it --platform linux/amd64 -e CHIA_ROOT=/root/.chia/testnet10 --expose=58444 -e testnet=true -e service=node -v ~/.chia:/root/.chia --name chia ghcr.io/fireacademy/leaflet:1.2.3`

# References
- [Official Chia Docker Container](https://github.com/Chia-Network/chia-docker)
- [leaflet-docker](https://github.com/FireAcademy/leaflet-docker)