## Transbank SDK Webpay REST example project for Python


### Requirements

You need to have `docker` and `docker-compose`installed

#### How to run this example project

You can run this project by typing `make` on your Terminal


### Troubleshooting

Currently this example project uses local repos as dependencies, exposing them from your computer to
the docker container. If the SDK is not found, you can check `docker-compose.yml` on the repo's root and check the
`volumes` entry, to verify that the origin path (the one with `{$HOME}`) matches the location of the SDK on your local
machine