
def gen_fn():
    result = yield 1
    print('result of yield: {}'.format(result))
    result2 = yield 2
    print('result of 2nd yield: {}'.format(result2))
    return 'done'


gen = gen_fn()
gen.send(None)
gen.send('hello')
gen.send('goodbye')