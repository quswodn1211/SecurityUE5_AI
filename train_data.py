import requests
import json
from fastapi import FastAPI
from torch.utils.data import DataLoader
from ai.predict import predict_anomaly
from SecurityUE5_AI.data_join.set_data import MovementDataset
from ai.train import train_model

data_folder = "data/"

dataset = MovementDataset(
    jsonl_path=data_folder + "output.jsonl",
    sequence_length=30,
    feature_dim=15
)

train_loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

model = train_model(train_loader, epochs=10)