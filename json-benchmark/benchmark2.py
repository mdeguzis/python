'''cjson, jsonlib, simplejson, and yajl also use C code
demjson did not use C code, but was too painfully slow to benchmark
(took about 20 seconds for these tests)
'''
import json
import sys
import time

with open('doc.json') as f:
    decoded = f.read()
encoded = json.loads(decoded)

def test_encodes(modules):    
    encode_times = {}
    
    for json_module in modules:
        start = time.clock()
    
        for _ in xrange(10000):
            json_module.loads(decoded)

        total_time = time.clock() - start
        assert json_module.loads(decoded) == encoded
        encode_times[json_module.__name__] = total_time
    return encode_times

def test_decodes(modules):
    decode_times = {}

    for json_module in modules:
        start = time.clock()

        for _ in xrange(10000):
            json_module.dumps(encoded)

        total_time = time.clock() - start
        assert json.loads(json_module.dumps(encoded)) == encoded
        decode_times[json_module.__name__] = total_time
    return decode_times

def printer(mapping):
    ''' mapping maps module name to time'''
    for k, v in mapping.iteritems():
        print '%s: %ss' % (k, v)


def main():
    print 'JSON Benchmark'
    try:
        import __pypy__
    except ImportError:
        # we are using CPython
        print sys.version
        import cjson, jsonlib, simplejson, ujson, yajl

        jsonlib.loads = jsonlib.read
        jsonlib.dumps = jsonlib.write
        cjson.loads = cjson.decode
        cjson.dumps = cjson.encode
        
        modules = [cjson, json, jsonlib, simplejson, ujson, yajl]
    else:
        # we are using PyPy
        print sys.version
        modules = [json]
    print '-----------------------------'
    print 'ENCODING'
    printer(test_encodes(modules))
    print ''
    print 'DECODING'
    printer(test_decodes(modules))

if __name__ == '__main__':
    main()
