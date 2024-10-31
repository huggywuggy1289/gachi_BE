from rest_framework.renderers import JSONRenderer

class UserJSONRenderer(JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        # 사용자 관련 JSON 응답 구조를 커스터마이즈
        return super().render({'user': data}, accepted_media_type, renderer_context)
