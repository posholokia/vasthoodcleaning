# Vasthood Cleaning Site 

https://vasthood.com

## Application Deployment

Set environment variables as specified in the example.env:

The application is ready for deployment. To run it in Docker, use the docker-compose files:
./.ci/docker/*.local.yml

Commands to start:

```
docker compose -f ./.ci/docker/storage.local.yml up
docker compose -f ./.ci/docker/app.local.yml up
docker exec -it vasthood_django python manage.py migrate
```

3. For local development, mark the core directory as "Source root" since imports in the application are done after core.

    Only files and folders not directly related to the application, such as test, ci/cd, docker, etc., should be 
outside the core directory. Everything necessary for the application's operation should be inside core.

## API docs
`https://api.vasthood.com/api/docs/`

## Admin panel
`https://api.vasthood.com/admin/`
