
from django.http import JsonResponse

from django.shortcuts import redirect

# 需要登录后才能访问的路径
LOGIN_REQUIRED_URLS={
    '/praise/','/criticize/','/excel/','/teachers_data/'
}

def check_login_middleware(get_resp):

    def wrapper(request,*args,**kwargs):
        if request.path in LOGIN_REQUIRED_URLS:
            # 判断是否已经登录
            if 'userid' not in request.session:
                # 判断是否为ajax请求
                if request.is_ajax():
                    return JsonResponse({'code':10003,'hint':'请先登录'})
                else:
                    backurl=request.get_full_path()
                    # 若非ajax请求重定向到登录页
                    return redirect(f'/login/?backurl={backurl}')
        return get_resp(request,*args,**kwargs)
    return wrapper