from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q
from entity import Entity, EntityRelationship


class SubscriptionManager(models.Manager):
    def mediums_subscribed(self, source, entity, subentity_type=None):
        """Return all mediums subscribed to for a source.

        Args:

          source - A `Source` object. Check the mediums subscribed to,
          for this source of notifications.

          entity - An `Entity` object. The entity to check
          subscriptions for.

          subentity_type - (Optional) A content_type indicating we're
          interested in the mediums subscribed to by all sub-entities
          of the `entity` argument matching this subentity_type.

        Returns:

           A queryset of mediums the entity is subscribed to.

           If the subentity_type is None, this queryset has all
           unsubscribed mediums filtered out.

           If the subentity_type is not None, this queryset contains
           all mediums that any of the subenties might be subscribed
           to, *without* any unsubscribed mediums filtered out.

        """
        if subentity_type is None:
            return self._mediums_subscribed_individual(source, entity)
        else:
            return self._mediums_subscribed_group(source, entity, subentity_type)

    def is_subscribed(self, source, medium, entity, subentity_type=None):
        """Return True if subscribed to this medium/source combination.

        Args:

          source - A `Source` object. Check that there is a
          subscription for this source and the given medium.

          medium - A `Medium` object. Check that there is a
          subscription for this medium and the given source

          entity - An `Entity` object. The entity to check
          subscriptions for.

          subentity_type - (Optional) A content_type indicating we're
          interested in the subscriptions by all sub-entities of the
          `entity` argument matching this subentity_type.

        Returns:

           A boolean indicating if the entity is subscribed to this
           source/medium combination.

           If the subentity_type is None, this boolean takes into
           account whether the entity is unsubscribed.

           If the subentity_type is not None, this boolean indicates
           that any of the subenties might be subscribed to this
           combination of source/medium, *without* any unsubscriptions
           filtered out.

        """
        if subentity_type is None:
            return self._is_subscribed_individual(source, medium, entity)
        else:
            return self._is_subscribed_group(source, medium, entity, subentity_type)

    def _mediums_subscribed_individual(self, source, entity):
        """Return the mediums a single entity is subscribed to for a source.
        """
        super_entities = entity.super_relationships.all().values_list('super_entity')
        entity_is_subscribed = Q(subentity_type__isnull=True, entity=entity)
        super_entity_is_subscribed = Q(subentity_type=entity.entity_type, entity__in=super_entities)
        subscribed_mediums = self.filter(
            entity_is_subscribed | super_entity_is_subscribed, source=source
        ).select_related('medium').values_list('medium', flat=True)
        unsubscribed_mediums = Unsubscribe.objects.filter(
            entity=entity, source=source
        ).select_related('medium').values_list('medium', flat=True)
        return Medium.objects.filter(id__in=subscribed_mediums).exclude(id__in=unsubscribed_mediums)

    def _mediums_subscribed_group(self, source, entity, subentity_type):
        """Return all the mediums any subentity in a group is subscrbed to.
        """
        all_group_sub_entities = entity.sub_relationships.select_related('sub_entity').filter(
            sub_entity__entity_type=subentity_type
        ).values_list('sub_entity')
        related_super_entities = EntityRelationship.objects.filter(
            sub_entity__in=all_group_sub_entities
        ).values_list('super_entity')
        group_subscribed_mediums = self.filter(
            source=source, subentity_type=subentity_type, entity__in=related_super_entities
        ).select_related('medium').values_list('medium', flat=True)
        return Medium.objects.filter(id__in=group_subscribed_mediums)

    def _is_subscribed_individual(self, source, medium, entity):
        """Return true if an entity is subscribed to that source/medium combo.
        """
        super_entities = entity.super_relationships.all().values_list('super_entity')
        entity_is_subscribed = Q(subentity_type__isnull=True, entity=entity)
        super_entity_is_subscribed = Q(subentity_type=entity.entity_type, entity__in=super_entities)
        is_subscribed = self.filter(
            entity_is_subscribed | super_entity_is_subscribed,
            source=source,
            medium=medium,
        ).exists()
        unsubscribed = Unsubscribe.objects.filter(
            source=source,
            medium=medium,
            entity=entity
        ).exists()
        return is_subscribed and not unsubscribed

    def _is_subscribed_group(self, source, medium, entity, subentity_type):
        """Return true if any subentity is subscribed to that source & medium.
        """
        all_group_sub_entities = entity.sub_relationships.select_related('sub_entity').filter(
            sub_entity__entity_type=subentity_type
        ).values_list('sub_entity')
        related_super_entities = EntityRelationship.objects.filter(
            sub_entity__in=all_group_sub_entities,
        ).values_list('super_entity')
        is_subscribed = self.filter(
            source=source,
            medium=medium,
            subentity_type=subentity_type,
            entity__in=related_super_entities
        ).exists()
        return is_subscribed


class Subscription(models.Model):
    """Include groups of entities to subscriptions.

    It is recommended that these be largely pre-configured within an
    application, as catch-all groups. The finer grained control of
    individual users subscription status is defined within the
    `Unsubscribe` model.

    If, however, you want to subscribe an individual entity to a
    source/medium combination, setting the `subentity_type` field to
    None will create an individual subscription.
    """
    medium = models.ForeignKey('Medium')
    source = models.ForeignKey('Source')
    entity = models.ForeignKey(Entity)
    subentity_type = models.ForeignKey(ContentType, null=True)

    objects = SubscriptionManager()


class UnsubscribeManager(models.Manager):
    def is_unsubscribed(self, source, medium, entity):
        """Return True if the entity is unsubscribed
        """
        return self.filter(source=source, medium=medium, entity=entity).exists()


class Unsubscribe(models.Model):
    """Individual entity-level unsubscriptions.

    Entities can opt-out individually from recieving any notification
    of a given source/medium combination.
    """
    entity = models.ForeignKey(Entity)
    medium = models.ForeignKey('Medium')
    source = models.ForeignKey('Source')

    objects = UnsubscribeManager()


class Medium(models.Model):
    """A method of actually delivering the notification to users.

    Mediums describe a particular method the application has of
    sending notifications. The code that handles actually sending the
    message should own a medium object that represents itself, or at
    least, know the name of one.
    """
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()


class Source(models.Model):
    """A category of where notifications originate from.

    Sources should make sense as a category of notifications to users,
    and pieces of the application which create that type of
    notification should own a `source` object which they can pass
    along to the business logic for distributing the notificaiton.
    """
    name = models.CharField(max_length=64, unique=True)
    display_name = models.CharField(max_length=64)
    description = models.TextField()
