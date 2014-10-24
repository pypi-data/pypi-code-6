# -*- coding: utf-8 -*-
# copyright 2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact http://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

""" Clinical scales """



# http://en.wikipedia.org/wiki/Performance_status#Lansky_score
LANSKY_SCORE = [(100, u'fully active, normal'),
                (90,u'minor restrictions in strenuous physical activity'),
                (80, u'active, but gets tired more quickly'),
                (70, u'greater restriction of play and less time spent in play activity'),
                (60, u'up and around, but active play minimal; keeps busy by being involved in quieter activities'),
                (50, u'lying around much of the day, but gets dressed; no active playing participates in all quiet play and activities'),
                (40, u'mainly in bed; participates in quiet activities'),
                (30, u'bedbound; needing assistance even for quiet play'),
                (20, u'sleeping often; play entirely limited to very passive activities'),
                (10, u"doesn't play; does not get out of bed"),
                (0, u"unresponsive")]

# http://en.wikipedia.org/wiki/Performance_status#Karnofsky_scoring
KARNOFSKY_SCORE = [(100, u'Normal; no complaints; no evidence of disease.'),
                   (90, u'Able to carry on normal activity; minor signs or symptoms of disease.'),
                   (80, u'Normal activity with effort; some signs or symptoms of disease.'),
                   (70, u'Cares for self; unable to carry on normal activity or to do active work.'),
                   (60, u'Requires occasional assistance, but is able to care for most of his personal needs.'),
                   (50, u'Requires considerable assistance and frequent medical care.'),
                   (40, u'Disabled; requires special care and assistance.'),
                   (30, u'Severely disabled; hospital admission is indicated although death not imminent.'),
                   (20, u'Very sick; hospital admission necessary; active supportive treatment necessary.'),
                   (10, u'Moribund; fatal processes progressing rapidly.'),
                   (0, u'Dead')]

#http://en.wikipedia.org/wiki/Performance_status#ECOG.2FWHO.2FZubrod_score
ECOG_SCORE = [(0, u'Asymptomatic (Fully active, able to carry on all predisease activities without restriction)'),
              (1, u'Symptomatic but completely ambulatory (Restricted in physically strenuous activity but ambulatory and able to carry out work of a light or sedentary nature. For example, light housework, office work)'),
              (2, u'Symptomatic, <50% in bed during the day (Ambulatory and capable of all self care but unable to carry out any work activities. Up and about more than 50% of waking hours)'),
              (3, u'Symptomatic, >50% in bed, but not bedbound (Capable of only limited self-care, confined to bed or chair 50% or more of waking hours)'),
              (4, u'Bedbound (Completely disabled. Cannot carry on any self-care. Totally confined to bed or chair)'),
              (5, u'Death')]

#http://en.wikipedia.org/wiki/Response_Evaluation_Criteria_in_Solid_Tumors
RECIST_SCORE_TARGET = [u'Complete Response (CR): Disappearance of all target lesions',
                       u'Partial Response (PR): At least a 30% decrease in the sum of the LD of target lesions, taking as reference the baseline sum LD',
                       u'Stable Disease (SD): Neither sufficient shrinkage to qualify for PR nor sufficient increase to qualify for PD, taking as reference the smallest sum LD since the treatment started',
                       u'Progressive Disease (PD): At least a 20% increase in the sum of the LD of target lesions, taking as reference the smallest sum LD recorded since the treatment started or the appearance of one or more new lesions']

RECIST_SCORE_NONTARGET = [u'Complete Response (CR): Disappearance of all non-target lesions and normalization of tumor marker level',
                          u'Incomplete Response/ Stable Disease (SD): Persistence of one or more non-target lesion(s) or/and maintenance of tumor marker level above the normal limits',
                          u'Progressive Disease (PD): Appearance of one or more new lesions and/or unequivocal progression of existing non-target lesions']

