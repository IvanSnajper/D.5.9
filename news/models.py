from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    rating_author = models.FloatField(default=0.0)

    def update_rating(self):
        author_articles_rating = Post.objects.filter(author=self).aggregate(post_rating=Sum('post_rating') * 3)
        print(author_articles_rating)
        author_comments_rating = Comment.objects.filter(user_id=self.author).aggregate(comment_rating=Sum('comment_rating'))
        print(author_comments_rating)
        all_to_author = Comment.objects.filter(post__author__author=self.author).aggregate(comments_rating_sum=Sum('comment_rating'))
        print(all_to_author)
        self.rating_author = author_articles_rating['post_rating'] + author_comments_rating['comment_rating'] + all_to_author['comments_rating_sum']
        self.save()


class Category(models.Model):
    culture = 'CU'
    science = 'SC'
    tech = 'TE'
    politics = 'PO'
    sport = 'SP'
    entertainment = 'EN'
    economics = 'EC'
    education = 'ED'

    CATEGORIES = [
        (culture, 'Культура'),
        (science, 'Наука'),
        (tech, 'Технология'),
        (politics, 'Политика'),
        (sport, 'Спорт'),
        (entertainment, 'Развлечения'),
        (economics, 'Экономика'),
        (education, 'Образование')
    ]

    news_category = models.CharField(unique=True, max_length=2, choices=CATEGORIES)


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    POST_TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPES)
    time_created = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    post_rating = models.FloatField(default=0.0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def like(self):
        self.likes += 1
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.dislikes += 1
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_time_created = models.DateTimeField(auto_now_add=True)
    comment_rating = models.FloatField(default=0.0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()

