import os
from config import Config
from flask import flash
from typing import Type
from werkzeug.utils import secure_filename


class Uploader(object):

    _config: Config

    def __init__(self, config: Type[Config]=None):

        self._config = config

    def upload_file(self, req, sub_folder: str=None, renamed: str=None, test: bool=False, file=None) -> str:
        if req.method == 'POST' or test is True:
            # check if the post request has the file part
            if 'file' not in req.files and not test:
                # TODO: probably raise an exception instead of redirect
                # TODO: possibly no flash message ??? maybe flash message ???
                flash('No file part')
                raise MissingFileException

            if file:
                file = file
            else:
                file = req.files['file']
            # if user does not select file, browser also
            # submit an empty part without filename
            if file.filename == '':
                # TODO: probably raise an exception instead of redirect
                # TODO: possibly no flash message ??? ??? maybe flash message ???
                flash('No selected file')
                raise MissingFileException

            print(file)

            if file and self._allowed_file(file.filename):
                f_name = str(file.filename)
                ext = f_name.rsplit('.', 1)[1].lower()

                if renamed:
                    file.filename = renamed + "." + ext

                filename = secure_filename(file.filename)

                path = self._config.UPLOAD_FOLDER
                if sub_folder:
                    path = os.path.join(path, sub_folder)
                file.save(os.path.join(path, filename))

                return filename
                # TODO: probably don't redirect
                # TODO: possibly no flash message ??? maybe flash message ???
                # return redirect(url_for('uploaded_file',
                #                         filename=filename))

    def _allowed_file(self, filename: str):
        if '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self._config.ALLOWED_EXTENSIONS:
            return True
        else:
            raise WrongFileTypeException


class UploaderException(Exception):
    """Raise for generic File Uploader Exception"""


class WrongFileTypeException(UploaderException, TypeError):
    """Raise for Wrong File Type Exception"""


class MissingFileException(UploaderException, FileNotFoundError):
    """Raise for Missing File Exception"""
