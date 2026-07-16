import sys
import torch
import torch.nn as nn
import torch.optim as optim

sys.path.insert(0, "C:/Users/Sheran/Desktop/Parkinson")
from src.deep_learning.models.tabular_models import MLP
from src.deep_learning.training.trainer import Trainer

print("="*60)
print("STEP 2: 5-ITERATION LOSS CONVERGENCE TRACE (MLP)")
print("="*60)

try:
    # 1. Initialize Dummy Data from "Phase 6" characteristics
    # We use batch_size=2, input_dim=10 to emulate Tabular Data Features
    X = torch.randn(2, 10)
    y = torch.tensor([0, 1], dtype=torch.long) # Binary classification targets

    # Create dummy DataLoader yielding the same batch 5 times
    dataloader = [(X, y) for _ in range(5)]

    # 2. Initialize Model, Criterion, Optimizer
    model = MLP(input_dim=10, hidden_dims=[16], output_dim=2)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.1)

    # Note: Using cpu explicitly for the dummy run
    trainer = Trainer(model, optimizer, None, criterion, 'cpu', 'C:/Users/Sheran/Desktop/Parkinson/artifacts/deep_learning/checkpoints/')
    
    # Let's run a manual tight loop to print loss at each batch
    model.train()
    print("Executing Forward/Backward Passes...")
    for i, (batch_x, batch_y) in enumerate(dataloader):
        optimizer.zero_grad()
        outputs = model(batch_x)
        loss = criterion(outputs, batch_y)
        loss.backward()
        optimizer.step()
        print(f"Iteration {i+1}/5 - Loss: {loss.item():.4f}")

    # 3. Save and Load Checkpoint verification
    print("\\nTesting Checkpoint I/O (`best_model.pt`)...")
    import os
    os.makedirs('C:/Users/Sheran/Desktop/Parkinson/artifacts/deep_learning/checkpoints/', exist_ok=True)
    trainer.save_checkpoint(epoch=1, val_loss=loss.item(), is_best=True)
    
    ckpt_path = 'C:/Users/Sheran/Desktop/Parkinson/artifacts/deep_learning/checkpoints/best_model.pt'
    checkpoint = torch.load(ckpt_path)
    
    print("Checkpoint Loaded Successfully.")
    print("Keys in Checkpoint:", list(checkpoint.keys()))
    
    # Load state dict back to prove it works
    model.load_state_dict(checkpoint['model_state_dict'])
    
    # Print a tiny sample of the actual weights
    sample_weights = list(checkpoint['model_state_dict'].values())[0].flatten()[:3]
    print(f"Sample First Layer Weights from Disk: {sample_weights.tolist()}")
    
except Exception as e:
    import traceback
    print(f"FAILED: {e}")
    traceback.print_exc()
