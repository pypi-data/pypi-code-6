from dm.view.manipulator import BaseManipulator
from dm.view.manipulator import DomainObjectManipulator
from dm.view.manipulator import HasManyManipulator
import dm.webkit as webkit
from dm.ioc import *
from quant.exceptions import KforgeCommandError
import re
import quant.regexps
import quant.command

if webkit.webkitName == 'django' and webkit.webkitVersion == '1.0':

    class PasswordField(webkit.fields.RegexField):

        widget = webkit.fields.PasswordInput

        def __init__(self, *args, **kwargs):
            kwargs['regex'] = '^\S{4,}$' 
            kwargs['min_length'] = 4 
            super(PasswordField, self).__init__(*args, **kwargs)
 

    class PasswordConfirmationField(webkit.fields.Field):

        widget = webkit.fields.PasswordInput

        def __init__(self, *args, **kwargs):
            super(PasswordConfirmationField, self).__init__(*args, **kwargs)
 

    class PersonNameField(webkit.fields.RegexField):

        def __init__(self, *args, **kwargs):
            regex = '^(?!%s)%s$' % (quant.regexps.reservedPersonName, quant.regexps.personName)
            kwargs['required'] = True
            kwargs['regex'] = regex 
            kwargs['min_length'] = 2
            kwargs['max_length'] = 20
            super(PersonNameField, self).__init__(*args, **kwargs)

        def clean(self, value):
            super(PersonNameField, self).clean(value)
            # Check name is available.
            command = quant.command.AllPersonRead(value)
            try:
                command.execute()
            except KforgeCommandError:
                pass
            else:
                message = "Login name is already being used by another person."
                raise webkit.ValidationError(message)
            return value

    class SshKeyStringField(webkit.fields.RegexField):

        def __init__(self, *args, **kwargs):
            regex = '^%s$' % (quant.regexps.sshKeyString)
            kwargs['required'] = True
            kwargs['regex'] = regex 
            kwargs['widget'] = webkit.widgets.Textarea
            super(SshKeyStringField, self).__init__(*args, **kwargs)

        def clean(self, value):
            super(SshKeyStringField, self).clean(value)
            # Check key string is available.
            value = value.strip()
            publicKey = value.split(' ')[1]
            if quant.command.Command.registry.sshKeys.search(publicKey):
                message = "Key has already been registered on this site."
                raise webkit.ValidationError(message)
            # Check key decodes from base64.
            try:
                publicKey.decode('base64')
            except:
                message = "Key does not appear to be encoded with base64."
                raise webkit.ValidationError(message)
            return value

    class ProjectNameField(webkit.fields.RegexField):
        
        def __init__(self, *args, **kwargs):
            regex = '^(?!%s)%s$' % (quant.regexps.reservedProjectName, quant.regexps.projectName)
            kwargs['required'] = True
            kwargs['regex'] = regex 
            kwargs['min_length'] = 3
            kwargs['max_length'] = 15
            super(ProjectNameField, self).__init__(*args, **kwargs)

        def clean(self, value):
            super(ProjectNameField, self).clean(value)
            # Check name is available.
            command = quant.command.AllProjectRead(value)
            try:
                command.execute()
            except KforgeCommandError:
                pass
            else:
                message = "Project name is already being used by another project."
                raise webkit.ValidationError(message)
            return value


    class ServiceNameField(webkit.fields.RegexField):
        
        def __init__(self, *args, **kwargs):
            regex = '^%s$' % (quant.regexps.serviceName)
            kwargs['required'] = True
            kwargs['regex'] = regex 
            kwargs['min_length'] = 1
            kwargs['max_length'] = 16
            super(ServiceNameField, self).__init__(*args, **kwargs)


