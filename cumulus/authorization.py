from tastypie.authorization import Authorization

class HostAuthorization(Authorization):
    def _auth_obj(self, obj, bundle):
        # hosts are allowed to examine/change their own data
        # and superusers can change any data
        return obj.name == bundle.request.user.name or \
            bundle.request.user.is_superuser

    def _auth_objs(self, object_list, bundle):
        return [ o for o in object_list if self._auth_obj(o, bundle) ]
    
    def read_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     

    def create_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     

    def update_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     
    
    def delete_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     

    read_list = _auth_objs
    create_list = _auth_objs
    update_list = _auth_objs
    delete_list = _auth_objs

class KeyAuthorization(Authorization):
    def _auth_obj(self, object_list, bundle):
        return bundle.request.user.is_superuser

    def _auth_objs(self, object_list, bundle):
        result = []
        if bundle.request.user.is_superuser:
            result = object_list
        return result

    # changing keys requires superuser
    create_detail = _auth_obj
    update_detail = _auth_obj
    delete_detail = _auth_obj
    create_list = _auth_objs
    update_list = _auth_objs
    delete_list = _auth_objs

class DataAuthorization(Authorization):
    def _auth_obj(self, obj, bundle):
        return obj.host.name == bundle.request.user.name or \
            bundle.request.user.is_superuser

    def _auth_objs(self, object_list, bundle):
        return [ o for o in object_list if self._auth_obj(o, bundle) ]

    def read_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     

    def create_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     

    def update_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     
    
    def delete_detail(self, object_list, bundle):
        return self._auth_obj(bundle.obj, bundle)     

    read_list = _auth_objs
    create_list = _auth_objs
    update_list = _auth_objs
    delete_list = _auth_objs
