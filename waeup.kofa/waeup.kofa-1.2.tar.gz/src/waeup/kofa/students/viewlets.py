3## $Id: viewlets.py 11612 2014-04-30 14:36:28Z henrik $
##
## Copyright (C) 2011 Uli Fouquet & Henrik Bettermann
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##
import os
import grok
from zope.component import getUtility
from zope.interface import Interface
from zope.i18n import translate
from waeup.kofa.interfaces import (
    IKofaObject, IExtFileStore, IFileStoreNameChooser)
from waeup.kofa.interfaces import MessageFactory as _
from waeup.kofa.utils.helpers import string_from_bytes, file_size
from waeup.kofa.browser import DEFAULT_IMAGE_PATH
from waeup.kofa.browser.viewlets import (
    PrimaryNavTab, ManageActionButton, AddActionButton)
from waeup.kofa.browser.layout import (
    default_primary_nav_template, default_filedisplay_template,
    default_fileupload_template)
from waeup.kofa.students.workflow import (
    ADMITTED, PAID, REQUESTED, RETURNING, CLEARED, REGISTERED,
    VALIDATED, GRADUATED, TRANSCRIPT)
from waeup.kofa.students.browser import (
    clearance_disabled_message,
    StudentClearanceManageFormPage,
    StudentBaseManageFormPage, StudentFilesUploadPage,
    ExportPDFClearanceSlipPage, StudentsContainerPage,
    StudentsContainerManagePage, StudentBaseDisplayFormPage,
    StudentClearanceDisplayFormPage, StudentPersonalDisplayFormPage,
    StudyCourseDisplayFormPage, StudyLevelDisplayFormPage,
    CourseTicketDisplayFormPage, OnlinePaymentDisplayFormPage,
    AccommodationManageFormPage, BedTicketDisplayFormPage,
    StudentClearanceEditFormPage, StudentPersonalEditFormPage,
    PaymentsManageFormPage, StudyCourseTranscriptPage)
from waeup.kofa.students.interfaces import (
    IStudentsContainer, IStudent, IStudentStudyCourse, IStudentAccommodation,
    IStudentStudyLevel, ICourseTicket, IStudentOnlinePayment, IBedTicket,
    IStudentPaymentsContainer, IStudentsUtils
    )
from waeup.kofa.utils.helpers import get_fileformat

grok.context(IKofaObject) # Make IKofaObject the default context
grok.templatedir('browser_templates')

ALLOWED_FILE_EXTENSIONS = ('jpg', 'png', 'pdf', 'tif', 'fpm')

class StudentManageSidebar(grok.ViewletManager):
    grok.name('left_studentmanage')

class StudentManageLink(grok.Viewlet):
    """A link displayed in the student box which shows up for StudentNavigation
    objects.

    """
    grok.baseclass()
    grok.viewletmanager(StudentManageSidebar)
    grok.context(IKofaObject)
    grok.view(Interface)
    grok.order(5)
    grok.require('waeup.viewStudent')

    link = 'index'
    text = _(u'Base Data')

    def render(self):
        url = self.view.url(self.context.student, self.link)
        # Here we know that the cookie has been set
        lang = self.request.cookies.get('kofa.language')
        text = translate(self.text, 'waeup.kofa',
            target_language=lang)
        if not self.link:
            return ''
        return u'<li><a href="%s">%s</a></li>' % (
                url, text)

class StudentManageApplicationLink(StudentManageLink):
    grok.order(1)
    link = 'application_slip'
    text = _(u'Application Slip')

    def render(self):
        slip = getUtility(IExtFileStore).getFileByContext(
            self.context.student, attr=self.link)
        if slip:
            lang = self.request.cookies.get('kofa.language')
            text = translate(self.text, 'waeup.kofa',
                target_language=lang)
            url = self.view.url(self.context.student,self.link)
            return u'<li><a href="%s">%s</a></li>' % (
                    url, text)
        return ''

class StudentManageBaseLink(StudentManageLink):
    grok.order(2)
    link = 'index'
    text = _(u'Base Data')

class StudentManageClearanceLink(StudentManageLink):
    grok.order(3)
    grok.name('studentmanageclearancelink')
    link = 'view_clearance'
    text = _(u'Clearance Data')

class StudentManagePersonalLink(StudentManageLink):
    grok.order(4)
    grok.name('studentmanagepersonallink')
    link = 'view_personal'
    text = _(u'Personal Data')

