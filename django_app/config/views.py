"""
Main index
첫 화면
"""

from django.shortcuts import redirect


def index(request):
    """
    1. If patient user is signed in and haven't submitted today's survey, redirect to survey page.
    2. If patient user is signed in and submitted today's survey, redirect to results page.
    3. If researcher user is signed in, redirect to progress page.
    4. If developer user is signed in, redirect to management page.
    5. If user isn't signed in, redirect to sign-in page.
    1. 환자 유저가 로그인했고 오늘의 설문조사를 작성하지 않았다면, 설문조사 페이지로 이동한다.
    2. 환자 유저가 로그인했고 오늘의 설문조사를 작성했다면, 결과 페이지로 이동한다.
    3. 연구자 유저가 로그인하면, 진행도 페이지로 이동한다.
    4. 개발자 유저가 로그인하면, 관리 페이지로 이동한다.
    5. 로그인된 유저가 없으면, 로그인 페이지로 이동한다.
    """
    if request.user.is_authenticated:
        return redirect('survey:today')
    elif request.user.is_authenticated:
        return redirect('result:today')
    elif request.user.is_authenticated:
        return redirect('manage:progress')
    elif request.user.is_authenticated:
        return redirect('manage:index')
    else:
        return redirect('member:signin')
