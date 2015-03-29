
poppy_config={}

poppy_config['controllers'] = {}

poppy_config['controllers']['upper_body_controller'] = {
    "port": "TODO: Set the good port name",
    "sync_read": False,
    "attached_motors": ["head"],
}

poppy_config['motorgroups'] = {
    "head": ["head_z", "head_y"],
}

poppy_config['motors'] = {
    "head_y": {
      "id": 37,
      "type": "AX-12",
      "orientation": "indirect",
      "offset": 10.0,
      "angle_limit": [-40, 8 ],
    },
    "head_z": {
      "id": 36,
      "type": "AX-18",
      "orientation": "direct",
      "offset": 0.0,
      "angle_limit": [-100, 100 ],
    },
}

if __name__ == '__main__':
    '''
    You can easily generate the configuration file for your Poppy by specifying the 2 serial ports of the USB2AX dongles.
    Then execute this script. It will produce the poppy_config file needed to create the robot using this command:

    import json
    import pypot.robot
    poppy_config = json.load(path/poppy_config.json)
    poppy = pypot.robot.from_config(poppy_config)

    '''
    import json
    poppy_config['controllers']['upper_body_controller']['port'] = 'auto'

    with open('poppy_config.json','w') as f:
        json.dump(poppy_config, f, indent=2)
