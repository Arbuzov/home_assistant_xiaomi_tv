from .hass_web_proxy_lib import ProxyView, ProxiedURL


class MyProxyView(ProxyView):
    """Прокси-представление для вашей интеграции."""

    url = "/api/xiaomi_tv/proxy/"
    name = "api:xiaomi_tv:proxy"

    def _get_proxied_url(self, request):
        """Возвращает объект ProxiedURL с параметрами проксирования."""
        target_url = request.query.get("url")
        if not target_url:
            raise ValueError("Параметр 'url' не указан")
        return ProxiedURL(url=target_url)
