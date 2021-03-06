from django.template import RequestContext
from django.template.loader import render_to_string

class BaseItem(object):
    template = 'wagtailadmin/userbar/item_base.html'

    def render(self, request):
        return render_to_string(self.template, dict(self=self, request=request), context_instance=RequestContext(request))

class AddPageItem(BaseItem):
    template = 'wagtailadmin/userbar/item_page_add.html'

    def __init__(self, page):
        self.page = page
        self.parent_page = page.get_parent()

    def render(self, request):
        # Don't render if the page doesn't have an id
        if not self.page.id:
            return ""

        # Don't render if user doesn't have permission to access the admin area
        if not request.user.has_perm('wagtailadmin.access_admin'):
            return ""

        # Don't render if user doesn't have ability to add siblings
        permission_checker = self.page.get_parent().permissions_for_user(request.user)
        if not permission_checker.can_add_subpage():
            return ""

        return super(AddPageItem, self).render(request)

class EditPageItem(BaseItem):
    template = 'wagtailadmin/userbar/item_page_edit.html'

    def __init__(self, page):
        self.page = page

    def render(self, request):
        # Don't render if the page doesn't have an id
        if not self.page.id:
            return ""

        # Don't render if user doesn't have permission to access the admin area
        if not request.user.has_perm('wagtailadmin.access_admin'):
            return ""
 
        # Don't render if the user doesn't have permission to edit this page
        permission_checker = self.page.permissions_for_user(request.user)
        if not permission_checker.can_edit():
            return ""

        return super(EditPageItem, self).render(request)

class ModeratePageItem(BaseItem):

    def __init__(self, revision):
        self.revision = revision

    def render(self, request):
        if not self.revision.id:
            return ""

        if not self.revision.submitted_for_moderation:
            return ""

        if not request.user.has_perm('wagtailadmin.access_admin'):
            return ""

        if not self.revision.page.permissions_for_user(request.user).can_publish():
            return ""
       
        return super(ModeratePageItem, self).render(request)

class ApproveModerationEditPageItem(ModeratePageItem):
    template = 'wagtailadmin/userbar/item_page_approve.html'

class RejectModerationEditPageItem(ModeratePageItem):
    template = 'wagtailadmin/userbar/item_page_reject.html'
