# aldo
Inject dependencies on python 3 functions, methods and classes using type hint:

    @aldo
    def my_func(foo: Foo):
        return foo
    
Calling my_func without parameters will be handled using aldo dependency manager.

You can also "teach" aldo how to create an instance of a class (or subclass):

    @aldo
    def my_view(cache: Cache):
        return cache.get('key')
    
    @teach
    def cache_factory(*args, **kwargs):
        return RedisCache()
        
    
    my_view()
