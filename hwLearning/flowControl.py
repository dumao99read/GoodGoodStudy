next_step_true = 'true'
next_step_false = 'false'
next_step_column_n = 'next_column_n'
class Step(object):
    def __int__(self, func, *args, call=None, call_end=None, next_true=None, next_false=None, next_column_n=None):
        self.func = func
        self.args = args
        self.call = call
        self.call_end = call_end
        self.next = {
            next_step_true: next_true,
            next_step_false: next_false,
            next_step_column_n: next_column_n
        }

    def start(self):
        result = self.func(*self.args)

        if self.call is not None:
            self.call(result)

        if result in self.next and self.next[result]:
            s = self.next[result]
            return s.start()

        if self.call_end is not None:
            self.call_end(result)
            return result

