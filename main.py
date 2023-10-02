import argparse
from experiment_impact_tracker.compute_tracker import ImpactTracker    
from codecarbon import EmissionsTracker
from object_detector import object_detection
from carbontracker.tracker import CarbonTracker

if __name__ == "__main__":
    # Argument parsing
    parser = argparse.ArgumentParser(description="Object Detection")
    parser.add_argument("--image", type=str, help="Path to the image for object detection")
    parser.add_argument("--tracker", type=str, help="Type of tracker to use")
    args = parser.parse_args()

    # This one isn't working
    if args.tracker == "experiment-tracker":
        tracker = ImpactTracker("logs")
        tracker.launch_impact_monitor()
        info = tracker.get_latest_info_and_check_for_errors()
        print("Tracker Info:", info)
        object_detection(args.image)
    # This one is working
    elif args.tracker == "code-carbon":
        tracker = EmissionsTracker()
        tracker.start()
        object_detection(args.image)
        tracker.stop()
    # This one is mainly used for training
    elif args.tracker == "carbon-tracker":
        tracker = CarbonTracker(epochs=2)
        object_detection(args.image)
        tracker.stop()
    else:
        raise ValueError("Invalid tracker name")
    


