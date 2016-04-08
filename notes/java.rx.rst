================================================================================
Introduction to Java.Rx
================================================================================

https://github.com/ReactiveX/RxJava/wiki
http://xgrommx.github.io/rx-book/why_rx.html
http://reactivex.io/documentation/observable.html
http://www.introtorx.com/content/v1.0.10621.0/

--------------------------------------------------------------------------------
ReactiveX
--------------------------------------------------------------------------------

ReactiveX is a library for composing asynchronous and event-based programs by
using observable sequences. It is basically an extension of the *observer* design
pattern.

.. code-block:: java

                      single item         multiple items
    ---------------------------------------------------------------
    synchronous    T getData()            Iterable<T> getData()
    asynchronous   Future<T> getData()    Observable<T> getData()

The `Observable` can be seen as the dual of the `Iterable`:

.. code-block:: java

       event          Iterable(pull)        Observable(push)
    ---------------------------------------------------------------
    retrieve data     T next()               onNext(T)
    discover error    throws Exception       onError(Exception)
    complete          !hasNext()             onComplete()

--------------------------------------------------------------------------------
ReactiveX Single
--------------------------------------------------------------------------------

To represent a single result instead of a collection of results, the reactive
team introduced an observable *either* called `Single`. It only has two methods
and the contract states that one of the methods will be called and it will be
called only once. After that the subscription is terminated.

.. code-block:: java

    interface Single<T> {
        void onSuccess(T t);
        void onError(Exception e);
    }
