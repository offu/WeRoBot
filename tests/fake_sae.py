#!/usr/bin/env python
"""
Fake client for sae kvdb service.

This should give you a feel for how this module operates::

    import kvdb
    kv = kvdb.KVClient()

    kv.set("some_key", "Some value")
    value = kv.get("some_key")

    kv.set("another_key", 3)
    kv.delete("another_key")
"""

import sys
import os
import six
import time
import re
import pickle

SERVER_MAX_KEY_LENGTH = 250
#  Storing values larger than 1MB requires recompiling memcached.  If you do,
#  this value can be changed by doing "memcache.SERVER_MAX_VALUE_LENGTH = N"
#  after importing this module.
SERVER_MAX_VALUE_LENGTH = 1024 * 1024


class _Error(Exception):
    pass


class _ConnectionDeadError(Exception):
    pass


class _CacheEntry(object):
    def __init__(self, value, flags, expiration):
        self.value = value
        self.flags = flags
        self.created_time = time.time()
        self.will_expire = expiration != 0
        self.locked = False
        self._set_expiration(expiration)

    def _set_expiration(self, expiration):
        if expiration > (86400 * 30):
            self.expiration = expiration
        else:
            self.expiration = self.created_time + expiration

    def is_expired(self):
        return self.will_expire and time.time() > self.expiration


class local(object):
    pass


_DEAD_RETRY = 30  # number of seconds before retrying a dead server.
_SOCKET_TIMEOUT = 3  # number of seconds before sockets timeout.

_cache = {}


