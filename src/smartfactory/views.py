from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse

from smartfactory.models import SmartSearch
from recommendation.forms import CreateBlogPostForm, UpdateBlogPostForm

from account.models import Account


def create_smart_search_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form

	return render(request, "blog/create_blog.html", context)


def detail_smart_search_view(request, slug):

	context = {}

	blog_post = get_object_or_404(SmartSearch, slug=slug)
	context['blog_post'] = blog_post

	return render(request, 'blog/detail_blog.html', context)



def edit_smart_search_view(request, slug):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect("must_authenticate")

	blog_post = get_object_or_404(SmartSearch, slug=slug)

	if blog_post.author != user:
		return HttpResponse("You are not the author of that post.")

	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=blog_post)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			blog_post = obj
			return render(request, 'blog/edit_blog.html', context)

	form = UpdateBlogPostForm(
			initial = {
					"title": blog_post.title,
					"body": blog_post.body,
					"image": blog_post.image,
			}
		)

	context['form'] = form
	return render(request, 'blog/edit_blog.html', context)


def get_smart_search_queryset(query=None):
	queryset = []
	queries = query.split(" ") # python install 2019 = [python, install, 2019]
	for q in queries:
		posts = SmartSearch.objects.filter(
				Q(title__icontains=q) |
				Q(body__icontains=q)
			).distinct()

		for post in posts:
			queryset.append(post)

	return list(set(queryset))
