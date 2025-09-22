import re
import yaml
import uuid

def extract_types(graphql_schema):
    """
    Extracts type definitions and list types from a GraphQL schema string.
    """
    all_types = set()

    # Regex to find object type definitions like `type Author {`
    type_pattern = re.compile(r'type\s+(\w+)\s*{')
    matches = type_pattern.findall(graphql_schema)
    all_types.update(matches)

    # Regex to find list types in the Query definition like `books: [Book]`
    list_type_pattern = re.compile(r':\s*\[(\w+)\]')
    list_matches = list_type_pattern.findall(graphql_schema)
    
    # Add the extracted list types and their bracketed forms
    for match in list_matches:
        all_types.add(f'[{match}]')
    
    # Remove the `Query` type, as it's not a data type in the same sense
    all_types.discard('Query')
        
    return sorted(list(all_types))

def generate_alert_yaml(types):
    """
    Generates a Grafana alerting YAML structure based on a list of types.
    """
    rules = []
    
    # Create an alert rule for each type
    for graphql_type in types:
        # A simple slug for the title
        slug = graphql_type.strip('[]')
        
        rule = {
            'uid': str(uuid.uuid4())[:14],  # Generate a unique ID
            'title': f'p95 {graphql_type} Query above 1s',
            'condition': 'C',
            'data': [
                {
                    'refId': 'A',
                    'relativeTimeRange': {'from': 600, 'to': 0},
                    'datasourceUid': 'prometheus',
                    'model': {
                        'editorMode': 'code',
                        'expr': f'histogram_quantile(0.95, sum(rate(traces_spanmetrics_latency_bucket{{graphql_field_type="{graphql_type}"}}[1m])) by (le))',
                        'instant': True,
                        'intervalMs': 1000,
                        'legendFormat': '__auto',
                        'maxDataPoints': 43200,
                        'range': False,
                        'refId': 'A'
                    }
                },
                {
                    'refId': 'C',
                    'datasourceUid': '__expr__',
                    'model': {
                        'conditions': [
                            {
                                'evaluator': {'params': [1], 'type': 'gt'},
                                'operator': {'type': 'and'},
                                'query': {'params': ['C']},
                                'reducer': {'params': [], 'type': 'last'},
                                'type': 'query'
                            }
                        ],
                        'datasource': {'type': '__expr__', 'uid': '__expr__'},
                        'expression': 'A',
                        'intervalMs': 1000,
                        'maxDataPoints': 43200,
                        'refId': 'C',
                        'type': 'threshold'
                    }
                }
            ],
            'noDataState': 'NoData',
            'execErrState': 'Error',
            'for': '1m',
            'annotations': {},
            'labels': {},
            'isPaused': False,
            'notification_settings': {
                'receiver': 'grafana-default-email'
            }
        }
        rules.append(rule)
    
    # Assemble the final YAML structure
    yaml_structure = {
        'apiVersion': 1,
        'groups': [
            {
                'orgId': 1,
                'name': 'GraphQL Latency Alerts',
                'folder': 'GraphQL',
                'interval': '1m',
                'rules': rules
            }
        ]
    }
    
    return yaml_structure

# Main script execution
file_name = "schema.graphql"
try:
    with open(file_name, 'r') as file:
        schema = file.read()
    
    extracted_types = extract_types(schema)
    print(f"Extracted types from '{file_name}': {extracted_types}")
    
    # Generate the YAML structure
    alert_yaml_data = generate_alert_yaml(extracted_types)
    
    # Write the YAML structure to a file
    output_file_name = '../grafana-stack/alerts/alerts.yaml'
    with open(output_file_name, 'w') as outfile:
        yaml.dump(alert_yaml_data, outfile, sort_keys=False)
        
    print(f"\nSuccessfully generated alerts and saved to '{output_file_name}'.")

except FileNotFoundError:
    print(f"Error: The file '{file_name}' was not found.")
    print("Please make sure your schema.graphql file is in the same directory as the script.")