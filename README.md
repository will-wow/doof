# Doof

Eventually the brains for a little robot friend

## Development

```bash
cd doof
./bin/doof
```

## Run on boot

```bash
sudo ln -s $HOME/repos/doof/doof.service /lib/systemd/system/doof.service
sudo systemctl daemon-reload
sudo systemctl enable doof.service
```

### Stop (for development)

```bash
sudo systemctl stop doof.service
```

### Restart

```bash
sudo systemctl restart doof.service
```

### Check Service Status

```bash
sudo systemctl status doof.service
```


## Useful Tutorials & Links

- [Movement Detection](https://www.pyimagesearch.com/2019/09/02/opencv-stream-video-to-web-browser-html-page/)
- [Face Detection](https://realpython.com/face-recognition-with-python/)
- [OpenCV Face Detection](
- [Face Detection](https://realpython.com/face-recognition-with-python/)
)
- [OpenCV Cascades](https://docs.opencv.org/3.4/db/d28/tutorial_cascade_classifier.html)

