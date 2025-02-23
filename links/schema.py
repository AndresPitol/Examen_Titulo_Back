import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from links.models import Link, Vote

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

# Add after the LinkType
class VoteType(DjangoObjectType):
    class Meta:
        model = Vote


class Query(graphene.ObjectType):
    links = graphene.List(LinkType)
    votes = graphene.List(VoteType)

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    nombre = graphene.String()
    marca = graphene.String()
    precio = graphene.String()
    descripcion = graphene.String()
    posted_by = graphene.Field(UserType)

    #2
    class Arguments:
     nombre = graphene.String()
     marca = graphene.String()
     precio = graphene.String()
     descripcion = graphene.String()

    #3
    def mutate(self, info, nombre, marca, precio, descripcion):
        user = info.context.user or None

        link = Link(
            nombre=nombre, 
            marca=marca,
            precio=precio,
            descripcion=descripcion,
            posted_by=user)

        link.save()

        return CreateLink(
            id=link.id,
            nombre=link.nombre,
            marca=link.marca,
            precio=link.precio,
            descripcion=link.descripcion,
            posted_by=user
        )

# Add the CreateVote mutation
class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()
        
    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('You must be logged to vote!')

        link = Link.objects.filter(id=link_id).first()
        if not link:
            raise Exception('Invalid Link!')

        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)




#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()

