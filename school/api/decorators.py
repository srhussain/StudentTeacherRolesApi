from rest_framework.response import Response

def unauthenticated_user(view_func):
    def wrapper_func(request,*args,**kwargs):
        if request.user.is_authenticated:
            return Response({'message':"Done"})
        else:
            return view_func(request,*args,**kwargs)
    return wrapper_func

def allowed_teachers(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request,*args,**kwargs):

            group=None
            print("hello")
            if request.user.groups.exists():
                group=request.user.groups.all()[0].name
            print("Bye")
            if group in allowed_roles:
                return view_func(request,*args,**kwargs)
            else:
                return Response({
                    'message':"You are not authorised to view this page"
                })
        print("compl")
        return wrapper_func
    return decorator