class StudentManageStudyCourseLink(StudentManageLink):
    grok.order(5)
    link = 'studycourse'
    text = _(u'Study Course')

class StudentManagePaymentsLink(StudentManageLink):
    grok.order(6)
    grok.require('waeup.viewStudent')
    link = 'payments'
    text = _(u'Payments')

class StudentManageAccommodationLink(StudentManageLink):
    grok.order(7)
    grok.name('studentmanageaccommodationlink')
    grok.require('waeup.handleAccommodation')
    link = 'accommodation'
    text = _(u'Accommodation')

class StudentManageHistoryLink(StudentManageLink):
    grok.order(8)
    link = 'history'
    text = _(u'History')


class StudentsContainerManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentsContainer)
    grok.view(StudentsContainerPage)
    grok.require('waeup.manageStudent')
    text = _('Manage student section')

class StudentsContainerAddActionButton(AddActionButton):
    grok.order(1)
    grok.context(IStudentsContainer)
    grok.view(StudentsContainerManagePage)
    grok.require('waeup.manageStudent')
    text = _('Add student')
    target = 'addstudent'

class ContactActionButton(ManageActionButton):
    grok.order(5)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.manageStudent')
    icon = 'actionicon_mail.png'
    text = _('Send email')
    target = 'contactstudent'

class StudentBaseManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Manage')
    target = 'manage_base'

class StudentTrigTransActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.triggerTransition')
    icon = 'actionicon_trigtrans.png'
    text = _(u'Trigger transition')
    target = 'trigtrans'

class StudentLoginAsActionButton(ManageActionButton):
    grok.order(3)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.loginAsStudent')
    icon = 'actionicon_mask.png'
    text = _(u'Login as student')
    target = 'loginasstep1'

class AdmissionSlipActionButton(ManageActionButton):
    grok.order(4)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.viewStudent')
    icon = 'actionicon_pdf.png'
    text = _('Download admission letter')
    target = 'admission_slip.pdf'

class StudentTransferButton(ManageActionButton):
    grok.order(6)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Transfer student')
    target = 'transfer'
    icon = 'actionicon_redo.png'

class StudentDeactivateActionButton(ManageActionButton):
    grok.order(7)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Deactivate account')
    target = 'deactivate'
    icon = 'actionicon_traffic_lights_red.png'

    @property
    def target_url(self):
        if self.context.suspended:
            return ''
        return self.view.url(self.view.context, self.target)

    @property
    def onclick(self):
        return "return window.confirm(%s);" % _(
            "'A history message will be added. Are you sure?'")

class StudentActivateActionButton(ManageActionButton):
    grok.order(7)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Activate account')
    target = 'activate'
    icon = 'actionicon_traffic_lights_green.png'

    @property
    def target_url(self):
        if not self.context.suspended:
            return ''
        return self.view.url(self.view.context, self.target)

    @property
    def onclick(self):
        return "return window.confirm(%s);" % _(
            "'A history message will be added. Are you sure?'")

class StudentClearanceManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentClearanceDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Manage')
    target = 'manage_clearance'

class StudentClearActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IStudent)
    grok.view(StudentClearanceDisplayFormPage)
    grok.require('waeup.clearStudent')
    text = _('Clear student')
    target = 'clear'
    icon = 'actionicon_accept.png'

    @property
    def target_url(self):
        if clearance_disabled_message(self.context):
            return ''
        if self.context.state != REQUESTED:
            return ''
        return self.view.url(self.view.context, self.target)

class StudentRejectClearanceActionButton(ManageActionButton):
    grok.order(3)
    grok.context(IStudent)
    grok.view(StudentClearanceDisplayFormPage)
    grok.require('waeup.clearStudent')
    text = _('Reject clearance')
    target = 'reject_clearance'
    icon = 'actionicon_reject.png'

    @property
    def target_url(self):
        if clearance_disabled_message(self.context):
            return ''
        if self.context.state not in (REQUESTED, CLEARED):
            return ''
        return self.view.url(self.view.context, self.target)

class ClearanceSlipActionButton(ManageActionButton):
    grok.order(4)
    grok.context(IStudent)
    grok.view(StudentClearanceDisplayFormPage)
    grok.require('waeup.viewStudent')
    icon = 'actionicon_pdf.png'
    text = _('Download clearance slip')
    target = 'clearance_slip.pdf'

class ClearanceViewActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentClearanceEditFormPage)
    grok.require('waeup.viewStudent')
    icon = 'actionicon_view.png'
    text = _('View')
    target = 'view_clearance'

class PersonalViewActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentPersonalEditFormPage)
    grok.require('waeup.viewStudent')
    icon = 'actionicon_view.png'
    text = _('View')
    target = 'view_personal'

class StudentPersonalManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentPersonalDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Manage')
    target = 'manage_personal'

class StudentPersonalEditActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IStudent)
    grok.view(StudentPersonalDisplayFormPage)
    grok.require('waeup.handleStudent')
    text = _('Edit')
    target = 'edit_personal'

class StudyCourseManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentStudyCourse)
    grok.view(StudyCourseDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Manage')
    target = 'manage'

    @property
    def target_url(self):
        if self.context.is_current:
            return self.view.url(self.view.context, self.target)
        return False

class StudyCourseTranscriptActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IStudentStudyCourse)
    grok.view(StudyCourseDisplayFormPage)
    grok.require('waeup.viewTranscript')
    text = _('Transcript')
    target = 'transcript'
    icon = 'actionicon_transcript.png'

    @property
    def target_url(self):
        if self.context.student.transcript_enabled:
            return self.view.url(self.view.context, self.target)
        return False

class TranscriptSlipActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentStudyCourse)
    grok.view(StudyCourseTranscriptPage)
    grok.require('waeup.viewTranscript')
    text = _('Academic Transcript')
    target = 'transcript.pdf'
    icon = 'actionicon_pdf.png'

    @property
    def target_url(self):
        if self.context.student.transcript_enabled:
            return self.view.url(self.view.context, self.target)
        return False

class RevertTransferActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentStudyCourse)
    grok.view(StudyCourseDisplayFormPage)
    grok.require('waeup.manageStudent')
    icon = 'actionicon_undo.png'
    text = _('Reactivate this study course (revert previous transfer)')
    target = 'revert_transfer'

    @property
    def target_url(self):
        if self.context.is_previous:
            return self.view.url(self.view.context.__parent__, self.target)
        return False

class StudyLevelManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentStudyLevel)
    grok.view(StudyLevelDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Manage')
    target = 'manage'

    @property
    def target_url(self):
        is_current = self.context.__parent__.is_current
        if not is_current:
            return ''
        return self.view.url(self.view.context, self.target)

class StudentValidateCoursesActionButton(ManageActionButton):
    grok.order(3)
    grok.context(IStudentStudyLevel)
    grok.view(StudyLevelDisplayFormPage)
    grok.require('waeup.validateStudent')
    text = _('Validate courses')
    target = 'validate_courses'
    icon = 'actionicon_accept.png'

    @property
    def target_url(self):
        is_current = self.context.__parent__.is_current
        if self.context.student.state != REGISTERED or \
            str(self.context.__parent__.current_level) != self.context.__name__ or\
            not is_current:
            return ''
        return self.view.url(self.view.context, self.target)

class StudentRejectCoursesActionButton(ManageActionButton):
    grok.order(4)
    grok.context(IStudentStudyLevel)
    grok.view(StudyLevelDisplayFormPage)
    grok.require('waeup.validateStudent')
    text = _('Reject courses')
    target = 'reject_courses'
    icon = 'actionicon_reject.png'

    @property
    def target_url(self):
        is_current = self.context.__parent__.is_current
        if self.context.student.state not in (VALIDATED, REGISTERED) or \
            str(self.context.__parent__.current_level) != self.context.__name__ or\
            not is_current:
            return ''
        return self.view.url(self.view.context, self.target)

class CourseRegistrationSlipActionButton(ManageActionButton):
    grok.order(5)
    grok.context(IStudentStudyLevel)
    grok.view(StudyLevelDisplayFormPage)
    grok.require('waeup.viewStudent')
    icon = 'actionicon_pdf.png'
    text = _('Download course registration slip')
    target = 'course_registration_slip.pdf'

    @property
    def target_url(self):
        is_current = self.context.__parent__.is_current
        if not is_current:
            return ''
        return self.view.url(self.view.context, self.target)

class CourseTicketManageActionButton(ManageActionButton):
    grok.order(1)
    grok.context(ICourseTicket)
    grok.view(CourseTicketDisplayFormPage)
    grok.require('waeup.manageStudent')
    text = _('Manage')
    target = 'manage'

#class OnlinePaymentManageActionButton(ManageActionButton):
#    grok.order(1)
#    grok.context(IStudentPaymentsContainer)
#    grok.view(PaymentsDisplayFormPage)
#    grok.require('waeup.manageStudent')
#    text = 'Manage payments'
#    target = 'manage'

class PaymentReceiptActionButton(ManageActionButton):
    grok.order(9) # This button should always be the last one.
    grok.context(IStudentOnlinePayment)
    grok.view(OnlinePaymentDisplayFormPage)
    grok.require('waeup.viewStudent')
    icon = 'actionicon_pdf.png'
    text = _('Download payment slip')
    target = 'payment_slip.pdf'

    @property
    def target_url(self):
        #if self.context.p_state != 'paid':
        #    return ''
        return self.view.url(self.view.context, self.target)

class ApprovePaymentActionButton(ManageActionButton):
    grok.order(8)
    grok.context(IStudentOnlinePayment)
    grok.view(OnlinePaymentDisplayFormPage)
    grok.require('waeup.managePortal')
    icon = 'actionicon_accept.png'
    text = _('Approve payment')
    target = 'approve'

    @property
    def target_url(self):
        if self.context.p_state == 'paid':
            return ''
        return self.view.url(self.view.context, self.target)

class AddBedTicketActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentAccommodation)
    grok.view(AccommodationManageFormPage)
    grok.require('waeup.handleAccommodation')
    icon = 'actionicon_home.png'
    text = _('Book accommodation')
    target = 'add'

class BedTicketSlipActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IBedTicket)
    grok.view(BedTicketDisplayFormPage)
    grok.require('waeup.handleAccommodation')
    icon = 'actionicon_pdf.png'
    text = _('Download bed allocation slip')
    target = 'bed_allocation_slip.pdf'

class RelocateStudentActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IBedTicket)
    grok.view(BedTicketDisplayFormPage)
    grok.require('waeup.manageHostels')
    icon = 'actionicon_reload.png'
    text = _('Relocate student')
    target = 'relocate'

class StudentBaseActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.handleStudent')
    text = _('Edit')
    target = 'edit_base'

class StudentPasswordActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.handleStudent')
    icon = 'actionicon_key.png'
    text = _('Change password')
    target = 'change_password'

class StudentPassportActionButton(ManageActionButton):
    grok.order(3)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.handleStudent')
    icon = 'actionicon_portrait.png'
    text = _('Change portrait')
    target = 'change_portrait'

    @property
    def target_url(self):
        PWCHANGE_STATES = getUtility(IStudentsUtils).PWCHANGE_STATES
        if self.context.state not in PWCHANGE_STATES:
            return ''
        return self.view.url(self.view.context, self.target)

class StudentClearanceStartActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentClearanceDisplayFormPage)
    grok.require('waeup.handleStudent')
    icon = 'actionicon_start.gif'
    text = _('Start clearance')
    target = 'start_clearance'

    @property
    def target_url(self):
        if self.context.state != ADMITTED:
            return ''
        return self.view.url(self.view.context, self.target)

class StudentClearanceEditActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentClearanceDisplayFormPage)
    grok.require('waeup.handleStudent')
    text = _('Edit')
    target = 'cedit'

    @property
    def target_url(self):
        if self.context.clearance_locked:
            return ''
        return self.view.url(self.view.context, self.target)

class StartSessionActionButton(ManageActionButton):
    grok.order(1)
    grok.context(IStudentStudyCourse)
    grok.view(StudyCourseDisplayFormPage)
    grok.require('waeup.handleStudent')
    icon = 'actionicon_start.gif'
    text = _('Start new session')
    target = 'start_session'

    @property
    def target_url(self):
        if self.context.next_session_allowed and self.context.is_current:
            return self.view.url(self.view.context, self.target)
        return False

class AddStudyLevelActionButton(AddActionButton):
    grok.order(1)
    grok.context(IStudentStudyCourse)
    grok.view(StudyCourseDisplayFormPage)
    grok.require('waeup.handleStudent')
    text = _('Add course list')
    target = 'add'

    @property
    def target_url(self):
        student = self.view.context.student
        condition1 = student.state != PAID
        condition2 = str(student['studycourse'].current_level) in \
            self.view.context.keys()
        condition3 = not self.context.is_current
        if condition1 or condition2 or condition3:
            return ''
        return self.view.url(self.view.context, self.target)

