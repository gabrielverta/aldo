# aldo
Inject dependencies on python 3 functions, methods and classes using typehint:

    @aldo
    def my_func(foo: Foo):
        return foo
    
Calling my_func without parameters will be handled using aldo dependency manager.

You can also bind classes to "teach" aldo how to instanciate a new class of specific type:

    def my_view(cache: Cache):
        return cache.get('key')
        
    def create_cache_instance(*args, **kwargs):
        return RedisCache()
        
    aldo = Aldo(other_func)
    aldo.bind(Cache, create_cache_intance)
    aldo()
    
