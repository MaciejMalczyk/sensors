import os

def get_max_res(device):
    resolutions = []

    command = f"v4l2-ctl --device={device} --list-formats-ext | grep Size | sed 's/^.................//'"

    res = os.popen(command).read().splitlines()

    for n in res:
        v = n.split('x')
        resolutions.append([int(v[0]),int(v[1])])

    return max(resolutions)
