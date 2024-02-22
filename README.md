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

### Alternative Way to run the example project

If you don't want to use docker, you can run the example project by following these steps:

- Execute the command python3 -m venv venv
- Activate the virtual environment with source venv/bin/activate
- Install the dependencies with pip install transbank-sdk
- Run the example with python `__init__.py`
