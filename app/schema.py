import graphene

import goods.schema


class Query(goods.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)