import graphene

import goods.schema
import category.schema


class Query(goods.schema.Query, category.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)