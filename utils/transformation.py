class JsonTransformation:
    def __init__(self, json_data):
        self.json_data = json_data

    def filter_fields(self, fields_to_remove):
        for item in self.json_data:
            for field in fields_to_remove:
                if field in item:
                    del item[field]

        return self.json_data
