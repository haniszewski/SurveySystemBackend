from marshmallow import Schema, fields, validate


class AllQuestionAnalysisSchema(Schema):
    type = fields.Str(validate=validate.OneOf(['percentage']))
    display = fields.Str(validate=validate.OneOf(['percentage', 'count']))
    show_total = fields.Bool()
    min_score = fields.Integer(required=False)

class BasicQuestionAnalysisSchema(Schema):
    order = fields.Integer(required=True)
    type = fields.Str(validate=validate.OneOf(['percentage']))
    display = fields.Str(validate=validate.OneOf(['percentage', 'count']))
    show_total = fields.Bool()
    min_score = fields.Integer(required=False)

class RootAnalysisSchema(Schema):
    all_questions = fields.Nested(AllQuestionAnalysisSchema, required=False)
    basic = fields.List(fields.Nested(BasicQuestionAnalysisSchema), required=True)
