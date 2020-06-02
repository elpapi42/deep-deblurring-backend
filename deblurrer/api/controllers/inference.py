#!/usr/bin/python
# coding=utf-8

"""Logic for inference controller."""

from requests.exceptions import ConnectionError
import requests
import base64
import imghdr
import uuid
import io

from flask import make_response, request, jsonify
from flask import current_app as app
from flask_restful import Resource, abort
from cloudinary import uploader
from PIL import Image, UnidentifiedImageError

from deblurrer.api.models import Example
from deblurrer import db, limiter


class InferenceController(Resource):
    """Call the serving API for inference over the supplied image."""

    decorators = [limiter.limit('5/minute;1/second', methods=['POST'])]

    def post(self):
        """
        Send image to inference API.

        Returns:
            json response with the result of inference
        """
        input_image = self.validate_image(request.files.get('image'))

        # Limits files size to 1024 and stores original size
        # For upsample the resulting image later
        original_size = input_image.size
        original_format = input_image.format
        input_image.thumbnail([1024, 1024])

        # Get bytes from resized and validated image
        input_bytes = io.BytesIO()
        input_image.save(input_bytes, input_image.format)
        input_bytes = input_bytes.getvalue()

        # Sends image to inference engine for processing
        output_bytes = self.predict_image(input_bytes)

        # Converts Bytes to PIL Image and resize to original size
        output_bytes = io.BytesIO(output_bytes)
        output_image = Image.open(output_bytes)
        output_image = output_image.resize(original_size)

        # Write the PIL image to bytes again
        output_bytes = io.BytesIO()
        output_image.save(output_bytes, input_image.format)
        output_bytes = output_bytes.getvalue()

        # Upload the images to cloudinary
        rid, input_url, output_url = self.upload_to_cloudinary(
            input_bytes,
            output_bytes,
        )

        # Create and commit new example to the database
        example = Example(rid, input_url, output_url)
        db.session.add(example)
        db.session.commit()

        return make_response(
            jsonify({
                'input_image': input_url,
                'output_image': output_url,
                'resource_id': str(rid),
            }),
            200,
        )

    def validate_image(self, image_file):
        """
        Verify the input file is a valid image.

        Abort the request in case the file cant be verified

        Args:
            image_file (FileIO): file to validate

        Returns:
            validated pillow image
        """
        # Check if the image was not supplied
        if (image_file is None):
            abort(
                400,
                message='Image was not supplied',
            )

        try:
            image_pil = Image.open(image_file)
        except UnidentifiedImageError:
            abort(
                400,
                message='Invalid file',
            )

        if (not image_pil.format in {'PNG', 'JPG', 'JPEG'}):
            abort(
                400,
                message='Invalid file',
            )
        
        max_res = app.config.get('MAX_IMAGE_RESOLUTION')
        if (image_pil.width > max_res or image_pil.height > max_res):
            abort(
                400,
                message='Image resolution too big',
            )

        return image_pil

    def predict_image(self, image):
        """
        Send image to deblurring inference engine.

        Args:
            image (bytes): Image to deblur

        Returns
            Deblurred image bytes
        """
        # Encode the image bytes as b64 string
        image = str(base64.b64encode(image), encoding='utf-8')

        try:
            # Request predictions to inference engine
            preds = requests.post(
                url=app.config['SERVING_URL'],
                json={'instances': [
                    [{'b64': r'{string}'.format(string=image)}],
                ]},
            ).json()
        except ConnectionError:
            abort(
                500,
                message='Inference engine unavailable'
            )

        # Validates inference engine reponse
        if (preds.get('error') is not None):
            abort(
                500,
                message='Inference engine error',
            )
        # Inference engine returns URL Safe B64 Encoding
        # decodes Base64URL to Bytes
        image = preds['predictions'][0]
        image = base64.urlsafe_b64decode(image)

        return image

    def upload_to_cloudinary(self, input_image, output_image):
        """
        Upload to images to cloudinary static host provider.

        Args:
            input_image (bytes): Image received as request input
            output_image (bytes): Output of the inferece engine
        
        Returns:
            uuid and URL of the uploaded files
        """
        # Identifier for the images
        resource_id = uuid.uuid4()

        # Upload the input image
        input_resp = uploader.upload(
            bytearray(input_image),
            public_id=str(resource_id),
            folder='/input',
        )

        # Upload the generated image
        output_resp = uploader.upload(
            bytearray(output_image),
            public_id=str(resource_id),
            folder='/generated',
        )

        return (
            resource_id,
            input_resp.get('secure_url'),
            output_resp.get('secure_url'),
        )