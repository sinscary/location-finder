from model import Grant
from datetime import datetime, timedelta
from flask_oauthlib.provider import OAuth2Provider
from api import oauth, app, db

def delete(self):
	db.session.delete(self)
	db.session.commit()
	return self

@property
def scopes(self):
	if self._scopes:
		return self._scopes.split()
	return []

@oauth.grantgetter
def load_grant(client_id, code):
	return Grant.query.filter_by(client_id=client_id, code=code).first()

@oauth.grantsetter
def save_grant(client_id, code, request, *args, **kwargs):
	expires = datetime.utcnow() + timedelta(seconds=100)
	grant = Grant(
		client_id = client_id,
		code = code['code'],
		redirect_uri=request.redirect_uri,
		_scopes=' '.join(request.scopes),
		user = get_current_user(),
		expires = expires
		)
	db.session.add(grant)
	db.session.commit()
	return grant