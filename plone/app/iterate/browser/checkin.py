##################################################################
#
# (C) Copyright 2006 ObjectRealms, LLC
# All Rights Reserved
#
# This file is part of iterate.
#
# iterate is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# iterate is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with iterate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
##################################################################

from zope.component import getMultiAdapter

from Acquisition import aq_inner
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.iterate.interfaces import ICheckinCheckoutPolicy
from plone.app.iterate.interfaces import CheckinException

class Checkin(BrowserView):
    
    template = ViewPageTemplateFile('checkin.pt')
    
    def __call__(self):
        context = aq_inner(self.context)
        
        if self.request.form.has_key('form.button.Checkin'):
            control = getMultiAdapter((context, self.request), name=u"iterate_control")
            if not control.checkin_allowed():
                raise CheckinException(u"Not a checkout")

            message = self.request.form.get('checkin_message', "")

            policy = ICheckinCheckoutPolicy(context)
            baseline = policy.checkin(message)
            baseline.reindexObject()
            
            IStatusMessage(self.request).addStatusMessage("Checked in", type='info')
            self.request.response.redirect(baseline.absolute_url())
        elif self.request.form.has_key('form.button.Cancel'):
            self.request.response.redirect(self.context.absolute_url())
        else:
            return self.template()