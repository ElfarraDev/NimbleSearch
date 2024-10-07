import argparse
import json
from .index import NimbleSearch

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description="NimbleSearch: A lightweight search index for small to medium-sized datasets.")
    parser.add_argument('action', choices=['create', 'search', 'add', 'remove'], help="Action to perform")
    parser.add_argument('--index', required=True, help="Path to the index file")
    parser.add_argument('--text-fields', nargs='+', help="Text fields to index")
    parser.add_argument('--keyword-fields', nargs='+', help="Keyword fields to index")
    parser.add_argument('--documents', help="Path to JSON file containing documents to index")
    parser.add_argument('--query', help="Search query")
    parser.add_argument('--filters', help="JSON string of filters to apply")
    parser.add_argument('--boost', help="JSON string of boost values for fields")
    parser.add_argument('--num-results', type=int, default=10, help="Number of results to return")
    parser.add_argument('--document', help="JSON string of a document to add or remove")
    parser.add_argument('--document-id', type=int, help="ID of the document to remove")

    args = parser.parse_args()

    if args.action == 'create':
        if not args.text_fields or not args.keyword_fields or not args.documents:
            parser.error("create action requires --text-fields, --keyword-fields, and --documents")

        docs = load_json(args.documents)
        index = NimbleSearch(args.text_fields, args.keyword_fields)
        index.fit(docs)
        index.save(args.index)
        print(f"Index created and saved to {args.index}")

    elif args.action == 'search':
        if not args.query:
            parser.error("search action requires --query")

        index = NimbleSearch.load(args.index)
        filters = json.loads(args.filters) if args.filters else {}
        boost = json.loads(args.boost) if args.boost else {}

        results = index.search(args.query, filter_dict=filters, boost_dict=boost, num_results=args.num_results)
        for result in results:
            print(json.dumps(result))

    elif args.action == 'add':
        if not args.document:
            parser.error("add action requires --document")

        index = NimbleSearch.load(args.index)
        doc = json.loads(args.document)
        index.add_document(doc)
        index.save(args.index)
        print(f"Document added and index saved to {args.index}")

    elif args.action == 'remove':
        if args.document_id is None:
            parser.error("remove action requires --document-id")

        index = NimbleSearch.load(args.index)
        index.remove_document(args.document_id)
        index.save(args.index)
        print(f"Document removed and index saved to {args.index}")

if __name__ == "__main__":
    main()
