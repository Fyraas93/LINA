"""
Module for generating embeddings for log messages.
"""
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_random_exponential


class LogEmbedder:
    """Class for generating embeddings for log messages."""

    def __init__(self, model="text-embedding-3-small", api_key=None):
        """
        Initialize the log embedder.

        Args:
            model: OpenAI embedding model to use
            api_key: OpenAI API key (will use OPENAI_API_KEY env var if None)
        """
        
        load_dotenv()

        # Explicitly get API key from environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Error: OpenAI API key not configured.")
            self.client = None
        else:
            self.client = OpenAI(api_key=self.api_key)

        self.model = model

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(5))
    def generate_embedding(self, text):
        """
        Generate embedding for a single text string.

        Args:
            text: Text to generate embedding for

        Returns:
            list: Embedding vector as a list of floats, or None if generation fails
        """
        if not self.client:
            print("OpenAI client not initialized. Cannot generate embeddings.")
            return None

        if not text or not isinstance(text, str):
            print("Invalid or empty text.")
            return None

        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=text,
                encoding_format="float"
            )
            # Convert to native Python list for better compatibility
            embedding = response.data[0].embedding
            return embedding
        except Exception as e:
            print(f"Error generating embedding via OpenAI: {e}")
            raise e  # Let tenacity handle retry

    def generate_embeddings(self, texts, batch_size=20):
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of text strings
            batch_size: Number of embeddings to generate in each batch

        Returns:
            list: List of embedding vectors (lists of floats)
        """
        if not self.client:
            print("OpenAI client not initialized. Cannot generate embeddings.")
            return [None] * len(texts)

        embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch,
                    encoding_format="float"
                )
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
            except Exception as e:
                print(f"Error generating batch embeddings: {e}")
                embeddings.extend([None] * len(batch))
        return embeddings

    def generate_embeddings_for_logs(self, logs_df, text_column="log_message", batch_size=20):
        """
        Generate embeddings for a DataFrame of logs.

        Args:
            logs_df: DataFrame containing log data
            text_column: Column name containing text to embed
            batch_size: Number of embeddings to generate in each batch

        Returns:
            DataFrame: Original DataFrame with 'embedding' column added
        """
        if logs_df is None or text_column not in logs_df.columns:
            print(f"Error: Invalid log DataFrame or column \'{text_column}\' not found.")
            return None

        print(f"Starting embedding generation for column \'{text_column}\'...")

        texts = logs_df[text_column].astype(str).tolist()
        embeddings = self.generate_embeddings(texts, batch_size=batch_size)

        result_df = logs_df.copy()
        result_df["embedding"] = embeddings

        # Print embedding statistics
        valid_embeddings = sum(e is not None for e in embeddings)
        print(f"Embedding generation completed. {valid_embeddings}/{len(embeddings)} valid embeddings created.")

        return result_df

