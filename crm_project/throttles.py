from django.core.cache import cache
from ninja_extra.throttling import BaseThrottle

class SimpleRateThrottle(BaseThrottle):
    rate = 5              # ruxsat berilgan requestlar soni
    duration = 60         # vaqt (sekundda) – 1 daqiqa

    def get_cache_key(self, request):
        if request.user.is_authenticated:
            return f"throttle:user:{request.user.id}"
        return f"throttle:ip:{request.client.host}"

    def allow_request(self, request, view):
        key = self.get_cache_key(request)
        current = cache.get(key, 0)

        if int(current) >= self.rate:
            return False

        # Yangi user/request uchun initial qiymat o‘rnatish
        added = cache.add(key, 1, timeout=self.duration)
        if not added:
            cache.incr(key)

        return True
