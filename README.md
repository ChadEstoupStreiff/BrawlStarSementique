# BrawlStarSementique
## Presentation
Mines Ales formation project  
This is a WebApp using Streamlit and RDFLib to read a Sementic Database about BrawlStar. The application will determine compatibility between map and brawler based on map tag and brawler stats.
## To launch
Clone this repo
```sh
git clone git@github.com:ChadEstoupStreiff/BrawlStarSementique.git
```
Clone .env_ex to .env
```sh
cp .env_ex .env
```
Edit .env file with parameters you want
```
nano .env
```
and launch docker-compose
``` sh
docker-compose up -d
```
You can now access to the webapp on the ip http://127.0.0.1:8080 (another port if you changed it).  
You can setup a reverse proxy like NGinx or Traefik if you want to access it from the outside or add a SSL certificate to it.