try:
    from src.shared.pyjwt.backends.cryptography_backend import get_random_bytes  # noqa: F401
except ImportError:
    try:
        from src.shared.pyjwt.backends.pycrypto_backend import get_random_bytes  # noqa: F401
    except ImportError:
        from src.shared.pyjwt.backends.native import get_random_bytes  # noqa: F401

try:
    from src.shared.pyjwt.backends.cryptography_backend import CryptographyRSAKey as RSAKey  # noqa: F401
except ImportError:
    try:
        from src.shared.pyjwt.backends.rsa_backend import RSAKey  # noqa: F401
    except ImportError:
        RSAKey = None

try:
    from src.shared.pyjwt.backends.cryptography_backend import CryptographyECKey as ECKey  # noqa: F401
except ImportError:
    from src.shared.pyjwt.backends.ecdsa_backend import ECDSAECKey as ECKey  # noqa: F401

try:
    from src.shared.pyjwt.backends.cryptography_backend import CryptographyAESKey as AESKey  # noqa: F401
except ImportError:
    AESKey = None

try:
    from src.shared.pyjwt.backends.cryptography_backend import CryptographyHMACKey as HMACKey  # noqa: F401
except ImportError:
    from src.shared.pyjwt.backends.native import HMACKey  # noqa: F401

from .base import DIRKey  # noqa: F401