class Client(local):
    """
    Object representing a pool of memcache servers.

    See L{memcache} for an overview.

    In all cases where a key is used, the key can be either:
        1. A simple hashable type (string, integer, etc.).
        2. A tuple of C{(hashvalue, key)}.  This is useful if you want to avoid
        making this module calculate a hash value.  You may prefer, for
        example, to keep all of a given user's objects on the same memcache
        server, so you could use the user's unique id as the hash value.

    @group Setup: __init__, set_servers, forget_dead_hosts, disconnect_all, debuglog
    @group Insertion: set, add, replace, set_multi
    @group Retrieval: get, get_multi
    @group Integers: incr, decr
    @group Removal: delete, delete_multi
    @sort: __init__, set_servers, forget_dead_hosts, disconnect_all, debuglog,\
           set, set_multi, add, replace, get, get_multi, incr, decr, delete, delete_multi
    """
    _FLAG_PICKLE = 1 << 0
    _FLAG_INTEGER = 1 << 1
    _FLAG_LONG = 1 << 2
    _FLAG_COMPRESSED = 1 << 3

    _SERVER_RETRIES = 10  # how many times to try finding a free server.

    # exceptions for Client
    class MemcachedKeyError(Exception):
        pass

    class MemcachedKeyLengthError(MemcachedKeyError):
        pass

    class MemcachedKeyCharacterError(MemcachedKeyError):
        pass

    class MemcachedKeyNoneError(MemcachedKeyError):
        pass

    class MemcachedKeyTypeError(MemcachedKeyError):
        pass

    class MemcachedStringEncodingError(Exception):
        pass

    def __init__(
        self,
        servers=[],
        debug=0,
        pickleProtocol=0,
        pickler=pickle.Pickler,
        unpickler=pickle.Unpickler,
        pload=None,
        pid=None,
        server_max_key_length=SERVER_MAX_KEY_LENGTH,
        server_max_value_length=SERVER_MAX_VALUE_LENGTH,
        dead_retry=_DEAD_RETRY,
        socket_timeout=_SOCKET_TIMEOUT,
        cache_cas=False
    ):
        """
        Create a new Client object with the given list of servers.

        @param servers: C{servers} is passed to L{set_servers}.
        @param debug: whether to display error messages when a server can't be
        contacted.
        @param pickleProtocol: number to mandate protocol used by (c)Pickle.
        @param pickler: optional override of default Pickler to allow subclassing.
        @param unpickler: optional override of default Unpickler to allow subclassing.
        @param pload: optional persistent_load function to call on pickle loading.
        Useful for cPickle since subclassing isn't allowed.
        @param pid: optional persistent_id function to call on pickle storing.
        Useful for cPickle since subclassing isn't allowed.
        @param dead_retry: number of seconds before retrying a blacklisted
        server. Default to 30 s.
        @param socket_timeout: timeout in seconds for all calls to a server. Defaults
        to 3 seconds.
        @param cache_cas: (default False) If true, cas operations will be
        cached.  WARNING: This cache is not expired internally, if you have
        a long-running process you will need to expire it manually via
        "client.reset_cas(), or the cache can grow unlimited.
        @param server_max_key_length: (default SERVER_MAX_KEY_LENGTH)
        Data that is larger than this will not be sent to the server.
        @param server_max_value_length: (default SERVER_MAX_VALUE_LENGTH)
        Data that is larger than this will not be sent to the server.
        """
        local.__init__(self)
        self.debug = debug
        self.cache_cas = cache_cas
        self.reset_cas()

        # Allow users to modify pickling/unpickling behavior
        self.server_max_key_length = server_max_key_length
        self.server_max_value_length = server_max_value_length

        _cache = {}

        self.reset_stats()

    def reset_stats(self):
        self._get_hits = 0
        self._get_misses = 0
        self._cmd_set = 0
        self._cmd_get = 0

    def reset_cas(self):
        """
        Reset the cas cache.  This is only used if the Client() object
        was created with "cache_cas=True".  If used, this cache does not
        expire internally, so it can grow unbounded if you do not clear it
        yourself.
        """
        self.cas_ids = {}

    def set_servers(self, servers):
        """
        Set the pool of servers used by this client.

        @param servers: an array of servers.
        Servers can be passed in two forms:
            1. Strings of the form C{"host:port"}, which implies a default weight of 1.
            2. Tuples of the form C{("host:port", weight)}, where C{weight} is
            an integer weight value.
        """
        pass

    def get_info(self, stat_args=None):
        '''Get statistics from each of the servers.

        @param stat_args: Additional arguments to pass to the memcache
            "stats" command.

        @return: A list of tuples ( server_identifier, stats_dictionary ).
            The dictionary contains a number of name/value pairs specifying
            the name of the status field and the string value associated with
            it.  The values are not converted from strings.
        '''

        info = {
            'outbytes': 41,
            'total_size': 22,
            'inbytes': 62,
            'set_count': 16,
            'delete_count': 0,
            'total_count': 4,
            'get_count': 11
        }

        return info

    def debuglog(self, str):
        if self.debug:
            sys.stderr.write("MemCached: %s\n" % str)

    def forget_dead_hosts(self):
        """
        Reset every host in the pool to an "alive" state.
        """
        pass

    def disconnect_all(self):
        pass

    def delete(self, key):
        '''Deletes a key from the memcache.

        @return: Nonzero on success.
        '''
        if key not in _cache:
            return False
        del _cache[key]
        return True

    def add(self, key, val, time=0, min_compress_len=0):
        '''
        Add new key with value.

        Like L{set}, but only stores in memcache if the key doesn't already exist.

        @return: Nonzero on success.
        @rtype: int
        '''
        return self._set("add", key, val, time, min_compress_len)

    def replace(self, key, val, time=0, min_compress_len=0):
        '''Replace existing key with value.

        Like L{set}, but only stores in memcache if the key already exists.
        The opposite of L{add}.

        @return: Nonzero on success.
        @rtype: int
        '''
        return self._set("replace", key, val, time, min_compress_len)

    def set(self, key, val, time=0, min_compress_len=0):
        '''Unconditionally sets a key to a given value in the memcache.

        The C{key} can optionally be an tuple, with the first element
        being the server hash value and the second being the key.
        If you want to avoid making this module calculate a hash value.
        You may prefer, for example, to keep all of a given user's objects
        on the same memcache server, so you could use the user's unique
        id as the hash value.

        @return: Nonzero on success.
        @rtype: int
        @param time: Tells memcached the time which this value should expire, either
        as a delta number of seconds, or an absolute unix time-since-the-epoch
        value. See the memcached protocol docs section "Storage Commands"
        for more info on <exptime>. We default to 0 == cache forever.
        @param min_compress_len: The threshold length to kick in auto-compression
        of the value using the zlib.compress() routine. If the value being cached is
        a string, then the length of the string is measured, else if the value is an
        object, then the length of the pickle result is measured. If the resulting
        attempt at compression yeilds a larger string than the input, then it is
        discarded. For backwards compatability, this parameter defaults to 0,
        indicating don't ever try to compress.
        '''
        return self._set("set", key, val, time, min_compress_len)

    def _set(self, cmd, key, val, time, min_compress_len=0):
        self.check_key(key)

        self._cmd_set += 1

        key_exists = key in _cache

        if (
            (cmd == 'add' and key_exists)
            or (cmd == 'replace' and not key_exists)
            or (cmd == 'prepend' and not key_exists)
            or (cmd == 'append' and not key_exists)
        ):
            return False

        if cmd == 'prepend':
            new_val = val + _cache[key].value
        elif cmd == 'append':
            new_val = _cache[key].value + val
        else:
            new_val = val

        _cache[key] = _CacheEntry(new_val, 0, time)
        return True

    def _get(self, cmd, key):
        self.check_key(key)

        self._cmd_get += 1

        if key in _cache:
            entry = _cache[key]
            if not entry.is_expired():
                self._get_hits += 1
                return entry.value
        self._get_misses += 1
        return None

    def get(self, key):
        '''Retrieves a key from the memcache.

        @return: The value or None.
        '''
        return self._get('get', key)

    def get_multi(self, keys, key_prefix=''):
        '''
        Retrieves multiple keys from the memcache doing just one query.

        >>> success = mc.set("foo", "bar")
        >>> success = mc.set("baz", 42)
        >>> mc.get_multi(["foo", "baz", "foobar"]) == {"foo": "bar", "baz": 42}
        1

        get_mult [ and L{set_multi} ] can take str()-ables like ints / longs as keys too. Such as your db pri key fields.
        They're rotored through str() before being passed off to memcache, with or without the use of a key_prefix.
        In this mode, the key_prefix could be a table name, and the key itself a db primary key number.

        This method is recommended over regular L{get} as it lowers the number of
        total packets flying around your network, reducing total latency, since
        your app doesn't have to wait for each round-trip of L{get} before sending
        the next one.

        See also L{set_multi}.

        @param keys: An array of keys.
        @param key_prefix: A string to prefix each key when we communicate with memcache.
            Facilitates pseudo-namespaces within memcache. Returned dictionary keys will not have this prefix.
        @return:  A dictionary of key/value pairs that were available. If key_prefix was provided, the keys in the retured dictionary will not have it present.

        '''
        retval = {}
        for e in keys:
            _key = key_prefix + str(e)
            val = self._get('get', _key)
            if val is not None:
                retval[e] = val
        return retval

    def get_by_prefix(
        self, prefix, limit=None, max_count=None, marker=None, start_key=None
    ):
        '''
        >>> success = mc.set('k1', 1)
        >>> success = mc.set('k2', 2)
        >>> success = mc.set('xyz', 'xxxxxxx')
        >>> mc.get_by_prefix('k') == [('k2', 2), ('k1', 1)]
        1

        '''
        start_key = marker or start_key
        max_count = limit or max_count or 100

        ignore = False
        if start_key is not None:
            ignore = True

        for k, e in _cache.items():
            if ignore:
                if k == start_key:
                    ignore = False
                continue

            if e.is_expired():
                continue

            if max_count <= 0: break

            if str(k).startswith(prefix):
                max_count -= 1
                yield k, e.value

    def getkeys_by_prefix(
        self, prefix, limit=None, max_count=None, marker=None, start_key=None
    ):
        max_count = limit or max_count
        marker = marker or start_key
        kv = self.get_by_prefix(prefix, max_count, marker=marker)
        return [e[0] for e in kv]

    def check_key(self, key, key_extra_len=0):
        """Checks sanity of key.  Fails if:
            Key length is > SERVER_MAX_KEY_LENGTH (Raises MemcachedKeyLength).
            Contains control characters  (Raises MemcachedKeyCharacterError).
            Is not a string (Raises MemcachedStringEncodingError)
            Is an unicode string (Raises MemcachedStringEncodingError)
            Is not a string (Raises MemcachedKeyError)
            Is None (Raises MemcachedKeyError)
        """
        if isinstance(key, tuple): key = key[1]
        if not key:
            raise Client.MemcachedKeyNoneError("Key is None")
        if six.PY2:
            if isinstance(key, six.text_type):
                raise Client.MemcachedStringEncodingError(
                    "Keys must be str()'s, not unicode.  Convert your unicode "
                    "strings using mystring.encode(charset)!"
                )
        if not isinstance(key, str):
            raise Client.MemcachedKeyTypeError("Key must be str()'s")

        if isinstance(key, str):
            if self.server_max_key_length != 0 and \
                                    len(key) + key_extra_len > self.server_max_key_length:
                raise Client.MemcachedKeyLengthError(
                    "Key length is > %s" % self.server_max_key_length
                )
            for char in key:
                if ord(char) < 33 or ord(char) == 127:
                    raise Client.MemcachedKeyCharacterError(
                        "Control characters not allowed"
                    )


