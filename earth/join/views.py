from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *
from rest_framework import status
from django.shortcuts import get_object_or_404, redirect
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import generics

#튜토리얼 뷰
class TutorialView(APIView):
    permission_class = [IsAuthenticated]

    # 유저의 튜토리얼 상태 확인 (0인지 1인지)
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user = request.user)
        serializer = TutorialSerializer(profile)
        return Response(serializer.data)
    
    # 튜토리얼을 완료했음을 알리는 요청
    def post(self, request):
        profile, created = UserProfile.objects.get_or_create(user = request.user)
        serializer = TutorialSerializer(profile, data=request.data, partial=True) # data전달 필요, 인스턴스 자체를 전달하면 안됨.
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 카드작성뷰, 튜토리얼 완료못한 사람은 무조건 튜토리얼 끝낸 후 작성가능 /join/card_post/
class CardPostView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 사용자 프로필에서 튜토리얼 완료 여부 확인
        profile, created =  UserProfile.objects.get_or_create(user = request.user)

        if not profile.tutorial_completed:
            return Response({"message": "튜토리얼을 완료해야 카드 작성이 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = CardPostSerializer(data = request.data)
        if serializer.is_valid():
            card_post = serializer.save(author=request.user)  # 카드 포스트 저장
            card_post_id = card_post.id

            # '이미지' URL 생성
            image_url = request.build_absolute_uri(card_post.image.url)

            return Response({
                "card_post_id" : card_post_id,
                "image_url" : image_url, # 인스타그램 공유를 위한 이미지 URL
                "message": "카드가 성공적으로 작성되었습니다.",
                "redirect_url": "/join/frame_selection/"
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# 프레임 선택 페이지 뷰 /join/frame_selection/
class FrameSelection(APIView):
    permission_classes = [IsAuthenticated]

    # 유저가 프레임을 골랐는지 확인
    def get(self, request):
        cardpost_id = request.query_params.get("cardpost_id")  # cardpost_id를 쿼리 파라미터로 받아옴
        cardpost = get_object_or_404(CardPost, id=cardpost_id)

        frame, created = Frame.objects.get_or_create(user=request.user, cardpost=cardpost)
        serializer = FrameSerializer(frame)
        return Response(serializer.data)
    
    # 프레임 고르면
    def post(self, request):
        cardpost_id = request.data.get("cardpost_id")  # request body1
        cardpost = get_object_or_404(CardPost, id=cardpost_id)

        frame, created = Frame.objects.get_or_create(user = request.user, cardpost=cardpost)
        serializer = FrameSerializer(frame, data=request.data)
        
        # 프레임 선택 완료여부 판별
        if not serializer.initial_data.get('frame_completed', False): # request body2
            return Response({"message": "프레임 선택해야 카드 작성이 가능합니다."}, status=status.HTTP_403_FORBIDDEN)
        
        # 데이터 유효성 검사
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "프레임 잘 골랐습니다.",
                "redirect_url": "/join/completed/"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#----------------------실천카드 완성-----------------------
# 이미지 저장단계 /join/completed/
class CompletedView(APIView):
    permission_classes = [IsAuthenticated]

    # 이미지 저장됐는지 상태확인
    def get(self, request):
        # 사용자가 만든 카드 포스트와 관련된 이미지를 가져옴
        photos = Photo.objects.filter(card_post__author=request.user)
        serializer = PhotoSerializer(photos, many=True)
        points = request.user.points
        return Response({"points":points,"message": "완성된 이미지가 저장되었습니다..", "images": serializer.data})
    
    # 이미지 저장 메서드
    def post(self, request):
        card_post_id = request.data.get('card_post_id')
        if not card_post_id:
            return Response({"message": "card_post_id가 필요합니다."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            card_post = CardPost.objects.get(id=card_post_id, author=request.user)
        except CardPost.DoesNotExist:
            return Response({"message": "해당 카드 포스트가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
        # `decorated_image` 필드를 통해 이미지 저장
        serializer = PhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.save(card_post=card_post)
            # 포인트 추가 및 저장
            request.user.points += photo.point
            request.user.save()
            return Response({
                "message": "이미지가 저장되었습니다.",
                "image_url": photo.decorated_image.url  # S3 URL 반환
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Instagram 스토리 공유
class ImageShareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, image_id):
        try:
            card_post = CardPost.objects.get(id=image_id, author=request.user)
            serializer = ImageShareSerializer(data=request.data)

            # Instagram 스토리 링크 생성 / 여기서 발급받은 포인트는 completed/에 쌓인다.
            image_url = request.build_absolute_uri(card_post.image.url)
            # 인스타그램 스토리 URL 스킴 생성 (Android용 intent URL) *iOS의 경우, instagram://story 스킴을 사용
            instagram_share_url = f"https://www.instagram.com/create/story?background_image_url={image_url}"
            
            if serializer.is_valid():
                share = serializer.save(card_post=card_post)
                # 포인트 지급 (공유 시에만)
                request.user.points += share.point
                request.user.save()

                return Response({
                    "message": "포인트 지급완료",
                    "instagram_share_url": instagram_share_url  # 공유 링크 포함
                }, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except CardPost.DoesNotExist:
            return Response({"message": "해당 이미지가 존재하지 않거나 권한이 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        
# 키워드 정렬 >> 데이터베이스에 저장된 CardPost 객체들을 목록 형태로 보여줌. *인증된 사용자만 조회가능*
class PostListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardPostSerializer

    def get_queryset(self):
        user = self.request.user
        qs = CardPost.objects.filter(author=user)

        # URL 경로 파라미터로 전달된 category_id 받아오기
        category_id = self.kwargs.get('category_id', None)

        if category_id is not None:
            try:
                selected_keyword = CardPost.KEYWORD_CHOICES[category_id][0]
                qs = qs.filter(keyword=selected_keyword) # 키워드 기준으로 필터링
            except IndexError:
                qs = CardPost.objects.none()
        return qs