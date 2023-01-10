class Checkauth():
    def check(self, request, pk):
        if not request.user.pk == pk:
            return True
