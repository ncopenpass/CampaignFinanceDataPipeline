# Docker Compose for NC Elections Transparency Project
docker-compose oriented Jupyter Notebook with some extra packages for geospatial work and a postgres db

Also contains an rstudio, shiny, and neo4j enviroment that can be loaded

Default login for pgadmin to manage the postgres enviroment is UN:admin@admin.com PW:admin

Jupyter notebook is configured to use a token. The login URL is visible in the docker logs on screen

Other info available in docker-compose.yml

This builds a custom Jupyter and will require a long build time the first time 'docker-compose up'. You will have time to prepare and eat a meal before it is finished.


