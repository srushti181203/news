import nltk
import pickle
from scraper import fetch_article
from vectorizer import preprocess_text

# Ensure punkt is downloaded (needed for NLTK tokenizers)
nltk.download('punkt')

# Load your trained model and vectorizer
model = pickle.load(open('fake_news_model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))


def predict_news(news_text: str) -> str:
    """
    Preprocess the input text, vectorize it, and predict using the trained model.
    Returns 'Fake News' or 'Real News'.
    """
    cleaned_text = preprocess_text(news_text)
    vect_text = vectorizer.transform([cleaned_text])
    prediction = model.predict(vect_text)[0]
    return 'Fake News' if prediction == 1 else 'Real News'


def main():
    print("📢 Real-time Fake News Checker")
    print("Enter 'URL <url>' to check a news link or 'TEXT <your news>' to check news text directly.")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nYour Input: ")
        if user_input.lower() == 'exit':
            break

        if user_input.lower().startswith("url "):
            url = user_input[4:].strip()
            article_data = fetch_article(url)  # dict from scraper.py

            if article_data and "text" in article_data and article_data["text"].strip():
                article_text = article_data["text"]
                result = predict_news(article_text)
                print(f"\n📰 Title: {article_data.get('title', 'N/A')}")
                print(f"✅ Prediction: {result}")
            else:
                print("❌ Failed to fetch or extract article text.")

        elif user_input.lower().startswith("text "):
            news_text = user_input[5:].strip()
            if news_text:
                result = predict_news(news_text)
                print(f"\n📰 Entered News Prediction: {result}")
            else:
                print("❌ Please provide some text after 'TEXT '.")

        else:
            print("❗ Invalid format. Use 'URL <url>' or 'TEXT <news text>'.")


if __name__ == '__main__':
    main()
