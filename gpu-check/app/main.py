import torch

if __name__ == "__main__":
    print(f"gpu available: {torch.cuda.is_available()}")
    count = torch.cuda.device_count()
    print(f"gpu count: {count}")

    for i in range(count):
        print(f"{i}, {torch.cuda.get_device_name(i)}")
