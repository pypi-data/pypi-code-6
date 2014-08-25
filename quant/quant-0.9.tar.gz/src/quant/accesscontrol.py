from dm.accesscontrol import SystemAccessController
from dm.exceptions import *
from quant.dictionarywords import AC_SKIP_ROLE_INFERENCE

moddebug = False

class AccessController(SystemAccessController):
    "Introduces project member role to access controller."

    def isAccessAuthorised(self, **kwds):
        return super(AccessController, self).isAccessAuthorised(**kwds)

    def assertAccessAuthorised(self):
        if not self.dictionary[AC_SKIP_ROLE_INFERENCE]:
            if self.isInferredRoleAuthorised():
                raise AccessIsAuthorised
        else:
            if moddebug and self.debug:
                msg = "Access not authorised by skipping role inference."
                self.logger.debug(msg)
        super(AccessController, self).assertAccessAuthorised()

    def isInferredRoleAuthorised(self):
        roleName = self.inferRoleName()
        if roleName:
            role = self.registry.roles[roleName]
        else:
            role = None
        if role and self.isRoleAuthorised(role):
            if self.debug:
                msg = "Access authorised by inferred '%s' role." % roleName
                self.logger.debug(msg)
            return True
        elif role:
            if self.debug:
                msg = "Access not authorised by inferred '%s' role." % roleName
                self.logger.debug(msg)
            return False
        else:
            if self.debug:
                msg = "Access not authorised as no role was inferred."
                self.logger.debug(msg)
            return False

    def inferRoleName(self):
        roleName = ''
        if self.isProtectedObjectClassName('Person'):
            if self.person == self.protectedObject:
                return 'Administrator'
        if not self.person.researcher:
            return ''
        viewingResearcher = self.person.researcher
        if self.isProtectedObjectClassName('Approval'):
            approval = self.protectedObject
            if viewingResearcher in approval.principalInvestigators:
                return 'PrincipalInvestigator'
            if viewingResearcher in approval.additionalResearchers:
                return 'Researcher'
            for study in approval.studies.keys():
                if viewingResearcher in study.principalInvestigators:
                    return 'Researcher'
                for group in study.groups.keys():
                    if viewingResearcher in group.principals:
                        return 'Researcher'
        elif self.isProtectedObjectClassName('Group'):
            group = self.protectedObject
            if viewingResearcher in group.principals:
                return 'PrincipalInvestigator'
            elif viewingResearcher in group.researchers:
                return 'Researcher'
        elif self.isProtectedObjectClassName('Researcher'):
            researcher = self.protectedObject
            groupList = []
            groupList += researcher.principalships.keys()
            groupList += researcher.memberships.keys()
            for group in groupList:
                if viewingResearcher in group.principals:
                    return 'PrincipalInvestigator'
            for group in groupList:
                if viewingResearcher in group.researchers:
                    return 'Researcher'
        elif self.isProtectedObjectClassName('Study'):
            study = self.protectedObject
            if viewingResearcher in study.principalInvestigators:
                return 'PrincipalInvestigator'
            for group in study.groups.keys():
                if viewingResearcher in group.principals:
                    return 'PrincipalInvestigator'
            for group in study.groups.keys():
                if viewingResearcher in group.researchers:
                    return 'Researcher'
        elif self.isProtectedObjectClassName('Project'):
            project = self.protectedObject
            if viewingResearcher in project.researchers:
                return 'PrincipalInvestigator'
            for study in project.studies.keys():
                if viewingResearcher in study.principalInvestigators:
                    return 'PrincipalInvestigator'
                for group in study.groups.keys():
                    if viewingResearcher in group.principals:
                        return 'PrincipalInvestigator'
            for study in project.studies.keys():
                for group in study.groups.keys():
                    if viewingResearcher in group.researchers:
                        return 'Researcher'
        elif self.isProtectedObjectClassName('Report'):
            report = self.protectedObject
            if viewingResearcher in report.reportsTo:
                return 'PrincipalInvestigator'
        return roleName
    
    def isProtectedObjectClassName(self, className):
        protectedObjectClass = self.protectedObject.__class__
        namedClass = self.registry.getDomainClass(className)
        return protectedObjectClass == namedClass
        
    def isResearcherPerson(self):
        if self.isProtectedObjectClassName('Researcher'):
            researcher = self.protectedObject
            if researcher == self.person.researcher:
                return True
        return False

