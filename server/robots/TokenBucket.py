from time import time
from threading import RLock

__all__ = ("TokenBucket", )


class TokenBucket(object):
    def __init__(self, tokens, fill_rate):
        self.capacity = float(tokens)
        self._tokens = float(tokens)
        self.fill_rate = float(fill_rate)
        self.timestamp = time()

    def consume(self, tokens):
        if tokens <= self.tokens:
            self._tokens -= tokens
        else:
            return False
        return True

    def get_tokens(self):
        if self._tokens < self.capacity:
            now = time()
            delta = self.fill_rate * (now - self.timestamp)
            self._tokens = min(self.capacity, self._tokens + delta)
            self.timestamp = now
        return self._tokens
    tokens = property(get_tokens)


'''if __name__ == '__main__':
    from time import sleep
    bucket = TokenBucket(1000, 100)
    print "tokens =", bucket._tokens
    print "consume(10) =", bucket.consume(800)
    print "consume(10) =", bucket.consume(10)
    sleep(0.5)
    print "tokens =", bucket.tokens
    sleep(1)
    print "tokens =", bucket.tokens
    print "consume(90) =", bucket.consume(90)
    print "tokens =", bucket.tokens
    sleep(10)
    print "tokens =", bucket.tokens'''