KVClient = Client


def _doctest():
    import doctest
    import werobot.tests.fake_sae as kvdb
    servers = ["127.0.0.1:11211"]
    mc = Client(servers, debug=1)
    globs = {"mc": mc}
    return doctest.testmod(kvdb, globs=globs)


if __name__ == "__main__":
    failures = 0
    print("Testing docstrings...")
    _doctest()
    print("Running tests:")
    print()
    serverList = [["127.0.0.1:11211"]]
    if '--do-unix' in sys.argv:
        serverList.append([os.path.join(os.getcwd(), 'memcached.socket')])

    for servers in serverList:
        mc = KVClient(servers, debug=1)

        def to_s(val):
            if not isinstance(val, str):
                return "%s (%s)" % (val, type(val))
            return "%s" % val

        def test_setget(key, val):
            global failures
            print("Testing set/get {'%s': %s} ..." % (to_s(key), to_s(val)))
            mc.set(key, val)
            newval = mc.get(key)
            if newval == val:
                print("OK")
                return 1
            else:
                print("FAIL")
                failures = failures + 1
                return 0

        class FooStruct(object):
            def __init__(self):
                self.bar = "baz"

            def __str__(self):
                return "A FooStruct"

            def __eq__(self, other):
                if isinstance(other, FooStruct):
                    return self.bar == other.bar
                return 0

        test_setget("a_string", "some random string")
        test_setget("an_integer", 42)
        if test_setget("long", int(1 << 30)):
            print("Testing delete ...")
            if mc.delete("long"):
                print("OK")
            else:
                print("FAIL")
                failures = failures + 1
            print("Checking results of delete ...")
            if mc.get("long") == None:
                print("OK")
            else:
                print("FAIL")
                failures = failures + 1
        print("Testing get_multi ...")
        print(mc.get_multi(["a_string", "an_integer"]))

        #  removed from the protocol
        # if test_setget("timed_delete", 'foo'):
        #    print "Testing timed delete ...",
        #    if mc.delete("timed_delete", 1):
        #        print "OK"
        #    else:
        #        print "FAIL"; failures = failures + 1
        #    print "Checking results of timed delete ..."
        #    if mc.get("timed_delete") == None:
        #        print "OK"
        #    else:
        #        print "FAIL"; failures = failures + 1

        print("Testing get(unknown value) ...")
        print(to_s(mc.get("unknown_value")))

        f = FooStruct()
        test_setget("foostruct", f)

        # print "Testing incr ...",
        # x = mc.incr("an_integer", 1)
        # if x == 43:
        #    print "OK"
        # else:
        #    print "FAIL"; failures = failures + 1

        # print "Testing decr ...",
        # x = mc.decr("an_integer", 1)
        # if x == 42:
        #    print "OK"
        # else:
        #    print "FAIL"; failures = failures + 1
        sys.stdout.flush()

        # sanity tests
        print("Testing sending spaces...")
        sys.stdout.flush()
        try:
            x = mc.set("this has spaces", 1)
        except Client.MemcachedKeyCharacterError as msg:
            print("OK")
        else:
            print("FAIL")
            failures = failures + 1

        print("Testing sending control characters...")
        try:
            x = mc.set("this\x10has\x11control characters\x02", 1)
        except Client.MemcachedKeyCharacterError as msg:
            print("OK")
        else:
            print("FAIL")
            failures = failures + 1

        print("Testing using insanely long key...")
        try:
            x = mc.set('a' * SERVER_MAX_KEY_LENGTH, 1)
        except Client.MemcachedKeyLengthError as msg:
            print("FAIL")
            failures = failures + 1
        else:
            print("OK")
        try:
            x = mc.set('a' * SERVER_MAX_KEY_LENGTH + 'a', 1)
        except Client.MemcachedKeyLengthError as msg:
            print("OK")

db_file = os.environ.get('sae.kvdb.file')
if db_file:
    import pickle

    def _save_cache():
        # XXX: reloader should not do this
        if not os.environ.get('sae.run_main'): return
        try:
            pickle.dump(_cache, open(db_file, 'wb'))
        except Exception as e:
            print("save kvdb to '%s' failed: %s" % (db_file, str(e)))

    def _restore_cache():
        try:
            _cache.update(pickle.load(open(db_file, 'rb')))
        except Exception as e:
            print("load kvdb from '%s' failed: %s" % (db_file, str(e)))

    import atexit

    atexit.register(_save_cache)
    _restore_cache()
