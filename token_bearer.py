from model import Token
from api import oauth, app, db
from datetime import datetime, timedelta

def delete(self):
	db.session.delete(self)
	db.session.commit()
	return self

@property
def scopes(self):
	if self._scopes:
		return self._scopes.split()

	return []

@oauth.tokengetter
def load_token(access_token=None, refresh_token=None):
	if access_token:
		return Token.query.filter_by(access_token=access_token).first()
	elif refresh_token:
		return Token.query.filter_by(refresh_token=refresh_token).first()

@oauth.tokensetter
def save_token(token, request, *args, **kwargs):
	toks = Token.query.filter_by(client_id=request.client.client_id)
	for t in toks:
		db.session.delete(t)

	expires_in = token.get('expires_in')
	expires = datetime.utcnow()+timedelta(seconds=expires_in)

	tok = Token(
		access_token = token['access_token'],
		refresh_token = token['refresh_token'],
		token_type = token['token_type'],
		_scope=token['scope'],
		expires = expires,
		client_id = request.client.client_id,
		)

	db.session.add(tok)
	db.session.commit()
	return token