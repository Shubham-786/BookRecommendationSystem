import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

class BookRecommendationModel:
    def __init__(self):
        """
        Initializing the BookRecommendationModel with a placeholder for the model.
        """
        self.model = None

    def prepare_and_train_model(self, data: pd.DataFrame, target_column: str, test_size: float = 0.2):
        """
        Preparing the data and training a RandomForestClassifier model.

        Args:
            data (pd.DataFrame): The input data containing features and target.
            target_column (str): The name of the target column in the data.
            test_size (float): The proportion of the dataset to include in the test split. Defaults to 0.2.
        """
        X = data.drop(columns=[target_column])
        y = data[target_column]

        X = pd.get_dummies(X, drop_first=True)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
        self.model = RandomForestClassifier()
        self.model.fit(X_train, y_train)

    def predict(self, genre: str, average_rating: float) -> int:
        """
        Predicting whether a book is recommended based on its genre and average rating.

        Args:
            genre (str): The genre of the book.
            average_rating (float): The average rating of the book.

        Returns:
            int: The prediction, where 1 means recommended and 0 means not recommended.
        """
        genre_code = {
            'Fiction': 0,
            'Non-Fiction': 1,
            'Science Fiction': 2,
            'Fantasy': 3,
            'Horror': 4
        }[genre]
        
        prediction = self.model.predict([[genre_code, average_rating]])
        return prediction[0]

books_data = pd.DataFrame({
    'genre': ['Fiction', 'Non-Fiction', 'Science Fiction', 'Fantasy', 'Horror'],
    'average_rating': [4.1, 3.9, 4.7, 4.2, 3.8],
    'recommended': [1, 0, 1, 1, 0]
})

model = BookRecommendationModel()
model.prepare_and_train_model(books_data, target_column='recommended')
