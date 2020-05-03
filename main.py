from data_handler import prepare_dataset
from model import train_model
from model import test_model

dataset = prepare_dataset()
print("Dataset Prepared")

model = train_model(dataset)
print("Model Trained")

test_model(model)
print("Model Tested")