class PersonManipulator(DomainObjectManipulator):

    def isPersonName(self, field_data, all_data):
        pattern = re.compile('^%s$' % quant.regexps.personName)
        if not pattern.match(field_data):
            msg = "This field can only contain alphanumerics, "
            msg += "underscores, hyphens, and dots."
            raise webkit.ValidationError(msg)

    def isReservedPersonName(self, field_data, all_data):
        pattern = re.compile('^%s$' % quant.regexps.reservedPersonName)
        if pattern.match(field_data):
            msg = "This field is reserved and can not be registered."
            raise webkit.ValidationError(msg)

    def isAvailablePersonName(self, field_data, all_data):
        command = quant.command.AllPersonRead(field_data)
        try:
            command.execute()
        except KforgeCommandError:
            pass
        else:
            message = "Login name is already being used by another person."
            raise webkit.ValidationError(message)

    def isMatchingPassword(self, field_data, all_data):
        password = all_data['password']
        passwordconfirmation = all_data['passwordconfirmation']
        if not (password == passwordconfirmation):
            raise webkit.ValidationError("Passwords do not match.")

    def isMatchingEmail(self, field_data, all_data):
        email = all_data['email']
        emailconfirmation = all_data['emailconfirmation']
        if not (email == emailconfirmation):
            raise webkit.ValidationError("Emails do not match.")

    def isCaptchaCorrect(self, field_data, all_data):
        if self.dictionary['captcha.enable']:
            word = all_data['captcha']
            hash = all_data['captchahash']
            if not word and not hash:
                raise webkit.ValidationError("Captcha failure.")
            read = quant.command.CaptchaRead(hash)
            try:
                read.execute()
            except KforgeCommandError, inst: 
                raise webkit.ValidationError("Captcha failure.")
            captcha = read.object
            if not captcha.checkWord(word):
                raise webkit.ValidationError("Captcha failure.")

    def clean(self):
        if 'passwordconfirmation' in self.cleaned_data and 'password' in self.cleaned_data \
        and self.cleaned_data['passwordconfirmation'] != self.cleaned_data['password']:
            if 'passwordconfirmation' in self._errors:
                self._errors['passwordconfirmation'].append("Passwords do not match.")
            else:
                self._errors['passwordconfirmation'] = webkit.fields.ErrorList(["Passwords do not match."])
        if 'emailconfirmation' in self.cleaned_data and 'email' in self.cleaned_data \
        and self.cleaned_data['emailconfirmation'] != self.cleaned_data['email']:
            if 'emailconfirmation' in self._errors:
                self._errors['emailconfirmation'].append("Emails do not match.")
            else:
                self._errors['emailconfirmation'] = webkit.fields.ErrorList(["Emails do not match."])
        if self._errors:
            delattr(self, 'cleaned_data')
        else:
            return self.cleaned_data


class PersonCreateManipulator(PersonManipulator):

    def buildFields(self):
        if webkit.webkitName == 'django' and webkit.webkitVersion == '1.0':
            self.fields = webkit.SortedDict([
                ('name', PersonNameField()),
                ('password', PasswordField()),
                ('passwordconfirmation', PasswordConfirmationField()), 
                ('fullname', webkit.Field(required=True)),
                ('email', webkit.EmailField(required=True)),
                ('emailconfirmation', webkit.Field(required=True)),
            ])
            # Todo: Fixup captcha.
        elif webkit.webkitName == 'django' and webkit.webkitVersion == '0.96':
            self.fields.append(
                webkit.TextField(
                    field_name="name", 
                    is_required=True, 
                    validator_list=[
                        self.isPersonName, 
                        self.isReservedPersonName, 
                        self.isAvailablePersonName, 
                        self.isTwoCharsMin,
                        self.isTwentyCharsMax,
                    ]
                )
            )
            self.fields.append(
                webkit.PasswordField(
                    field_name="password", 
                    is_required=True, 
                    validator_list=[
                        self.isFourCharsMin,
                    ]
                )
            )
            self.fields.append(
                webkit.PasswordField(
                    field_name="passwordconfirmation", 
                    is_required=True, 
                    validator_list=[
                        self.isMatchingPassword
                    ]
                )
            )
            self.fields.append(
                webkit.TextField(
                    field_name="fullname", 
                    is_required=True
                )
            )
            self.fields.append(
                webkit.EmailField(
                    field_name="email", 
                    is_required=True
                )
            )
            self.fields.append(
                webkit.EmailField(
                    field_name="emailconfirmation", 
                    is_required=True, 
                    validator_list=[
                        self.isMatchingEmail
                    ]
                ) 
            )
            if self.dictionary['captcha.enable']:
                self.fields.append(
                    webkit.TextField(
                        field_name="captcha", 
                        is_required=isCaptchaEnabled, 
                        validator_list=[
                            self.isCaptchaCorrect
                        ]
                    ) 
                )
                self.fields.append(
                    webkit.HiddenField(
                        field_name="captchahash", 
                        is_required=False,
                    )   
                )

class PersonUpdateManipulator(PersonManipulator):

    def buildFields(self):
        if webkit.webkitName == 'django' and webkit.webkitVersion == '1.0':
            self.fields = webkit.SortedDict([
                ('password', PasswordField(required=False)),
                ('passwordconfirmation', PasswordField(required=False)),
                ('fullname', webkit.Field(required=True)),
                ('email', webkit.EmailField(required=True)),
            ])
        elif webkit.webkitName == 'django' and webkit.webkitVersion == '0.96':
            self.fields.append(
                webkit.PasswordField(
                    field_name="password", 
                    is_required=False, 
                    validator_list=[
                        self.isFourCharsMin,
                    ]
                )
            )
            self.fields.append(
                webkit.PasswordField(
                    field_name="passwordconfirmation", 
                    is_required=False, 
                    validator_list=[
                        self.isMatchingPassword
                    ]
                )
            )
            self.fields.append(
                webkit.TextField(
                    field_name="fullname", 
                    is_required=True
                )
            )
            self.fields.append(
                webkit.EmailField(
                    field_name="email", 
                    is_required=True
                )
            )


