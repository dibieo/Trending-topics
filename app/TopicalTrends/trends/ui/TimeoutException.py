import sys
import signal
 
class TimeoutException(Exception): 
    pass 
 
def timeout(timeout_time, default):
    '''
        a decorator to be used in order to limit the time a function can take
    '''
    def timeout_function(f):
        def f2(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutException()
 
            old_handler = signal.signal(signal.SIGALRM, timeout_handler) 
            signal.alarm(timeout_time) # triger alarm in timeout_time seconds
            try: 
                retval = f(*args, **kwargs)
            except TimeoutException:
                return default
            finally:
                signal.signal(signal.SIGALRM, old_handler) 
            signal.alarm(0)
            return retval
        return f2
    return timeout_function
 