DOMAIN = "xiaomi_tv"

PYMITV_HACK = [
    {
        'file': 'tv.py',
        'from': '        self.volume = Control().get_volume(self.ip_address)',
        'to': '        # self.volume = Control().get_volume(self.ip_address)',
        'line': 32
    },
    {
        'file': 'discover.py',
        'from': 'request_timeout = 0.1',
        'to': 'request_timeout = 1'
    },
    {
        'file': 'control.py',
        'from': 'http://{}:6095/general?action=getVolum',
        'to': 'http://{}:6095/controller?action=getVolume'
    },
    {
        'file': 'control.py',
        'from': 'request_timeout = 0.1',
        'to': 'request_timeout = 1'
    },
]
