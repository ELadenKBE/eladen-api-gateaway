import graphene

import goods.schema
import category.schema
import users.schema
import orders.schema
import goods_list.schema


class Query(users.schema.Query,
            goods.schema.Query,
            category.schema.Query,
            orders.schema.Query,
            goods_list.schema.Query,
            graphene.ObjectType):
    pass


class Mutation(goods.schema.Mutation,
               users.schema.Mutation,
               category.schema.Mutation,
               goods_list.schema.Mutation,
               graphene.ObjectType,):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
