from django.forms.models import ModelChoiceField
from tastypie.validation import FormValidation

# Based on https://github.com/toastdriven/django-tastypie/issues/152#issuecomment-6438894
class ModelFormValidation(FormValidation):
    """
    Override tastypie's standard ``FormValidation`` since this does not care
    about URI to PK conversion for ``ToOneField`` or ``ToManyField``.
    """

    def uri_to_pk(self, uri):
        """
        Returns the integer PK part of a URI.

        Assumes ``/api/v1/resource/123/`` format. If conversion fails, this just
        returns the URI unmodified.

        Also handles lists of URIs
        """

        if uri is None:
            return None

        # handle all passed URIs
        converted = None
        try:
            if isinstance(uri, dict):
                if isinstance(uri.get('id'), int):
                    converted = uri['id']
            else:
                converted = int(uri.split('/')[-1])
                
        except (IndexError, ValueError):
            raise ValueError(
                "URI %s could not be converted to PK integer." % uri)

        # convert back to original format
        return converted

    def form_args(self, bundle):
        kwargs = super(ModelFormValidation, self).form_args(bundle)

        relation_fields = [name for name, field in
                           self.form_class.base_fields.items()
                           if issubclass(field.__class__, ModelChoiceField)]

        for field in relation_fields:
            if field in kwargs['data']:
                kwargs['data'][field] = self.uri_to_pk(kwargs['data'][field])

        return kwargs

