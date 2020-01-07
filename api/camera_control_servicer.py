import logging
import threading
import cv2
import generated.camera_control_pb2_grpc

from generated.camera_control_pb2 import SetCameraRotationResponse, GetFrameResponse
from hardware.controller import Controller
from utils.servo import angle_to_pwm, clip_horizontal_angle, clip_vertical_angle

logger = logging.getLogger(__name__)


class CameraControlServicer(generated.camera_control_pb2_grpc.CameraControlServicer):

    class Camera(threading.Thread):

        def __init__(self, device):
            threading.Thread.__init__(self)

            self.daemon = True
            self.camera = cv2.VideoCapture(device)
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 352)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 288)
            self.frame = None
            self.lock = threading.Lock()

        def run(self):
            ret = True

            while ret is True:
                ret, frame = self.camera.read()

                self.lock.acquire()
                self.frame = frame
                self.lock.release()

        def get_frame(self):
            self.lock.acquire()
            frame = self.frame.copy()
            self.lock.release()
            return frame

    def __init__(self, controller):
        self.controller = controller
        self.camera = CameraControlServicer.Camera(0)
        self.camera.start()

    def SetRotation(self, request, context):
        logger.info('Set camera rotation to horizontal angle {} and vertical angle {}'.format(request.horizontal,
                                                                                              request.vertical))

        horizontal_angle = clip_horizontal_angle(request.horizontal)
        logger.debug('Clipped horizontal angle is {}'.format(horizontal_angle))

        vertical_angle = clip_vertical_angle(request.vertical)
        logger.debug('Clipped vertical angle is {}'.format(vertical_angle))

        self.controller.write(Controller.CMD_SERVO2, angle_to_pwm(horizontal_angle))
        self.controller.write(Controller.CMD_SERVO3, angle_to_pwm(vertical_angle))
        return SetCameraRotationResponse()

    def GetFrame(self, request, context):
        logger.info('Get frame')

        ret, frame = cv2.imencode('.jpg', self.camera.get_frame())
        return GetFrameResponse(frame=frame.tobytes())
