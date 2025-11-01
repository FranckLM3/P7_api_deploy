from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import pickle
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CreditScorer:
    """
    A class to handle credit scoring predictions.
    """
    def __init__(self, preprocess_path: str, model_path: str):
        """
        Initialize the CreditScorer with preprocessor and model paths.

        Args:
            preprocess_path (str): Path to the preprocessor pickle file
            model_path (str): Path to the model pickle file
        """
        self.preprocessor = self._load_pickle(preprocess_path, "preprocessor")
        self.clf = self._load_pickle(model_path, "model")
        self.scorer_meaning = {
            False: 'No payment difficulties',
            True: 'Payment difficulties'
        }
        
    def _load_pickle(self, path: str, name: str) -> Any:
        """
        Load a pickle file safely.

        Args:
            path (str): Path to the pickle file
            name (str): Name of the object for logging

        Returns:
            Any: Loaded object

        Raises:
            FileNotFoundError: If the file doesn't exist
            pickle.UnpicklingError: If there's an error loading the file
        """
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                raise FileNotFoundError(f"{name} file not found at {path}")
                
            with open(path, "rb") as f:
                return pickle.load(f)
        except (pickle.UnpicklingError, Exception) as e:
            logger.error(f"Error loading {name} from {path}: {str(e)}")
            raise

    def transform(self, data: pd.DataFrame, client_id: Dict[str, int]) -> np.ndarray:
        """
        Preprocess the features for prediction.

        Args:
            data (pd.DataFrame): Input data frame
            client_id (dict): Dictionary containing client ID

        Returns:
            np.ndarray: Transformed features

        Raises:
            ValueError: If client ID is not found in the data
        """
        df = data.copy()
        df = df.replace([np.inf, -np.inf], np.nan)
        id_value = client_id['id']
        
        # Filter for client ID
        df = df[df['SK_ID_CURR'] == id_value]
        
        if df.empty:
            raise ValueError(f"Client ID {id_value} not found in the data")

        # Select features
        X = df.drop(['TARGET', 'SK_ID_CURR'], axis=1)
        
        # Transform features
        try:
            X_transformed = self.preprocessor.transform(X)
            return X_transformed
        except Exception as e:
            logger.error(f"Error transforming features: {str(e)}")
            raise

    def make_prediction(self, features: np.ndarray) -> Tuple[float, str]:
        """
        Predicts the credit score.

        Args:
            features (np.ndarray): Transformed features

        Returns:
            Tuple[float, str]: Probability and prediction interpretation
            
        Raises:
            ValueError: If features are not in the correct format
        """
        try:
            # Get probability of payment difficulties
            prob = self.clf.predict_proba(features)[:, 1]
            
            # Threshold decision
            pred = (prob >= 0.47)[0]
            
            # Get interpretation
            score = self.scorer_meaning[pred]
            
            return prob, score
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise