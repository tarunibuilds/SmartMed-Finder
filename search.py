import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.preprocess import preprocess_text

class SearchEngine:
    def __init__(self, df):
        self.df = df.copy()

        # Combine fields
        self.df["content"] = (
            self.df["specialization"].astype(str) + " " +
            self.df["sub_specialization"].astype(str) + " " +
            self.df["symptoms"].astype(str) + " " +
            self.df["description"].astype(str)
        )

        self.df["content"] = self.df["content"].apply(preprocess_text)

        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["content"])

    # =========================
    # TF-IDF SEARCH (FIXED)
    # =========================
    def tfidf_search(self, query):
        query = preprocess_text(query)

        synonyms = {
            "cardiologist": "heart cardiac cardiology chest pain",
            "skin": "dermatology dermatologist acne rash",
            "child": "pediatrician kids baby",
            "brain": "neurologist neuro headache",
            "fever": "viral infection temperature body pain"
        }

        for word, expansion in synonyms.items():
            if word in query:
                query += " " + expansion

        query_vec = self.vectorizer.transform([query])
        scores = cosine_similarity(query_vec, self.tfidf_matrix).flatten()

        self.df["score"] = scores

        results = self.df.sort_values(by="score", ascending=False)

        # Remove weak matches
        results = results[results["score"] > 0.01]

        return results.head(20)

    # =========================
    # BOOLEAN SEARCH
    # =========================
    def boolean_search(self, query):
        query = query.lower()

        if " and " in query:
            terms = query.split(" and ")
            result = self.df[
                self.df["content"].str.contains(terms[0]) &
                self.df["content"].str.contains(terms[1])
            ]
        elif " or " in query:
            terms = query.split(" or ")
            result = self.df[
                self.df["content"].str.contains(terms[0]) |
                self.df["content"].str.contains(terms[1])
            ]
        else:
            result = self.df[self.df["content"].str.contains(query)]

        return result.head(20)