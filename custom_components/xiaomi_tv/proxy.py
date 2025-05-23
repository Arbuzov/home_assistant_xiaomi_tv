import logging

from .hass_web_proxy_lib import ProxiedURL, ProxyView

LOGGER = logging.getLogger(__name__)


class MyProxyView(ProxyView):
    """Proxy image to the Xiaomi TV."""

    url = "/api/xiaomi_tv/proxy/"
    name = "api:xiaomi_tv:proxy"

    def _get_proxied_url(self, request):
        """Get the proxied URL."""
        target_url = request.query.get("url")
        if not target_url:
            LOGGER.error("No target URL provided")
            return None
        try:
            return ProxiedURL(
              target_url,
              headers={},
              allow_unauthenticated=True
            )
        except Exception as e:
            LOGGER.error(f"Failed to create proxied URL: {e}")
            return None
