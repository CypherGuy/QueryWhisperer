import wandb
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from datasets import load_dataset
from dataset import extract_question_and_sql
from preprocess import tokenize, vocab_size, dimensions
from model import Seq2SeqModel

# Load dataset splits
dataset = load_dataset("wikisql")
train_ds = dataset["train"]
val_ds = dataset["validation"]
test_ds = dataset["test"]

# Init wandb
wandb.init(project="text-2-sql", name="training_real")


class WikiSQLDataset(Dataset):
    # Custom PyTorch dataset that returns 1D tensors for token IDs
    def __init__(self, hf_dataset):
        self.samples = []
        for sample in hf_dataset:
            question, sql = extract_question_and_sql(sample)
            # Tokenize and then take the first element to remove the extra batch dimension.
            question_ids, question_mask = tokenize(question)
            sql_ids, sql_mask = tokenize(sql)
            self.samples.append(
                (question_ids[0], question_mask[0], sql_ids[0], sql_mask[0]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        return self.samples[idx]


# Create dataset objects using our subset for training.
train_dataset = WikiSQLDataset(train_ds)
val_dataset = WikiSQLDataset(val_ds)
test_dataset = WikiSQLDataset(test_ds)

# Create dataloaders
train_dataloader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_dataloader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# Create model, optimizer and loss function
model = Seq2SeqModel(hidden_size=dimensions)
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.CrossEntropyLoss()

# Training loop
epochs = 3
for epoch in range(epochs):
    model.train()
    total_loss = 0.0
    for batch in train_dataloader:
        src_ids, src_mask, tgt_ids, tgt_mask = batch
        optimizer.zero_grad()
        logits = model(src_ids, tgt_ids)
        # Here we use Teacher Forcing, a strategy where the model predicts the next token using the actual corresponding target tokens over baseless predictions
        # This is used to help the model learn the correct sequence of tokens
        # First step, remove the final prediction as there's no target ie "next step" for it
        logits = logits[:, :-1, :].contiguous()
        # Second step, remove the first prediction as there's no target ie "previous step" for it
        target = tgt_ids[:, 1:].contiguous()

        loss = criterion(logits.view(-1, vocab_size), target.view(-1))
        loss.backward()  # Backprop
        optimizer.step()  # Update weights
        total_loss += loss.item()

    avg_loss = total_loss / len(train_dataloader)
    wandb.log({"epoch": epoch, "train_loss": avg_loss})

    # Validation loop
    model.eval()
    validation_loss = 0.0
    with torch.no_grad():
        for batch in val_dataloader:
            src_ids, src_mask, tgt_ids, tgt_mask = batch
            logits = model(src_ids, tgt_ids)
            logits = logits[:, :-1, :].contiguous()
            target = tgt_ids[:, 1:].contiguous()

            loss = criterion(logits.view(-1, vocab_size), target.view(-1))
            validation_loss += loss.item()
    avg_validation_loss = validation_loss / len(val_dataloader)
    wandb.log({"epoch": epoch, "val_loss": avg_validation_loss})

wandb.finish()
