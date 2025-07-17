"""
Module for storing log embeddings in Milvus.
"""
import os
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from pymilvus import connections, utility, Collection, DataType, FieldSchema, CollectionSchema


class MilvusStorage:
    """Class for storing log embeddings in Milvus."""

    def __init__(self, host="localhost", port="19530", collection_name="log_embeddings", embedding_dim=1536):
        """
        Initialize the Milvus storage.
        """
        load_dotenv()
        self.host = os.getenv("MILVUS_HOST", host)
        self.port = int(os.getenv("MILVUS_PORT", port))
        self.collection_name = collection_name
        self.embedding_dim = embedding_dim
        self.collection = None
        self._connect()

    def _connect(self):
        """Connect to Milvus server and initialize collection."""
        try:
            if connections.has_connection("default"):
                connections.disconnect("default")
            print(f"Connecting to Milvus at {self.host}:{self.port}")
            connections.connect(
                alias="default",
                host=self.host,
                port=self.port,
                timeout=30
            )
            self._load_or_create_collection()
        except Exception as e:
            print(f"Failed to connect to Milvus: {e}")
            self.collection = None

    def _create_schema(self):
        """Create schema for the collection."""
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.embedding_dim),
            FieldSchema(name="log_message", dtype=DataType.VARCHAR, max_length=10000),
            FieldSchema(name="timestamp", dtype=DataType.VARCHAR, max_length=100),
            FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=500),
            FieldSchema(name="severity", dtype=DataType.VARCHAR, max_length=20),
            FieldSchema(name="anomaly_flag", dtype=DataType.BOOL, default_value=False),
            FieldSchema(name="anomaly_reason", dtype=DataType.VARCHAR, max_length=500, default_value=""),
            FieldSchema(name="target_label", dtype=DataType.VARCHAR, max_length=100),
        ]
        schema = CollectionSchema(
            fields=fields,
            description="Log embeddings collection",
            enable_dynamic_field=True
        )
        return schema

    def _load_or_create_collection(self):
        """Load existing collection or create a new one."""
        try:
            has_collection = utility.has_collection(self.collection_name, using="default")
            if has_collection:
                self.collection = Collection(self.collection_name, using="default")
            else:
                print(f"Creating new collection '{self.collection_name}'...")
                schema = self._create_schema()
                self.collection = Collection(
                    name=self.collection_name,
                    schema=schema,
                    using="default"
                )
                self._create_index()
            self.collection.load()
        except Exception as e:
            print(f"Error loading/creating collection: {e}")
            raise

    def _create_index(self):
        """Create index on embedding field for faster search."""
        if not self.collection:
            return
        try:
            index_params = {
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024}
            }
            print("Creating index on embedding field...")
            self.collection.create_index(
                field_name="embedding",
                index_params=index_params
            )
            print("Index created successfully!")
        except Exception as e:
            print(f"Error creating index: {e}")

    def _prepare_embeddings(self, embeddings):
        """
        Prepare embeddings for Milvus insertion.
        """
        result = []
        for emb in embeddings:
            if emb is None:
                continue
            if isinstance(emb, list):
                if len(emb) != self.embedding_dim:
                    if len(emb) < self.embedding_dim:
                        emb = emb + [0.0] * (self.embedding_dim - len(emb))
                    else:
                        emb = emb[:self.embedding_dim]
                result.append(np.array([float(v) for v in emb], dtype=np.float32))
            elif isinstance(emb, np.ndarray):
                if emb.size != self.embedding_dim:
                    if emb.size < self.embedding_dim:
                        padded = np.zeros(self.embedding_dim, dtype=np.float32)
                        padded[:emb.size] = emb.flatten()
                        result.append(padded)
                    else:
                        result.append(emb.flatten()[:self.embedding_dim].astype(np.float32))
                else:
                    result.append(emb.flatten().astype(np.float32))
            else:
                print(f"Invalid embedding format: {type(emb)}")
        return result

    def store_logs(self, df_logs):
        """
        Store logs with embeddings in Milvus.
        Args:
            df_logs: DataFrame containing logs with embeddings
        Returns:
            bool: True if storage was successful, False otherwise
        """
        if not self.collection:
            print("No collection available. Cannot insert data.")
            return False
        if df_logs is None or df_logs.empty:
            print("No data to insert.")
            return False

        required_cols = ['embedding', 'log_message', 'timestamp']
        missing_cols = [col for col in required_cols if col not in df_logs.columns]
        if missing_cols:
            print(f"Missing required columns: {missing_cols}")
            return False

        valid_mask = df_logs['embedding'].notna()
        if not valid_mask.any():
            print("No valid embeddings found in the data.")
            return False

        df_valid = df_logs[valid_mask].copy()
        print(f"Inserting {len(df_valid)} records into Milvus...")

        try:
            numpy_embeddings = self._prepare_embeddings(df_valid["embedding"].tolist())
            if not numpy_embeddings:
                print("No valid embeddings to insert.")
                return False

            log_messages = df_valid["log_message"].astype(str).tolist()[:len(numpy_embeddings)]
            timestamps = df_valid["timestamp"].astype(str).tolist()[:len(numpy_embeddings)]
            sources = df_valid["source"].astype(str).tolist()[:len(numpy_embeddings)] if "source" in df_valid.columns else ["unknown"] * len(numpy_embeddings)
            labels = df_valid["target_label"].astype(str).tolist()[:len(numpy_embeddings)] if "target_label" in df_valid.columns else ["UNKNOWN"] * len(numpy_embeddings)
            anomaly_flags = df_valid["anomaly_flag"].tolist()[:len(numpy_embeddings)] if "anomaly_flag" in df_valid.columns else [False] * len(numpy_embeddings)
            anomaly_reasons = df_valid["anomaly_reason"].astype(str).tolist()[:len(numpy_embeddings)] if "anomaly_reason" in df_valid.columns else [""] * len(numpy_embeddings)
            severities = df_valid["severity"].astype(str).tolist()[:len(numpy_embeddings)] if "severity" in df_valid.columns else ["Info"] * len(numpy_embeddings)

            data = [
                {
                    "embedding": numpy_embeddings[i],
                    "log_message": log_messages[i],
                    "timestamp": timestamps[i],
                    "source": sources[i],
                    "target_label": labels[i],
                    "anomaly_flag": anomaly_flags[i],
                    "anomaly_reason": anomaly_reasons[i],
                    "severity": severities[i]
                }
                for i in range(len(numpy_embeddings))
            ]

            print("Inserting data into Milvus collection...")
            result = self.collection.insert(data)
            print("Flushing data to disk...")
            self.collection.flush()
            print(f"Successfully inserted {len(result.primary_keys)} records.")
            print(f"Collection now has {self.collection.num_entities} entities.")
            return True

        except Exception as e:
            print(f"Error inserting data: {e}")
            import traceback
            traceback.print_exc()
            return False

    def search_similar_logs(self, query_embedding, top_k=50, only_anomalies=False):
        """
        Search for similar logs based on embedding.
        """
        if not self.collection:
            print("No collection available. Cannot search.")
            return None
        if query_embedding is None:
            print("No query embedding provided.")
            return None

        try:
            if isinstance(query_embedding, list):
                query_embedding = np.array(query_embedding, dtype=np.float32)
            elif isinstance(query_embedding, np.ndarray):
                query_embedding = query_embedding.astype(np.float32)
            else:
                print(f"Invalid query embedding type: {type(query_embedding)}")
                return None

            if query_embedding.size != self.embedding_dim:
                if query_embedding.size < self.embedding_dim:
                    padded = np.zeros(self.embedding_dim, dtype=np.float32)
                    padded[:query_embedding.size] = query_embedding.flatten()
                    query_embedding = padded
                else:
                    query_embedding = query_embedding.flatten()[:self.embedding_dim]

            search_params = {
                "metric_type": "COSINE",
                "params": {"nprobe": 10}
            }
            output_fields = ["log_message", "timestamp", "source", "target_label", "anomaly_flag", "anomaly_reason", "severity"]
            expr = "anomaly_flag == true" if only_anomalies else None
            results = self.collection.search(
                data=[query_embedding],
                anns_field="embedding",
                param=search_params,
                limit=top_k,
                output_fields=output_fields,
                expr=expr
            )
            similar_logs = []
            for hit in results[0]:
                log_info = {
                    "id": hit.id,
                    "distance": hit.distance,
                    "log_message": hit.entity.get("log_message"),
                    "timestamp": hit.entity.get("timestamp"),
                    "source": hit.entity.get("source"),
                    "target_label": hit.entity.get("target_label"),
                    "anomaly_flag": hit.entity.get("anomaly_flag"),
                    "anomaly_reason": hit.entity.get("anomaly_reason"),
                    "severity": hit.entity.get("severity")
                }
                similar_logs.append(log_info)
            print("Milvus retrieval complete.")
            return similar_logs

        except Exception as e:
            print(f"Error during search: {e}")
            return None

    def disconnect(self):
        """Disconnect from Milvus."""
        try:
            if connections.has_connection("default"):
                connections.disconnect("default")
                print("Disconnected from Milvus.")
        except Exception as e:
            print(f"Error disconnecting: {e}")