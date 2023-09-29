import argparse
from experiment_impact_tracker.compute_tracker import ImpactTracker    
from codecarbon import EmissionsTracker
from object_detector import object_detection

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Object Detection")
    parser.add_argument("--image", type=str, help="Path to the image for object detection")
    parser.add_argument("--tracker", type=str, help="Type of tracker to use")
    args = parser.parse_args()

    if args.tracker == "experiment-tracker":
        # Initialize Experiment Impact Tracker
        tracker = ImpactTracker(logdir="logs")
        # Perform object detection and save image with bounding boxes
        object_detection(args.image)
        # Stop the tracker and display the impact
        tracker.launch_impact_monitor()
    elif args.tracker == "code-carbon":
        # Initialize CodeCarbon's EmissionsTracker
        tracker = EmissionsTracker()
        tracker.start()
        # Perform object detection and save image with bounding boxes
        object_detection(args.image)
        # Stop the tracker and display the emissions
        tracker.stop()
    else:
        raise ValueError("Invalid tracker name")
    


