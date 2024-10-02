import torch

def save_checkpoint(model, optimizer, epoch, loss, filepath):
    """
    Save the model and optimizer state, along with the current epoch and loss.
    """
    checkpoint = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'loss': loss
    }
    torch.save(checkpoint, filepath)

def load_checkpoint(model, optimizer, filepath):
    """
    Load the model and optimizer state from a checkpoint file.
    """
    checkpoint = torch.load(filepath, weights_only=True)
    model.load_state_dict(checkpoint['model_state_dict'])
    optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    epoch = checkpoint['epoch']
    loss = checkpoint['loss']
    return epoch, loss