class StudyLevelEditActionButton(ManageActionButton):
    grok.order(2)
    grok.context(IStudentStudyLevel)
    grok.view(StudyLevelDisplayFormPage)
    grok.require('waeup.editStudyLevel')
    text = _('Edit course list')
    target = 'edit'

    @property
    def target_url(self):
        student = self.view.context.student
        condition1 = student.state == PAID
        condition2 = self.view.context.is_current_level
        is_current = self.context.__parent__.is_current
        if condition1 and condition2 and is_current:
            return self.view.url(self.view.context, self.target)
        return ''

class AddPaymentActionButton(AddActionButton):
    grok.order(1)
    grok.context(IStudentPaymentsContainer)
    grok.view(PaymentsManageFormPage)
    grok.require('waeup.payStudent')
    text = _('Add current session payment ticket')
    target = 'addop'

class AddPreviousPaymentActionButton(AddActionButton):
    grok.order(2)
    grok.context(IStudentPaymentsContainer)
    grok.view(PaymentsManageFormPage)
    grok.require('waeup.payStudent')
    grok.name('addpreviouspaymentactionbutton')
    text = _('Add previous session payment ticket')
    target = 'addpp'

    @property
    def target_url(self):
        student = self.view.context.student
        if student.before_payment or not self.target:
            return ''
        return self.view.url(self.view.context, self.target)

class AddBalancePaymentActionButton(AddActionButton):
    grok.order(3)
    grok.context(IStudentPaymentsContainer)
    grok.view(PaymentsManageFormPage)
    grok.require('waeup.manageStudent')
    grok.name('addbalancepaymentactionbutton')
    text = _('Add balance payment ticket')
    target = 'addbp'

    @property
    def target_url(self):
        if not self.target:
            return ''
        return self.view.url(self.view.context, self.target)

class RequestTranscriptActionButton(ManageActionButton):
    grok.order(8)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.handleStudent')
    text = _('Request transcript')
    target = 'request_transcript'
    icon = 'actionicon_transcript.png'

    @property
    def target_url(self):
        if self.context.state != GRADUATED:
            return ''
        return self.view.url(self.view.context, self.target)

class ProcessTranscriptRequestActionButton(ManageActionButton):
    grok.order(9)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.viewTranscript')
    text = _('Manage transcript request')
    target = 'process_transcript_request'
    icon = 'actionicon_transcript.png'

    @property
    def target_url(self):
        if self.context.state != TRANSCRIPT:
            return ''
        return self.view.url(self.view.context, self.target)

class StudentsTab(PrimaryNavTab):
    """Students tab in primary navigation.
    """

    grok.context(IKofaObject)
    grok.order(4)
    grok.require('waeup.viewStudentsTab')
    grok.name('studentstab')

    pnav = 4
    tab_title = _(u'Students')

    @property
    def link_target(self):
        return self.view.application_url('students')

class PrimaryStudentNavManager(grok.ViewletManager):
    """Viewlet manager for the primary navigation tab.
    """
    grok.name('primary_nav_student')

class PrimaryStudentNavTab(grok.Viewlet):
    """Base for primary student nav tabs.
    """
    grok.baseclass()
    grok.context(IKofaObject)
    grok.viewletmanager(PrimaryStudentNavManager)
    template = default_primary_nav_template
    grok.order(1)
    grok.require('waeup.Authenticated')
    pnav = 0
    tab_title = u'Some Text'

    @property
    def link_target(self):
        return self.view.application_url()

    @property
    def active(self):
        view_pnav = getattr(self.view, 'pnav', 0)
        if view_pnav == self.pnav:
            return 'active'
        return ''

