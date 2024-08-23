# FallPrediction## Environment Setup
Step 1: Download and install Miniconda from https://docs.conda.io/projects/miniconda/en/latest/.

Step 2: Create conda environment and install required packages.
```
conda create --name auto_va python=3.8
conda activate auto_va
pip install cython
pip install -r requirements.txt
```
Step 3 (optional): Install JavaScript packages.

*required for building JavaScript module
```
cd js_module
npm install @ricky0123/vad-web@0.0.12
npm install --save-dev webpack
sh copy.sh
```
Step 4: Download MediaPipe model bundle.
- Create a folder named `model` outside of the `Auto_VA` folder.
- Create a subfolder named `mediapipe` inside the newly created `model` folder.
- Download the face landmarker model bundle from https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task.
- Put the downloaded model (`face_landmarker.task`) into `model/mediapipe`.

Step 5: Setup Android debug bridge
- Download Android SDK Platform-Tools from https://developer.android.com/tools/releases/platform-tools.
- Edit system environment variables to add the `platform_tools` folder to the `PATH` variable.
- On the Android tablet, activate developer mode and enable the USB debugging option.

## Building JavaScript module (optional)
*required only when `js_module/src/index.js` is modified 
```
sh js_module/build.sh
```

## Building executables
```
sh build.sh
```

## Running the Python scripts
### Scenario 1: Running the full test
Step 0: Prepare the following devices: 
 - Android Tablet
 - IC/barcode scanner
 - External display monitor
 - External microphone
 - Webcam with zoom, tilt, and pan support

Step 1: Connect the Android tablet to the main computer via USB.

Step 2: Enable developer mode and USB debugging on the Android tablet.

Step 3: In command prompt, run `adb reverse tcp:5001 tcp:5001`.

Step 4: In command prompt, start the servers with `python main.py --test_all`.

Step 5: On the Android tablet, navigate to `127.0.0.1:5001/touch/index` with a web browser.

### Scenario 2: Running a quick test on a single laptop/computer
Step 1: In command prompt, start the servers with `python main.py --debug`.

Step 2: Open an incognito/private tab in the browser, then navigate to `127.0.0.1:5001/touch/index`, adjust the zoom level if needed.

Step 3: Bypass pose detection by pressing the Enter key.

### Scenario 3: Running the pose estimation module as a standalone application
Step 1: In command prompt, start the server with `python fl_server.py --debug –standalone`.

### **Additional notes
 - The working directory is always at the level of the `Auto_VA` folder.
 - Every time a new command prompt/terminal is opened, the conda environment (`auto_va`) must be activated before running any script.
 - Internet connection is required for the first launch of `main.py` to initiate the automated download of the speech recognition model.
 - During IC scanning, the mouse cursor must be focused on the VA display (by clicking on the browser window).
