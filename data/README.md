The file in the root directory, `image-sizes-origin_dataset.csv`, simply lists the original size of each image before downscaling.

Each folder represents the data for different final image sizes. Inside each folder, there is a csv for each of the downscaling methods.

The format of the CSVs is the following
```
'image_name','total_time','downscale_time','request_time','model_time','accuracy','size'
```

`total_time` = Turnaround time for the whole system

`downscale_time` = downscale image time

`request_time` = Time for server to process a request

`model_time` = time for server to run object detection model

`accuracy` = accuracy of prediction. Returned by Yolo when it identifies a cup

`size` = size of image in bytes

