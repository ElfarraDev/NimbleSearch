import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from typing import List, Dict, Any
import joblib
import os

class NimbleSearch:
    """
    A lightweight search index using TF-IDF and cosine similarity for text fields and exact matching for keyword fields.
    """

    def __init__(self, text_fields: List[str], keyword_fields: List[str], vectorizer_params: Dict[str, Any] = {}):
        """
        Initializes the NimbleSearch with specified text and keyword fields.

        Args:
            text_fields (List[str]): List of text field names to index.
            keyword_fields (List[str]): List of keyword field names to index.
            vectorizer_params (Dict[str, Any]): Optional parameters to pass to TfidfVectorizer.
        """
        self.text_fields = text_fields
        self.keyword_fields = keyword_fields
        self.vectorizers = {field: TfidfVectorizer(**vectorizer_params) for field in text_fields}
        self.keyword_df = None
        self.text_matrices = {}
        self.docs = []

    def fit(self, docs: List[Dict[str, Any]]):
        """
        Fits the index with the provided documents.

        Args:
            docs (List[Dict[str, Any]]): List of documents to index. Each document is a dictionary.

        Returns:
            NimbleSearch: The fitted index.
        """
        self.docs = docs
        keyword_data = {field: [] for field in self.keyword_fields}

        for field in self.text_fields:
            texts = [doc.get(field, '') for doc in docs]
            self.text_matrices[field] = self.vectorizers[field].fit_transform(texts)

        for doc in docs:
            for field in self.keyword_fields:
                keyword_data[field].append(doc.get(field, ''))

        self.keyword_df = pd.DataFrame(keyword_data)
        return self

    def search(self, query: str, filter_dict: Dict[str, Any] = {}, boost_dict: Dict[str, float] = {}, num_results: int = 10):
        """
        Searches the index with the given query, filters, and boost parameters.

        Args:
            query (str): The search query string.
            filter_dict (Dict[str, Any]): Dictionary of keyword fields to filter by. Keys are field names and values are the values to filter by.
            boost_dict (Dict[str, float]): Dictionary of boost scores for text fields. Keys are field names and values are the boost scores.
            num_results (int): The number of top results to return. Defaults to 10.

        Returns:
            List[Dict[str, Any]]: List of documents matching the search criteria, ranked by relevance.
        """
        query_vecs = {field: self.vectorizers[field].transform([query]) for field in self.text_fields}
        scores = np.zeros(len(self.docs))

        # Compute cosine similarity for each text field and apply boost
        for field, query_vec in query_vecs.items():
            sim = cosine_similarity(query_vec, self.text_matrices[field]).flatten()
            boost = boost_dict.get(field, 1)
            scores += sim * boost

        # Apply keyword filters
        for field, value in filter_dict.items():
            if field in self.keyword_fields:
                mask = self.keyword_df[field] == value
                scores = scores * mask.to_numpy()

        # Use argpartition to get top num_results indices
        top_indices = np.argpartition(scores, -num_results)[-num_results:]
        top_indices = top_indices[np.argsort(-scores[top_indices])]

        # Filter out zero-score results and add score to results
        top_docs = [
            {**self.docs[i], 'score': float(scores[i])}  # Convert numpy float to Python float for JSON serialization
            for i in top_indices if scores[i] > 0
        ]

        return top_docs

    def save(self, path: str):
        """
        Saves the index to a file.

        Args:
            path (str): The file path to save the index.
        """
        joblib.dump(self, path)

    @classmethod
    def load(cls, path: str):
        """
        Loads the index from a file.

        Args:
            path (str): The file path to load the index from.

        Returns:
            NimbleSearch: The loaded index.
        """
        return joblib.load(path)

    def add_document(self, doc: Dict[str, Any]):
        """
        Adds a single document to the index.

        Args:
            doc (Dict[str, Any]): The document to add.
        """
        self.docs.append(doc)

        for field in self.text_fields:
            text = doc.get(field, '')
            new_vector = self.vectorizers[field].transform([text])
            self.text_matrices[field] = np.vstack((self.text_matrices[field].toarray(), new_vector.toarray()))

        new_keyword_data = {field: [doc.get(field, '')] for field in self.keyword_fields}
        self.keyword_df = pd.concat([self.keyword_df, pd.DataFrame(new_keyword_data)], ignore_index=True)

    def remove_document(self, index: int):
        """
        Removes a document from the index by its index.

        Args:
            index (int): The index of the document to remove.
        """
        if 0 <= index < len(self.docs):
            del self.docs[index]

            for field in self.text_fields:
                self.text_matrices[field] = np.delete(self.text_matrices[field].toarray(), index, axis=0)

            self.keyword_df = self.keyword_df.drop(index).reset_index(drop=True)
        else:
            raise IndexError("Document index out of range")
