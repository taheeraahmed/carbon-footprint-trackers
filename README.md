# carbon-footprint-trackers

As an example project there is a Faster RCNN pretrained model which does an object detection task on an image of your own choice. It needs to be stored on your computer somewhere. 
## code-carbon.py 
Uses the code carbon tracker which is available as a python package and easily used. 
To run the script do as follows:

```bash
python code-carbon.py --image <path-to-image> --tracker "code-carbon"
```

This will also generate a file called "emissions.csv" which contains the carbon footprint of the code. There will also be stored an image which shows the objects detected in the image you have chosen.

## experiment-impact-tracker.py
Uses the experiment impact tracker which is available as a python package and easily used.
To run the script do as follows:

```bash
python experiment-impact-tracker.py --image <path-to-image> --tracker "experiment-impact"
```
