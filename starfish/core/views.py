

class View:
    def get(self, request, session, *args):
        raise NotImplementedError()

    def post(self, request, session, *args):
        raise NotImplementedError()

    def dispatch(self, request, session, *args):
        if request.command == 'POST':
            return self.post(request, session, *args)
        else:
            return self.get(request, session, *args)
