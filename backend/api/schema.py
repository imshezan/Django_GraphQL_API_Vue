from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
import graphene

from api import models

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class AuthorType(DjangoObjectType):
    class Meta:
        model = models.Profile

class PostType(DjangoObjectType):
    class Meta:
        model = models.Post

class CategoryType(DjangoObjectType):
    class Meta:
        model = models.Category
        fields = ("id", "name")

class TagType(DjangoObjectType):
    class Meta:
        model = models.Tag
        fields = ("id", "name")


class Query(graphene.ObjectType):
    all_posts = graphene.List(PostType)
    author_by_username = graphene.Field(AuthorType, username=graphene.String())
    post_by_slug = graphene.Field(PostType, slug=graphene.String())
    posts_by_author = graphene.List(PostType, username=graphene.String())
    posts_by_Categories = graphene.List(PostType, category=graphene.String())
    posts_by_tag = graphene.List(PostType, tag=graphene.String())
    categories = graphene.List(CategoryType)

    def resolve_all_posts(root, info):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(published=True)
        )


    def resolve_author_by_username(root, info, username):
        return models.Profile.objects.select_related("user").get(
            user__username=username
        )

    def resolve_post_by_slug(root, info, slug):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .get(slug=slug)
        )

    def resolve_posts_by_author(root, info, username):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(author__user__username=username)
        )

    def resolve_posts_by_category(root, info, category):
        return (
            models.Post.objects.prefetch_related("tag")
            .select_related("author")
            .filter(category__name__iexact=category)
        )
        
    def resolve_posts_by_tag(root, info, tag):
        return (
            models.Post.objects.prefetch_related("tags")
            .select_related("author")
            .filter(tags__name__iexact=tag)
        )

    def resolve_categories(root, info):
        return Category.objects.all()

schema = graphene.Schema(query=Query)