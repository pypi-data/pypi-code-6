import os
import wtforms
from cgi import FieldStorage
from wtforms.validators import *
from wtforms.validators import StopValidation, ValidationError

__all__ = wtforms.validators.__all__ + ('StopValidation', 'ValidationError', 'FileRequired', 'FileAllowed')

class FileRequired(InputRequired):
    '''
    Check if the field is valid file entity. This class could be used for single file / multi files field.
    '''

    def _check_fieldstorage(self, data):
        '''
        :param data: Could be instance of cgi.FieldStorage, or a list which contains instances of cgi.FieldStorage.
        '''
        if isinstance(data, list) and len(data) > 0:
            for each_data in data:
                if not isinstance(each_data, FieldStorage):
                    return False
            return True
        elif isinstance(data, FieldStorage):
            return True
        return False

    def __call__(self, form, field):
        if not self._check_fieldstorage(field.data):
            if self.message is None:
                message = field.gettext('This field is required for file(s).')
            else:
                message = self.message

            field.errors[:] = []
            raise StopValidation(message)

class FileAllowed:
    '''
    Check if the uploaded file(s) are valid mimetype(s).
    '''

    def __init__(self, allowed_types, message=None):
        '''
        :param allowed_types: A list/tuple of extension names, ex. ['jpg', 'png']
        '''
        self.allowed_types = [each_type.lower() for each_type in allowed_types]
        if message is None:
            self.message = 'Only these types are allowed: ' + ', '.join(allowed_types)
        else:
            self.message = message

    def _check_allowed_types(self, data):
        '''
        :param data: Could be instance of cgi.FieldStorage, or a list which contains instances of cgi.FieldStorage.
        '''
        pass_flag = True
        if isinstance(data, list):
            for each_data in data:
                if each_data.filename.split('.')[-1].lower() not in self.allowed_types:
                    pass_flag = False
                    break
        elif isinstance(data, FieldStorage):
            if data.filename.split('.')[-1].lower() not in self.allowed_types:
                pass_flag = False
        else:
            pass_flag = False
        return pass_flag

    def __call__(self, form, field):
        if not self._check_allowed_types(field.data):
            raise ValidationError(self.message)

class FileSize:
    '''
    Check if the all size of uploaded file(s) are valid
    '''

    def __init__(self, min=0, max=None, base='B', message=None):
        '''
        :param min: lower limit of file size
        :param max: upper limit of file size, None means no limit
        :param base: valid base are: b(bytes), kb, mb, gb
        :param message: The error message
        '''
        if message is None:
            msg = ['File size limited']
            msg.append('minimum size is {}'.format(min))
            if max is not None: msg.append('maximum size is {}'.format(max))
            self.message = ', '.join(msg) + '.'
        else:
            self.message = message
        
        self.min  = min
        self.max  = max
        self.base = base.lower()
        if self.base == 'b':
            self.min_size = min
            self.max_size = None if max is None else max
        elif self.base == 'kb':
            self.min_size = min * 1024
            self.max_size = None if max is None else max * 1024
        elif self.base == 'mb':
            self.min_size = min * 1024**2
            self.max_size = None if max is None else max * 1024**2
        elif self.base == 'gb':
            self.min_size = min * 1024**3
            self.max_size = None if max is None else max * 1024**3
        else:
            raise ValueError('base should be either b, kb, mb, or gb.')

    def _is_out_of_limit(self, file):
        import os
        current_pos = file.tell()
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(current_pos, os.SEEK_SET)
        if self.min_size > file_size:
            return True
        if self.max_size is not None:
            if self.max_size < file_size:
                return True
        return False

    def _check_file_size(self, data):
        '''
        :param data: Could be instance of cgi.FieldStorage, or a list which contains instances of cgi.FieldStorage.
        '''
        pass_flag = True
        if isinstance(data, list):
            for each_data in data:
                if self._is_out_of_limit(each_data.file):
                    pass_flag = False
                    break
        elif isinstance(data, FieldStorage):
            if self._is_out_of_limit(data.file):
                pass_flag = False
        else:
            pass_flag = False
        return pass_flag

    def __call__(self, form, field):
        if not self._check_file_size(field.data):
            raise ValidationError(self.message)

class FileQuantity:
    '''
    Check if quantities of uploaded file(s) are allowed
    '''

    def __init__(self, min, max, message=None):
        '''
        :param min: lower limit of files quantities
        :param max: upper limit of files quantities
        :param message: The error message
        '''
        if message is None:
            self.message = 'File quantity limited: minimum is {}, maximum is {}.'.format(min, max)
        else:
            self.message = message
        
        self.min  = min
        self.max  = max

    def _check_file_quantity(self, data):
        '''
        :param data: Could be instance of cgi.FieldStorage, or a list which contains instances of cgi.FieldStorage.
        '''
        pass_flag = True
        if isinstance(data, list):
            file_quantity = len(data)
            if self.min > file_quantity or self.max < file_quantity:
                pass_flag = False
        else:
            raise ValueError('FileQuantity should be used against multi files upload')
        return pass_flag

    def __call__(self, form, field):
        if not self._check_file_quantity(field.data):
            raise ValidationError(self.message)

