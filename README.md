# 3D_Drone_Based_Mapping_Backend




# Setup steps



## 1. Add Conda to the PATH Variable (if it isn't already)

### 1. Open Environment Variables

    1. Press Win + S, type "Environment Variables", and open "Edit the system environment variables"
    2. In the System Properties window, click "Environment Variables..."
    3. Under User variables, find and select the variable named **Path**, then click edit

### 2. Add the Required Conda Paths


Click New and add each of these:

    C:\Users\yourname\anaconda3
    C:\Users\yourname\anaconda3\Scripts
    C:\Users\yourname\anaconda3\Library\bin

### 3. Apply and Restart


Once added, click ok and close all dialogs. Then restart VS Code.
To test, run `conda --version` in the VS Code Terminal




## 2. Create and activate a Conda Environment


Run `conda create --name crash3d python=3.10` in your VS Code Terminal.
After the environent is created, you need to activate it by running `conda activate crash3d`




## 3. Install Required Dependencies


Run `pip install -r requirements.txt` to install the required modules




# Folder Structure


- /data                          
    - /processed<======= 3D models after processing has been done
    - /raw<============= 3D models before any processing   
    - /renders<========= 2D images generated from sides of vehicles
    - /reports<========= Output PDF's will be stored here
- /notebooks<=========== Jupyter notebooks
- /source<============== Python scripts   