from django.shortcuts import render, get_object_or_404
from django.views.generic.list import ListView
from blog.models import Post, PostImage, PostFile
from django.views.generic.detail import DetailView
from blog.forms import PostingForm
from django.views.generic.edit import FormView
from django.http.response import HttpResponseRedirect, HttpResponseNotAllowed
from audioop import reverse

#제네릭뷰: 장고에서 제공하는 여러가지 뷰 기능을 구현한 클래스모음
#ListView : 특정 모델클래스의 객체들을 목록화할 수 있는 기능이 구현된 뷰
# 글목록이 뜨는 페이지
class Main(ListView):
    #사용자에게 전달할 HTML 파일의 경로
    template_name = 'blog/main.html'
    #리스트로 뽑을 모델클래스
    model = Post
    #리스트로 추출한 객체를 HTML에 전달할 때 사용할 이름
    context_object_name = 'list'
    #한페이지에 몇개의 객체가 보여질지 설정
    paginate_by = 5
#글 상세보기 페이지
#DetailView : 특정 모델클래스의 특정 객체 한개를 추출할때 사용하는 뷰
class Detail(DetailView):
     #사용자에게 전달할 HTML 파일의 경로
    template_name = 'blog/detail.html'
    #리스트로 뽑을 모델클래스
    model = Post
    #리스트로 추출한 객체를 HTML에 전달할 때 사용할 이름
    context_object_name = 'obj'
#글 작성 페이지
from django.contrib.auth.mixins import LoginRequiredMixin
class Posting(LoginRequiredMixin, FormView):
    template_name='blog/posting.html'
    form_class = PostingForm
    def form_valid(self,form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        for f in self.request.FILES.getlist('files'):
            pf = PostFile()
            pf.post = p
            pf.file = f
            pf.save()
        for i in self.request.FILES.getlist('images'):
            pi = PostImage()
            pi.post = p
            pi.image = i
            pi.save()
            return HttpResponseRedirect(reverse('blog:detail',args=(p.id,)))
        
def post_delete(request, p_id):
    p = get_object_or_404(Post, id=p_id)
    if p.user == request.user:
        p.delete()
        return HttpResponseRedirect(reverse('blog.main'))
    else:
        return HttpResponseNotAllowed()