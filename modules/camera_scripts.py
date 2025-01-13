import subprocess

def get_camera_devices():
    cameras = []

    list_v4l2_devices = f"ls /dev/video*"

    list_proc = subprocess.Popen(list_v4l2_devices, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    list_res, list_err = list_proc.communicate()

    v4l2_dev_list = list_res.decode("utf-8").splitlines()

    for dev in v4l2_dev_list:
        get_v4l2_device_caps = f"v4l2-ctl --device={dev} --all | grep Caps"
        cap_proc = subprocess.Popen(get_v4l2_device_caps, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        cap_res, cap_err = cap_proc.communicate()
        cap_data = cap_res.decode("utf-8")[-11:]

        if cap_err:
            print(f"Camera_scripts: Error: {cap_err.decode('utf-8')}")

        if cap_data == "0x04200001\n":
            cameras.append(dev) #Camera
        elif cap_data == "0x04a00000\n":
            continue #Meta
        elif cap_data == "0x04208000\n":
            continue #Cedrus
        else:
            print(f"Unknown: {cap_data}")

    return cameras

def get_max_res(device):
    resolutions = []

    command = f"v4l2-ctl --device={device} --list-formats-ext | grep Size | sed 's/^.................//'"

    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    proc_res, proc_err = proc.communicate()

    res = proc_res.decode("utf-8").splitlines()

    for n in res:
        v = n.split('x')
        resolutions.append([int(v[0]),int(v[1])])

    return max(resolutions)