class MyStudentDataTab(PrimaryStudentNavTab):
    """MyData dropdown tab in primary navigation.
    """
    grok.order(3)
    grok.require('waeup.viewMyStudentDataTab')
    grok.template('mydatadropdowntabs')
    grok.name('mystudentdatatab')
    pnav = 4
    tab_title = _(u'My Data')

    @property
    def active(self):
        view_pnav = getattr(self.view, 'pnav', 0)
        if view_pnav == self.pnav:
            return 'active dropdown'
        return 'dropdown'

    @property
    def targets(self):
        student = grok.getSite()['students'][self.request.principal.id]
        student_url = self.view.url(student)
        app_slip = getUtility(IExtFileStore).getFileByContext(
            student, 'application_slip')
        targets = []
        if app_slip:
            targets = [{'url':student_url + '/application_slip',
                        'title':_('Application Slip')},]
        targets += [
            {'url':student_url, 'title':'Base Data'},
            {'url':student_url + '/view_clearance',
             'title':_('Clearance Data')},
            {'url':student_url + '/view_personal', 'title':_('Personal Data')},
            {'url':student_url + '/studycourse', 'title':_('Study Course')},
            {'url':student_url + '/payments', 'title':_('Payments')},
            {'url':student_url + '/accommodation',
             'title':_('Accommodation Data')},
            {'url':student_url + '/history', 'title':_('History')},
            ]
        return targets

def handle_file_delete(context, view, download_name):
    """Handle deletion of student file.

    """
    store = getUtility(IExtFileStore)
    store.deleteFileByContext(context, attr=download_name)
    context.writeLogMessage(view, 'deleted: %s' % download_name)
    view.flash(_('${a} deleted.', mapping = {'a':download_name}))
    return

def handle_file_upload(upload, context, view, max_size, download_name=None):
    """Handle upload of student file.

    Returns `True` in case of success or `False`.

    Please note that file pointer passed in (`upload`) most probably
    points to end of file when leaving this function.
    """
    # Check some file requirements first
    size = file_size(upload)
    if size > max_size:
        view.flash(_('Uploaded file is too big.'), type="danger")
        return False
    upload.seek(0) # file pointer moved when determining size
    dummy,ext = os.path.splitext(upload.filename)
    # fpm files are expected to be fingerprint minutiae, file
    # format is not yet checked
    if ext == '.fpm':
        file_format = 'fpm'
    else:
        file_format = get_fileformat(None, upload.read(512))
        upload.seek(0) # same here
    if file_format is None:
        view.flash(_('Could not determine file type.'), type="danger")
        return False
    basename, expected_ext = os.path.splitext(download_name)
    if expected_ext:
        if '.' + file_format != expected_ext:
            view.flash(_('${a} file extension expected.',
                mapping = {'a':expected_ext[1:]}), type="danger")
            return False
    else:
        if not file_format in ALLOWED_FILE_EXTENSIONS:
            view.flash(
                _('Only the following extensions are allowed: ${a}',
                mapping = {'a':', '.join(ALLOWED_FILE_EXTENSIONS)}),
                type="danger")
            return False
        download_name += '.' + file_format
    store = getUtility(IExtFileStore)
    file_id = IFileStoreNameChooser(context).chooseName(attr=download_name)
    store.createFile(file_id, upload)
    context.writeLogMessage(view, 'uploaded: %s (%s)' % (
        download_name,upload.filename))
    view.flash(_('File ${a} uploaded.', mapping = {'a':download_name}))
    return True

class FileManager(grok.ViewletManager):
    """Viewlet manager for uploading files, preferably scanned images.
    """
    grok.name('files')

class FileDisplay(grok.Viewlet):
    """Base file display viewlet.
    """
    grok.baseclass()
    grok.context(IStudent)
    grok.viewletmanager(FileManager)
    grok.view(StudentClearanceDisplayFormPage)
    template = default_filedisplay_template
    grok.order(1)
    grok.require('waeup.viewStudent')
    label = _(u'File')
    title = _(u'Scan')
    download_name = u'filename.jpg'

    @property
    def file_exists(self):
        image = getUtility(IExtFileStore).getFileByContext(
            self.context, attr=self.download_name)
        if image:
            return True
        else:
            return False

