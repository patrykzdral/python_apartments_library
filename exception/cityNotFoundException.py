class CityNotFoundException(Exception):
    def __init__(self, message):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        #self.errors = errors