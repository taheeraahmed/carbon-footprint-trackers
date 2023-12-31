
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image, ImageDraw, ImageFont

def object_detection(image_path, save_path="output.jpg"):
    # Initialize the model
    model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
    model.eval()

    # Load and preprocess the image
    input_image = Image.open(image_path).convert("RGB")
    preprocess = transforms.ToTensor()
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0)

    # Perform inference
    if torch.cuda.is_available():
        input_batch = input_batch.to("cuda")
        model.to("cuda")

    with torch.no_grad():
        output = model(input_batch)

    # Draw bounding boxes
    boxes = output[0]["boxes"].cpu().numpy()
    labels = output[0]["labels"].cpu().numpy()
    scores = output[0]["scores"].cpu().numpy()
    draw = ImageDraw.Draw(input_image)

    # Assume category names are the same as the original
    COCO_INSTANCE_CATEGORY_NAMES = [
        "__background__", "person", "bicycle", "car", "motorcycle", "airplane", "bus",
        "train", "truck", "boat", "traffic light", "fire hydrant", "stop sign",
        "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow",
        "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella", "handbag", "tie",
        "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
        "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass",
        "cup", "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange",
        "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair", "couch",
        "potted plant", "bed", "dining table", "toilet", "TV", "laptop", "mouse", "remote",
        "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
        "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"
    ]

    draw = ImageDraw.Draw(input_image)
    font = ImageFont.load_default()

    for box, label, score in zip(boxes, labels, scores):
        if score > 0.5:  # You can set your own threshold
            try:
                x1, y1, x2, y2 = box
                draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

                # Ensure the text position is within the image boundary
                text_y_position = max(0, y1 - 12)
                txt = f"{COCO_INSTANCE_CATEGORY_NAMES[label]}: {score:.2f}"
                draw.text((x1+4, text_y_position+4), txt, fill="red", font=font)
            except IndexError:
                print(f"Label out of range: {label}")
            
    input_image.save(save_path)
    print(f"Saved object detected image at {save_path}")