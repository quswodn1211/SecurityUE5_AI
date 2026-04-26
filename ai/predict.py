from AnomalyDataRNN import MovementAnomalyRNN
import torch


def predict_anomaly(x):
    model = MovementAnomalyRNN(feature_dim=12)
    model.load_state_dict(torch.load("movement_anomaly_rnn.pt"))
    model.eval()

    with torch.no_grad():
        logits = model(x)
        prob = torch.sigmoid(logits)

    return prob