# SmartMed Finder 🏥🔍

An intelligent Hospital Information Retrieval System that leverages Information Retrieval (IR) techniques such as TF-IDF vectorization and cosine similarity to recommend relevant doctors and hospitals based on user symptoms and search intent.

The system bridges the gap between user intent and healthcare search results by understanding semantic relevance instead of relying solely on exact keyword matching.

---

## 🚀 Features

* 🔍 Symptom-based doctor recommendation
* 🧠 TF-IDF vectorization for semantic retrieval
* 📊 Cosine similarity ranking
* ⭐ Ranking based on relevance, ratings, and experience
* 🗺️ Map-based hospital visualization
* 📅 Appointment booking simulation
* ⚡ Real-time search results
* 🎯 Query expansion for improved recall
* 🌐 Interactive Streamlit interface

---

## 🛠️ Tech Stack

### Languages & Frameworks

* Python
* Streamlit

### Libraries

* Pandas
* NumPy
* Scikit-learn

### Information Retrieval Techniques

* TF-IDF Vectorization
* Cosine Similarity
* Query Expansion
* Ranking Algorithms

---

## 🧩 System Workflow

User Query → Query Preprocessing → TF-IDF Vectorization → Cosine Similarity Calculation → Ranking Mechanism → Top Doctor Recommendations

---

## 📂 Project Structure

```bash
SmartMed-Finder/
│
├── app.py
├── requirements.txt
├── README.md
│
├── dataset/
│   └── improved_hospital_ir_dataset.xlsx
│
├── utils/
│   ├── search.py
│   ├── preprocessing.py
│   
│
└── assets/
```

---
## 📸 Screenshots

### Homepage

<img width="1820" height="1019" alt="homepage_ir" src="https://github.com/user-attachments/assets/d6f6f769-b5b1-4c19-b6dd-ecad1936a748" />


### Search Results

<img width="1709" height="872" alt="search" src="https://github.com/user-attachments/assets/f6312c7c-136d-4f2a-b4e0-bda0a2f0012b" />


### Appointment Booking

<img width="1919" height="1014" alt="booking" src="https://github.com/user-attachments/assets/efaf7770-ca6d-48a3-b2d5-1ee812beda8e" />


### Map Visualization

<img width="1857" height="1028" alt="map_location" src="https://github.com/user-attachments/assets/b15d904d-9223-41d4-90a8-0b0345292cf0" />





---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/SmartMed-Finder.git
cd SmartMed-Finder
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

## 📈 Key Concepts Used

* TF-IDF (Term Frequency–Inverse Document Frequency)
* Cosine Similarity
* Information Retrieval Pipeline
* Query Expansion
* Ranking Mechanisms
* NLP-based Search

---

## 🎯 Future Enhancements

* Integration with real hospital APIs
* Deep learning-based semantic search
* Voice-based search
* Personalized recommendations
* Mobile application development

---

## 👩‍💻 Author

**Taruni Middela**

AI & Machine Learning Enthusiast passionate about NLP, Information Retrieval, and Generative AI systems.

---

## ⭐ Acknowledgements

Built using:

* Streamlit
* Scikit-learn
* Pandas
* NumPy