class FileUpload(FileDisplay):
    """Base upload viewlet.
    """
    grok.baseclass()
    grok.context(IStudent)
    grok.viewletmanager(FileManager)
    grok.view(StudentClearanceManageFormPage)
    template = default_fileupload_template
    grok.require('waeup.uploadStudentFile')
    tab_redirect = '#tab2-top'
    mus = 1024 * 150
    upload_button =_('Upload selected file')
    delete_button = _('Delete')

    @property
    def show_viewlet(self):
        students_utils = getUtility(IStudentsUtils)
        if self.__name__ in students_utils.SKIP_UPLOAD_VIEWLETS:
            return False
        return True

    @property
    def input_name(self):
        return "%s" % self.__name__

    def update(self):
        self.max_upload_size = string_from_bytes(self.mus)
        delete_button = self.request.form.get(
            'delete_%s' % self.input_name, None)
        upload_button = self.request.form.get(
            'upload_%s' % self.input_name, None)
        if delete_button:
            handle_file_delete(
                context=self.context, view=self.view,
                download_name=self.download_name)
            self.view.redirect(
                self.view.url(
                    self.context, self.view.__name__) + self.tab_redirect)
            return
        if upload_button:
            upload = self.request.form.get(self.input_name, None)
            if upload:
                # We got a fresh upload
                handle_file_upload(upload,
                    self.context, self.view, self.mus, self.download_name)
                self.view.redirect(
                    self.view.url(
                        self.context, self.view.__name__) + self.tab_redirect)
            else:
                self.view.flash(_('No local file selected.'), type="danger")
                self.view.redirect(
                    self.view.url(
                        self.context, self.view.__name__) + self.tab_redirect)
        return

class PassportDisplay(FileDisplay):
    """Passport display viewlet.
    """
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentBaseDisplayFormPage)
    grok.require('waeup.viewStudent')
    grok.template('imagedisplay')
    label = _(u'Passport Picture')
    download_name = u'passport.jpg'

class PassportUploadManage(FileUpload):
    """Passport upload viewlet for officers.
    """
    grok.order(1)
    grok.context(IStudent)
    grok.view(StudentBaseManageFormPage)
    grok.require('waeup.manageStudent')
    grok.template('imageupload')
    label = _(u'Passport Picture (jpg only)')
    mus = 1024 * 50
    download_name = u'passport.jpg'
    tab_redirect = '#tab2'

class PassportUploadEdit(PassportUploadManage):
    """Passport upload viewlet for students.
    """
    grok.view(StudentFilesUploadPage)
    grok.require('waeup.uploadStudentFile')

class BirthCertificateDisplay(FileDisplay):
    """Birth Certificate display viewlet.
    """
    grok.order(1)
    label = _(u'Birth Certificate')
    title = _(u'Birth Certificate Scan')
    download_name = u'birth_certificate'

class BirthCertificateSlip(BirthCertificateDisplay):
    grok.view(ExportPDFClearanceSlipPage)

class BirthCertificateUpload(FileUpload):
    """Birth Certificate upload viewlet.
    """
    grok.order(1)
    label = _(u'Birth Certificate')
    title = _(u'Birth Certificate Scan')
    mus = 1024 * 150
    download_name = u'birth_certificate'
    tab_redirect = '#tab2-top'

class Image(grok.View):
    """Renders images for students.
    """
    grok.baseclass()
    grok.name('none.jpg')
    grok.context(IStudent)
    grok.require('waeup.viewStudent')
    download_name = u'none.jpg'

    def render(self):
        # A filename chooser turns a context into a filename suitable
        # for file storage.
        image = getUtility(IExtFileStore).getFileByContext(
            self.context, attr=self.download_name)
        if image is None:
            # show placeholder image
            self.response.setHeader('Content-Type', 'image/jpeg')
            return open(DEFAULT_IMAGE_PATH, 'rb').read()
        dummy,ext = os.path.splitext(image.name)
        if ext == '.jpg':
            self.response.setHeader('Content-Type', 'image/jpeg')
        elif ext == '.fpm':
            self.response.setHeader('Content-Type', 'application/binary')
        elif ext == '.png':
            self.response.setHeader('Content-Type', 'image/png')
        elif ext == '.pdf':
            self.response.setHeader('Content-Type', 'application/pdf')
        elif ext == '.tif':
            self.response.setHeader('Content-Type', 'image/tiff')
        return image

class Passport(Image):
    """Renders jpeg passport picture.
    """
    grok.name('passport.jpg')
    download_name = u'passport.jpg'
    grok.context(IStudent)

class ApplicationSlipImage(Image):
    """Renders application slip scan.
    """
    grok.name('application_slip')
    download_name = u'application_slip'

class BirthCertificateImage(Image):
    """Renders birth certificate scan.
    """
    grok.name('birth_certificate')
    download_name = u'birth_certificate'
