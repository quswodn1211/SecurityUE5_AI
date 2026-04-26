import requests
import json
from fastapi import FastAPI
from torch.utils.data import DataLoader
from ai.predict import predict_anomaly
from ai.set_data import MovementDataset
from ai.train import train_model

class LogResult():
    def __init__(self, player_id: int, abnormal_ratio: float):
        self.player_id = player_id
        self.abnormal_ratio = abnormal_ratio



# 디비와의 통신 GET
app = FastAPI()

response = requests.get(f"http://~~~~ 디비 주소/api/log/{log_id}")

if response.status_code == 200:
    data = response.json()

    player_id = data["player_id"]
    sequence = data["sequence"]

    print(player_id)
    print(sequence)
else:
    print("로그 가져오기 실패:", response.status_code)


# 데이터셋 생성


dataset = MovementDataset(
    jsonl_path="movement_train.jsonl",
    sequence_length=30,
    feature_dim=12
)

train_loader = DataLoader(
    dataset,
    batch_size=64,
    shuffle=True
)

model = train_model(train_loader, epochs=10)


# 결과를 저장하고 디비와의 통신 POST
result = LogResult(player_id=player_id, abnormal_ratio=predict_anomaly(sequence))

response = requests.post(
    "http://~~~~~ 디비 주소/analysis_result",
    json=result
)
