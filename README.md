# NimbleSearch

NimbleSearch is a lightweight, flexible search index for small to medium-sized datasets. It uses TF-IDF and cosine similarity for text fields and exact matching for keyword fields, providing a balance between performance and simplicity.

## Features

- Easy-to-use API for indexing and searching documents
- Command-line interface for quick operations
- Support for both text and keyword fields
- Customizable TF-IDF vectorization
- Field boosting for fine-tuned relevance
- Keyword filtering for precise results
- Persistence support (save/load functionality)
- Incremental updates to the index
- Docker support for easy deployment
- Automatic documentation generation

## Installation

You can install NimbleSearch using pip:

```bash
pip install nimble-search
```

Or clone the repository and install it locally:

```bash
git clone https://github.com/aelfarra/nimble-search.git
cd nimble-search
pip install -e .
```


## Quick Start

### Python API

```python
from nimble_search import NimbleSearch

# Create an index
index = NimbleSearch(text_fields=['title', 'content'], keyword_fields=['category'])

# Add documents
docs = [
    {'title': 'Python Programming', 'content': 'Python is a versatile programming language.', 'category': 'Programming'},
    {'title': 'Data Science with Python', 'content': 'Python is widely used in data science.', 'category': 'Data Science'},
    # ... more documents ...
]

index.fit(docs)

# Search
results = index.search('Python programming', filter_dict={'category': 'Programming'}, num_results=5)
for result in results:
    print(f"Title: {result['title']}, Score: {result['score']}")
```

## Command-Line Interface

NimbleSearch provides a command-line interface for quick operations:

#### Create an index:
```bash
nimble-search create --index myindex.pkl --text-fields title content --keyword-fields category --documents docs.json
```

#### Search the index:
```bash
nimble-search search --index myindex.pkl --query "Python programming" --filters '{"category": "Programming"}' --num-results 5
```

#### Add documents:
```bash
nimble-search add --index myindex.pkl --document '{"title": "New Python Course", "content": "Learn Python today!", "category": "Education"}'
```

#### Remove a document:
```bash
nimble-search remove --index myindex.pkl --document-id 2
```

## Docker Support

To run NimbleSearch using Docker:

### Build the Docker image:

```bash
docker build -t nimble-search .
```


### Run the container:

```bash
docker run -p 8080:80 nimble-search
```

Alternatively, you can use Docker Compose:

```bash
docker-compose up
```

### Documentation
To generate the documentation:

```bash
python setup.py build_docs
```

The generated documentation will be available in the docs/build/html directory.

## Development
To set up the development environment:

## Clone the repository:

```bash
git clone https://github.com/elfarradev/nimble-search.git
cd nimble-search
```


### Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```


### Install the development dependencies:
```bash
pip install -r requirements.txt
```

## Install the development dependencies:
```bash
pip install -r requirements.txt
```

## Run the tests:

```bash
python -m unittest discover tests
```

## Contributing

We welcome contributions to NimbleSearch! Please see our contributing guidelines for more details on how to get started.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Author

NimbleSearch is created and maintained by Ahmed Elfarra (elfarradev@gmail.com).
