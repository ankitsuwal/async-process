class CustomErrors(Exception):
    def __init__(self, error, msg, status_code):
        super().__init__()
        self.msg = msg
        self.status_code = status_code
        print("-"*25, "ERROR", "-"*25)
        print(str(error))
        print("\nyou are in exception" * 3)

    def to_dict(self):
        rv = {"message": self.msg, "status": "error"}, self.status_code
        print("\n You are in to_dict of exception." * 3)
        print(rv)
        return rv
