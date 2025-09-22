// Import required symbols
const { HttpInstrumentation } = require ('@opentelemetry/instrumentation-http');
const { ExpressInstrumentation } = require ('@opentelemetry/instrumentation-express');
const { registerInstrumentations } = require('@opentelemetry/instrumentation');
const { GraphQLInstrumentation } = require ('@opentelemetry/instrumentation-graphql');
const { OTLPTraceExporter } = require("@opentelemetry/exporter-trace-otlp-proto");
const { NodeSDK } = require('@opentelemetry/sdk-node');
const { ConsoleSpanExporter } = require('@opentelemetry/sdk-trace-base');

registerInstrumentations({
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new GraphQLInstrumentation()
  ]
});
const consoleExport = new ConsoleSpanExporter()
const sdk = new NodeSDK({
  traceExporter: 
  new OTLPTraceExporter({
    url: 'http://localhost:4318/v1/traces',
  })
  ,
  serviceName:"graphql",
  instrumentations: [
    new HttpInstrumentation(),
    new ExpressInstrumentation(),
    new GraphQLInstrumentation()
    ],
});

sdk.start();
