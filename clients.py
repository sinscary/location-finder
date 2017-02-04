from model import Client
from api import oauth

@property
def redirect_uris(self):
	if self._redirect_uris:
		return self._redirect_uris.split()
	return []

@property
def default_redirect_uri(self):
	return self.redirect_uris[0]

@property
def default_scopes(self):
	if self._default_scopes:
		return self._default_scopes.split()
	return []

@oauth.clientgetter
def load_client(client_id):
	return Client.query.filter_by(client_id=client_id).first()