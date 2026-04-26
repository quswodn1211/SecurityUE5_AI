import requests
import json
from torch.utils.data import DataLoader
from data_join.set_data import MovementJsonlDataset
from ai.train import train_model

data_folder = "data/"

dataset = MovementJsonlDataset(
    jsonl_path=data_folder + "output.jsonl",
    sequence_length=30,
    feature_dim=15
)

train_loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

print("훈련 시작")
model = train_model(train_loader, epochs=10)