import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class ParquetStorage:
    def __init__(self, base_path: Path):
        self.base_path = base_path

    def save(self, df, table_name: str, extraction_date)->Path:
        """
        Saves the given DataFrame as a parquet file in the appropriate directory structure.
        Args:
            df (pd.DataFrame): The DataFrame to save.
            table_name (str): The name of the table (used for naming the parquet file).
            extraction_date (pd.Timestamp): The date of extraction (used for directory structure).
        """
        # Build the directory path based on the extraction date
        dir_path = self.build_directory_path(extraction_date)

        # Generate a timestamp for the file name
        # It will used to create a unique file name for the parquet file based on the extraction date and time
        timestamp = extraction_date.strftime("%Y%m%d_%H%M%S")

        # Define the file path for the parquet file
        file_path = dir_path / f"{table_name}_{timestamp}.parquet"
        try:
            # Create the directory if it doesn't exist
            dir_path.mkdir(parents=True, exist_ok=True)

            df.to_parquet(file_path, index=False)

            logger.info(f"Raw data saved to {file_path}")

            return file_path
        
        except Exception as e:
            logger.exception(f"Failed to save DataFrame to {file_path}: {e}")
            raise


    def build_directory_path(self, extraction_date):
        """
        Builds the directory path based on the extraction date.
        Args:
            extraction_date (pd.Timestamp): The date of extraction.

        Returns:
            Path: The directory path based on the extraction date.
        """
        return self.base_path / str(extraction_date.year) / f"{extraction_date.month:02d}" / f"{extraction_date.day:02d}"