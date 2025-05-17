import logging
from .hass_web_proxy_lib import ProxyView, ProxiedURL

_LOGGER = logging.getLogger(__name__)


class MyProxyView(ProxyView):
    """Прокси-представление для вашей интеграции."""

    url = "/api/xiaomi_tv/proxy/"
    name = "api:xiaomi_tv:proxy"

    def _get_proxied_url(self, request):
        """Get the proxied URL."""
        target_url = request.query.get("url")
        if not target_url:
            raise ValueError("The 'url' was not set")
        _LOGGER.error("Proxied URL: %s", target_url)
        try:
            return ProxiedURL(url=target_url)
        except Exception as err:
            _LOGGER.error("Error creating ProxiedURL: %s %s", target_url, err)
            raise
