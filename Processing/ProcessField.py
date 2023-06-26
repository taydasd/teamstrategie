class ProcessField:
    def __init__(self, camera_field_size, controller):
        self.controller_maxima = controller.get_maxima()
        self.camera_field_size = camera_field_size

    def get_real_pos(self, x_cam, y_cam):
        return {0, 0}  # not implemented yet
