import json
from functools import wraps
from urllib.request import urlopen

from flask import _request_ctx_stack, request
from jose import jwt

AUTH0_DOMAIN = 'dev-deinyefa.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'casting-agency'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    auth_header = request.headers.get('Authorization', None)

    if auth_header is None:
        raise AuthError({
            'code': 'missing_authorization_header',
            'message': 'There is no Authothorization header in this request'
        }, 401)

    auth_header_parts = auth_header.split(' ')

    if len(auth_header_parts) != 2:
        raise AuthError({
            'code': 'invalid_authorization_header',
            'message': 'Authorization should be a bearer token'
        }, 401)
    elif auth_header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_authorization_header',
            'message': 'Your authorization header should begin with "Bearer"'
        }, 401)

    return auth_header_parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'No permissions in the provided payload'
        }, 400)

    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'not_authorized',
            'description': 'Permission not found'
        }, 401)

    return True


def verify_decode_jwt(token):
    rsa_key = {}
    jsonurl = urlopen(f'https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Malformed authorization. Missing kid'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'expired_token',
                'description': 'The provided token has expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check your audience/issuer'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_auth_header',
                'descripion': 'Unable to auth token'
            }, 400)

    raise AuthError({
        'code': 'invalid_auth_header',
        'descripion': 'Something went wrong. Unable to validate header'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except Exception as e:
                print(e)
                raise AuthError({
                    'code': 'expired_token',
                    'description': 'The provided token has expired'
                }, 401)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
