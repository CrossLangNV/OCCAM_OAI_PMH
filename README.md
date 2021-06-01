Init OAI-PMH through DSpace

Demo:
http://demo.dspace.org/

DSpace 6.3:
https://github.com/DSpace/DSpace/releases/tag/dspace-6.3

With docker:
https://github.com/DSpace/DSpace/blob/dspace-6_x/dspace/src/main/docker-compose/README.md

* `docker-compose.yml` from https://github.com/DSpace/DSpace/blob/dspace-6_x/docker-compose.yml
* `docker-compose-cli.yml` from https://github.com/DSpace/DSpace/blob/dspace-6_x/docker-compose-cli.yml

## Start DSpace server:

1. To refresh / pull DSpace images from Dockerhub

   `
   docker-compose -f docker-compose.yml -f docker-compose-cli.yml pull
   `

2. Run DSpace from your branch

   `docker-compose -p d6 up -d`

### Accessing OAI

* http://localhost:8080/oai OAI-PMH data provider
* http://localhost:8080/xmlui/ UI for uploading data
* http://localhost:8080/rest REST API for accessing data

## Updating OAI:

* [x] manually:
  see: https://wiki.lyrasis.org/display/DSDOC6x/OAI+2.0+Server

  `docker-compose -p d6 exec dspace bash`

  `/dspace/bin/dspace oai import`

* [ ] Add refresh task to your crontab (@Oan):
  https://wiki.lyrasis.org/display/DSDOC6x/OAI+2.0+Server#OAI2.0Server-ScheduledTasks

## Useful commands

* Ingesting test content Create an admin account. By default, the dspace-cli container runs the dspace command.

    1. Create an admin account. By default, the dspace-cli container runs the dspace command.

  `
  docker-compose -p d6 -f docker-compose-cli.yml run dspace-cli create-administrator -e test@test.edu -f admin -l user -p admin -c en
  `

    2. Download a Zip file of AIP content and ingest test data (**Outdated**)

  `
  docker-compose -p d6 -f docker-compose-cli.yml -f dspace/src/main/docker-compose/cli.ingest.yml run dspace-cli
  `
