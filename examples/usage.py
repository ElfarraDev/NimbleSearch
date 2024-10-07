from nimble_search import NimbleSearch
import json

# Sample documents
docs = [
    {'title': 'Python Programming', 'content': 'Python is a versatile programming language.', 'category': 'Programming'},
    {'title': 'Data Science with Python', 'content': 'Python is widely used in data science.', 'category': 'Data Science'},
    {'title': 'Web Development', 'content': 'Web development involves creating websites and web applications.', 'category': 'Web'},
]

# Create and fit the index
index = NimbleSearch(text_fields=['title', 'content'], keyword_fields=['category'])
index.fit(docs)

# Basic search
print("Basic search:")
results = index.search('Python programming')
for result in results:
    print(f"Title: {result['title']}, Score: {result['score']}")

# Search with filters
print("\nSearch with filters:")
results = index.search('Python', filter_dict={'category': 'Data Science'})
for result in results:
    print(f"Title: {result['title']}, Score: {result['score']}")

# Search with field boosting
print("\nSearch with field boosting:")
results = index.search('Python', boost_dict={'title': 2.0})
for result in results:
    print(f"Title: {result['title']}, Score: {result['score']}")

# Add a new document
new_doc = {'title': 'Machine Learning', 'content': 'Machine learning is a subset of AI.', 'category': 'AI'}
index.add_document(new_doc)

# Search after adding a new document
print("\nSearch after adding a new document:")
results = index.search('AI learning')
for result in results:
    print(f"Title: {result['title']}, Score: {result['score']}")

# Save and load the index
index.save('example_index.pkl')
loaded_index = NimbleSearch.load('example_index.pkl')

# Search using the loaded index
print("\nSearch using the loaded index:")
results = loaded_index.search('Python')
for result in results:
    print(f"Title: {result['title']}, Score: {result['score']}")
