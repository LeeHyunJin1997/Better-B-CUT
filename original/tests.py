from rest_framework.test import APITestCase
from django.urls import reverse

# Create your tests here.

class originalAPITest(APITestCase):
    # original 목록 조회 | GET: /api/v1/original
    def test_original_get_success(self):
        # client.login(username='lauren', password='secret')
        # client.logout()
        # client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        # response = self.client.get('/api/v1/original/')
        url = reverse('original:create_or_list_original')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # original 작성 | POST: /api/v1/original
    # 로그인 필요 | 제목 작성하지 않았을 때 | 대본, 스토리 여부 선택하지 않았을 때
    def test_original_post_success(self):
        url = reverse('original:create_or_list_original')
        data = {
            'type': 'Story',
            'title': '시그널',
            'content': '과거와 무전하는 형사의 이야기'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    # original 상세 조회 | GET: /api/v1/original/<int:original_id>
    # original_id가 비어있을 때 | original_id에 해당하는 게시글이 없을 때

    # original 수정 | PUT: /api/v1/original/<int:original_id>
    # 로그인 필요 | 본인 게시글 아닐 때 | title 작성하지 않았을 때 | 대본, 스토리 여부 선택하지 않았을 때

    # original 삭제 | DELETE: /api/v1/original/<int:original_id>
    # 로그인 필요 | 본인 게시글 아닐 때

    # original like 추가 | POST: /api/v1/original/<int:original_id>/like
    # 로그인 필요 | 이미 좋아요 되어있을 때

    # original like 삭제 | DELETE: /api/v1/original/<int:original_id>/like
    # 로그인 필요 | 좋아요 되어있지 않을 때

    # comment 목록 조회 | GET: /api/v1/original/<int:original_id>/comment
    
    # comment 작성 | POST: /api/v1/original/<int:original_id>/comment
    # 로그인 필요 | content 작성하지 않았을 때

    # comment 수정 | PUT: /api/v1/original/<int:original_id>/comment/<int:original_comment_id>
    # 로그인 필요 | 본인 댓글 아닐 때 | content 작성하지 않았을 때

    # comment 삭제 | DELETE: /api/v1/original/<int:original_id>/comment/<int:original_comment_id>
    # 로그인 필요 | 본인 댓글 아닐 때

    # comment like 추가 | POST: /api/v1/original/<int:original_id>/comment/<int:original_comment_id>/like
    # 로그인 필요 | 이미 좋아요 되어있을 때

    # comment like 삭제 | DELETE:/api/v1/original/<int:original_id>/comment/<int:original_comment_id>/like
    # 로그인 필요 | 좋아요 되어있지 않을 때
