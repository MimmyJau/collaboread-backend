# Generated by Django 4.2 on 2023-04-14 18:59

from django.db import migrations
from treebeard.numconv import NumConv

"""
GOAL: Migrate old Comment model to new Comment model inheriting from MP_Node.
WHY: Treebeard's MP_Node model is a better fit for self-referential objects.
COMPLICATION: Treebeard's MP_Node uses custom manager that has a function
called add_root() for adding a root node. In migrations, we don't have 
access to custom manager functions.
    SOURCE: https://github.com/django-treebeard/django-treebeard/issues/264
SOLUTION: Manually create each object and save. The only complicated 
attribute is path, which has a custom function to generate it. The
other attributes, such as depth, numchild, etc. are easy to calculate 
since we're just adding root. To be totally honest, I don't know if 
this will actually work since I fucked up the migration initially 
by forgetting to include .save(), and I couldn't revert since psycopg3 
was giving an error (something about duplicating keys). Probably will
have to flush production db anyways. Triggered.
    SOURCE: https://stackoverflow.com/a/37685925
"""

# from april fool's rfc 1924
BASE85 = (
    "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    "!#$%&()*+-;<=>?@^_`{|}~"
)


def int2str(self, num):
    """Converts an integer into a string.

    :param num: A numeric value to be converted to another base as a
                string.

    :rtype: string

    :raise TypeError: when *num* isn't an integer
    :raise ValueError: when *num* isn't positive
    """
    if int(num) != num:
        raise TypeError("number must be an integer")
    if num < 0:
        raise ValueError("number must be positive")
    radix, alphabet = self.radix, self.alphabet
    if radix in (8, 10, 16) and alphabet[:radix].lower() == BASE85[:radix].lower():
        return ({8: "%o", 10: "%d", 16: "%x"}[radix] % num).upper()
    ret = ""
    while True:
        ret = alphabet[num % radix] + ret
        if num < radix:
            break
        num //= radix
    return ret


def numconv_obj(obj):
    if obj.numconv_obj_ is None:
        obj.numconv_obj_ = NumConv(len(obj.alphabet), obj.alphabet)
    return obj.numconv_obj_


def _int2str(obj, num):
    return int2str(numconv_obj(obj), num)


def _get_basepath(obj, path, depth):
    """:returns: The base path of another path up to a given depth"""
    if path:
        return path[0 : depth * obj.steplen]
    return ""


def _get_path(obj, path, depth, newstep):
    """
    Builds a path given some values

    :param path: the base path
    :param depth: the depth of the  node
    :param newstep: the value (integer) of the new step
    """
    parentpath = _get_basepath(obj, path, depth - 1)
    key = _int2str(obj, newstep)
    return "{0}{1}{2}".format(
        parentpath, obj.alphabet[0] * (obj.steplen - len(key)), key
    )


def transfer_comments(apps, schema_editor):
    Article = apps.get_model("core", "Article")
    Comment = apps.get_model("core", "Comment")
    CommentTree = apps.get_model("core", "CommentTree")

    zarathustra = Article.objects.first()
    for comment in Comment.objects.all():
        new_comment = CommentTree(
            user=comment.user,
            article=zarathustra,
            annotation=comment.annotation,
            created_on=comment.created_on,
            updated_on=comment.updated_on,
            comment_html=comment.comment_html,
            comment_json=comment.comment_json,
        )

        new_comment.steplen = 4
        new_comment.alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        new_comment.node_order_by = ["created_on"]
        new_comment.numconv_obj_ = None
        new_comment.depth = 1
        new_comment.numchild = 0
        new_comment.path = _get_path(
            new_comment, "", new_comment.depth, new_comment.numchild
        )
        new_comment.save()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0009_alter_commenttree_created_on"),
    ]

    operations = [
        migrations.RunPython(transfer_comments),
    ]