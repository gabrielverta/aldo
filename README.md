# aldo
Inject dependencies on python 3 functions, methods and classes using type hint:

    @aldo
    def my_func(foo: Foo):
        return foo
    
Calling my_func without parameters will be handled using aldo dependency manager.

You can also "teach" aldo how to create an instance of a class (or subclass):

    @teach(Cache)
    def cache_factory(*args, **kwargs):
        return RedisCache()
        
    @aldo
    def my_view(cache: Cache):
        return cache
    >>> my_view()
    <RedisCache>

## aldo for django
Aldo was teached for some tricks in django, so you can use a view like this:

### urls.py
    url(r'^(?P<question_id>[0-9]+)/$', views.show),
    
### views.py
    @aldo
    def show(request, poll: models.Poll):
        return HttpResponse(poll.question_text)
        
Aldo knows that when you have a Model, he can use "MODELNAME_FIELD" kwarg (the name of the field used in uri regular expression) to query database for an instance of it.

Aldo also knows how to use forms.Form and forms.ModelForm:

### urls.py
    url(r'^store/$', views.store),
    
### views.py
    @aldo
    def store(request, form: forms.QuestionForm):
        return HttpResponse(form.data)

Here we have two cases:

* **GET** request: initial data is filled with request.GET, aka. forms.QuestionForm(initial=request.GET)
* **POST** request: form is filled with request.POST, aka. forms.QuestionForm(request.POST). In this case aldo also verify if form is valid, otherwise it redirects the request back to HTTP_REFERER, sending request.POST data back. You can use it like this:

### urls.py
    url(r'^create/$', views.create),
    url(r'^store/$', views.store, {'method': 'POST'}), # user can not access it without a POST
    
### views.py
    @aldo
    def create(request, form: forms.QuestionForm):
        return render(request, 'polls/create.html', locals())
    
    @aldo
    def store(request, form: forms.QuestionForm):
        form.save()
        return redirect('/polls')
