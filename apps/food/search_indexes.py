from haystack import indexes
from .models import Food, Flavour


class FoodIndex(indexes.SearchIndex, indexes.Indexable):
    """美食索引类"""
    text = indexes.CharField(document=True, use_template=True)
    school = indexes.IntegerField(model_attr='school_id')

    def get_model(self):
        return Food

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()


class FlavourIndex(indexes.SearchIndex, indexes.Indexable):
    """口味索引"""
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Flavour

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()