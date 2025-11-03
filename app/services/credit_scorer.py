from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import joblib
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CreditScorer:
    """
    A class to handle credit scoring predictions using a unified sklearn pipeline.
    """
    def __init__(self, pipeline_path: str):
        """
        Initialize the CreditScorer with a unified pipeline.

        Args:
            pipeline_path (str): Path to the pipeline.joblib file
        """
        self.pipeline = self._load_pipeline(pipeline_path)
        self.scorer_meaning = {
            False: 'No payment difficulties',
            True: 'Payment difficulties'
        }
        
    def _load_pipeline(self, path: str) -> Any:
        """
        Load a joblib pipeline file safely.

        Args:
            path (str): Path to the pipeline.joblib file

        Returns:
            Any: Loaded pipeline object

        Raises:
            FileNotFoundError: If the file doesn't exist
            Exception: If there's an error loading the file
        """
        try:
            path_obj = Path(path)
            if not path_obj.exists():
                raise FileNotFoundError(f"Pipeline file not found at {path}")
                
            return joblib.load(path)
        except Exception as e:
            logger.error(f"Error loading pipeline from {path}: {str(e)}")
            raise

    def transform(self, data: pd.DataFrame, client_id: Dict[str, int]) -> pd.DataFrame:
        """
        Filter and prepare the features for prediction.

        Args:
            data (pd.DataFrame): Input data frame
            client_id (dict): Dictionary containing client ID

        Returns:
            pd.DataFrame: Filtered features ready for prediction

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

        # Select features (remove TARGET and SK_ID_CURR)
        X = df.drop(['TARGET', 'SK_ID_CURR'], axis=1)
        
        return X

    def make_prediction(self, features: pd.DataFrame) -> Tuple[float, str]:
        """
        Predicts the credit score using the unified pipeline.

        Args:
            features (pd.DataFrame): Raw features (pipeline handles preprocessing)

        Returns:
            Tuple[float, str]: Probability and prediction interpretation
            
        Raises:
            ValueError: If features are not in the correct format
        """
        try:
            # Pipeline handles both preprocessing and prediction
            prob = self.pipeline.predict_proba(features)[:, 1]
            
            # Threshold decision (0.47 from optimization)
            pred = (prob >= 0.47)[0]
            
            # Get interpretation
            score = self.scorer_meaning[pred]
            
            return prob, score
        except Exception as e:
            logger.error(f"Error making prediction: {str(e)}")
            raise