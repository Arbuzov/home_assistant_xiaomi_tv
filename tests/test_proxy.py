import sys
import types
import ssl
import aiohttp
from aiohttp.test_utils import make_mocked_request
import pytest

# Create minimal homeassistant stubs required for import
ha = types.ModuleType('homeassistant')
components = types.ModuleType('homeassistant.components')
http = types.ModuleType('homeassistant.components.http')
util = types.ModuleType('homeassistant.util')
ssl_mod = types.ModuleType('homeassistant.util.ssl')

http.KEY_AUTHENTICATED = 'authenticated'
class HomeAssistantView:
    pass
http.HomeAssistantView = HomeAssistantView

ssl_mod.get_default_context = ssl.create_default_context
util.ssl = ssl_mod

components.http = http
ha.components = components
ha.util = util

sys.modules.setdefault('homeassistant', ha)
sys.modules.setdefault('homeassistant.components', components)
sys.modules.setdefault('homeassistant.components.http', http)
sys.modules.setdefault('homeassistant.util', util)
sys.modules.setdefault('homeassistant.util.ssl', ssl_mod)
sys.modules.setdefault('pymitv', types.ModuleType('pymitv'))

import importlib.util
from pathlib import Path

PROXY_PATH = Path(__file__).resolve().parents[1] / "custom_components" / "xiaomi_tv" / "proxy.py"

# Create fake package structure to load the proxy module without executing the
# real package __init__ which has heavy dependencies.
custom_components_pkg = types.ModuleType('custom_components')
xiaomi_tv_pkg = types.ModuleType('custom_components.xiaomi_tv')
xiaomi_tv_pkg.__path__ = [str(PROXY_PATH.parent)]
sys.modules.setdefault('custom_components', custom_components_pkg)
sys.modules.setdefault('custom_components.xiaomi_tv', xiaomi_tv_pkg)

spec = importlib.util.spec_from_file_location(
    'custom_components.xiaomi_tv.proxy', PROXY_PATH
)
proxy = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = proxy
spec.loader.exec_module(proxy)
MyProxyView = proxy.MyProxyView


@pytest.mark.asyncio
async def test_get_proxied_url_missing_url():
    async with aiohttp.ClientSession() as session:
        view = MyProxyView(session)
        request = make_mocked_request('GET', '/api/xiaomi_tv/proxy')
        assert view._get_proxied_url(request) is None
