from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from django.views import generic
from django.shortcuts import redirect, render

from blog.forms import CommentForm
from blog.models import Post


def index(request: HttpRequest) -> HttpResponse:
    return render(request, "blog/index.html")


class IndexView(generic.ListView):
    model = Post
    context_object_name = "posts"
    template_name = "blog/index.html"
    paginate_by = 5


class PostView(generic.edit.FormMixin, generic.DetailView):
    model = Post
    form_class = CommentForm

    def get_success_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments_count"] = self.object.comments.count()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if not request.user.is_authenticated:
            form.add_error(None, "You must be logged in to comment!")
            return self.form_invalid(form)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.user = request.user
            comment.save()

            return redirect(self.get_success_url())

        return self.form_invalid(form)
