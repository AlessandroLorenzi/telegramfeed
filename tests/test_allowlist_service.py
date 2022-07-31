from telegramfeed import services


class TestAllowListService:
    def setup(self):
        ids = ["123"]
        self.allowlist_service = services.AllowListService(ids)

    def test_is_whitelisted(self):
        assert self.allowlist_service.is_allowed("123") is True

    def test_is_whitelisted_nope(self):
        assert self.allowlist_service.is_allowed("456") is False
