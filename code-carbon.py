import argparse
import torch
import torchvision.transforms as transforms
from torchvision import models
from PIL import Image, ImageDraw, ImageFont
from codecarbon import EmissionsTracker

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
    fontsize = 1  # starting font size
    # TODO where is font stored?
    font = ImageFont.truetype(font ="",size = fontsize)

    for box, label, score in zip(boxes, labels, scores):
        if score > 0.5:  # You can set your own threshold
            x1, y1, x2, y2 = box
            draw.rectangle([x1, y1, x2, y2], outline="red", width=3)

            # Ensure the text position is within the image boundary
            text_y_position = max(0, y1 - 12)
            txt = f"{COCO_INSTANCE_CATEGORY_NAMES[label]}: {score:.2f}"

            # portion of image width you want text width to be
            img_fraction = 0.50

            font = ImageFont.truetype("arial.ttf", fontsize)
            while font.getsize(txt)[0] < img_fraction*input_image.size[0]:
                # iterate until the text size is just larger than the criteria
                fontsize += 1
                font = ImageFont.truetype("arial.ttf", fontsize)
            
            draw.text((x1+4, text_y_position+4), txt, fill="red", font=font, size=fontsize)

    input_image.save(save_path)
    print(f"Saved object detected image at {save_path}")


if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Object Detection")
    parser.add_argument("--image", type=str, help="Path to the image for object detection")
    args = parser.parse_args()

    # Initialize CodeCarbon's EmissionsTracker
    tracker = EmissionsTracker()
    tracker.start()

    # Perform object detection and save image with bounding boxes
    object_detection(args.image)

    # Stop the tracker and display the emissions
    tracker.stop()

    # For this specific version of CodeCarbon, the emissions data might be saved in a file.
    # Check the directory for a CSV or JSON file that contains the emissions data.
