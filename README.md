# GraphQL OTEL Observability
This repo is a demo of using OTEL for GraphQL and turning traces to metrics for observability.

## Prerequisites
- You will need NPM installed.
- You will need docker installed.
- You will need python 3 installed.

## Directories
- `/alert-creator`: a python script to parse a graphql schema to generate alerts on Grafana automatically
- `/grafana-stack`: Grafana, Prometheus, and Tempo stack.
- `/graphql-server`: A simple Node server using OTEL auto-instrumentation and Apollo GraphQL.

## How to run
1. Start Grafana stack.
```
cd grafana-stack
docker compose up --build
```

2. Start GraphQL server (in a separate terminal)
```
cd graphql-server
npm i
npm start
```

3. Regenerate Grafana alerts if necessary
```
cd alert-creator
npx apollo client:download-schema --endpoint=http://localhost:4000  schema.graphql
python3 main.py

# restart Grafana docker instance
```

## How to test
Go to https://studio.apollographql.com/sandbox/explorer
Set the URL as http://localhost:4000/graphql
Start building queries.

Go to http://localhost:3000 to navigate to Grafana.