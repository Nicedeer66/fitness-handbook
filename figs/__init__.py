from . import base, cover  # noqa: F401
import importlib
for _m in ('concepts', 'body', 'pose', 'pose2', 'life'):
    try:
        importlib.import_module('.' + _m, __name__)
    except ModuleNotFoundError as e:
        if _m not in str(e):
            raise
