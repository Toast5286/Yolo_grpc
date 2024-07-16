import concurrent.futures as futures
import grpc
import grpc_reflection.v1alpha.reflection as grpc_reflection
import logging
import generic_box_pb2
import generic_box_pb2_grpc
import utils

from ultralytics import YOLO

class ServiceImpl(generic_box_pb2_grpc.GenericBoxServiceServicer):

    def __init__(self, calling_function):
        """
        Args:
            calling_function: the function that should be called
                              when a new request is received

                              the signature of the function should be:

                              (image: bytes) -> bytes

                              as described in the process method

        """
        self.__calling_fn = calling_function
        self.__model = YOLO("yolov8n.pt")

    def process(self, request: generic_box_pb2.Data, context):
        """Processes a given ImageWithPoses request

        It expects that a process function was already registered
        with the following signature

        (image: bytes) -> bytes

        Image is the bytes of the image to process.

        Args:
            request: The ImageWithPoses request to process
            context: Context of the gRPC call

        Returns:
            The Image with the applied function

        """
        image = request.file
        model = self.__model
        return self.__calling_fn(image,model)

def grpc_server():
    logging.basicConfig(
        format='[ %(levelname)s ] %(asctime)s (%(module)s) %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.INFO)

    calling_fn = utils.get_calling_function()
    if not calling_fn:
        exit(1)

    server = grpc.server(futures.ThreadPoolExecutor())
    generic_box_pb2_grpc.add_GenericBoxServiceServicer_to_server(
        ServiceImpl(calling_fn),
        server)

    # Add reflection
    service_names = (
        generic_box_pb2.DESCRIPTOR.services_by_name['GenericBoxService'].full_name,
        grpc_reflection.SERVICE_NAME
    )
    grpc_reflection.enable_server_reflection(service_names, server)

    utils.run_server(server)
        

if __name__ == '__main__':
    grpc_server()
