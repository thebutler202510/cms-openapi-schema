```python
import json
import os
### File: `master_schema_router.py`
```python
import json
import os

# Load your catalog file
with open('cms_catalog.json', 'r') as f:
    catalog = json.load(f)

query = os.environ.get("GPT_QUERY", "plan finder drug cost")

# Search catalog by keyword
best_match = None
for dataset in catalog.get("dataset", []):
    title = dataset.get("title", "")
    description = dataset.get("description", "")
    if query.lower() in (title + description).lower():
        best_match = dataset
        break

# Generate schema from match
if best_match:
    dist = best_match.get("distribution", [])[0]
    access_url = dist.get("accessURL") or dist.get("downloadURL")
    schema = {
        "openapi": "3.1.0",
        "info": {
            "title": best_match.get("title"),
            "version": "1.0.0",
            "description": best_match.get("description")
        },
        "servers": [{"url": access_url.rsplit('/', 1)[0]}],
        "paths": {
            "/data": {
                "get": {
                    "summary": best_match.get("title"),
                    "operationId": "getData",
                    "responses": {
                        "200": {"description": "Success"}
                    }
                }
            }
        }
    }
    with open("schema_output.json", "w") as f:
        json.dump(schema, f, indent=2)
else:
    print("No matching schema found.")
```
