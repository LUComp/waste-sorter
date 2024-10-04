# Waste Sorter

## Resnet50
### Dataset
The dataset can be downloaded [here](https://www.dropbox.com/scl/fi/iqdp1yqlpczd6oyoqu2a8/dataset.zip?rlkey=l1qq1vq9zdma1095nw1boymoc&st=kdaaomas&dl=0)
### Model
The model can be downloaded [here]()

## Control Flow

```
on start:
    lock lock
    move to detect
    once in detect pos, unlock lock

on video frame -> detect done:
    if locked, continue
    lock lock
    get detect position
    move robot to detect position @ fixed height
    start classify

on classify done:
    move to lower height above obj
    open gripper
    move down
    close gripper
    move up
    move to bin (up)
    move down
    open gripper
    move up
    close gripper
    move to detect
    unlock lock
```