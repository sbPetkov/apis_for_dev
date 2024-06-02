from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from .models import Advice
from .serializers import AdviceSerializer


class AdviceViewSet(viewsets.ModelViewSet):
    queryset = Advice.objects.all()
    serializer_class = AdviceSerializer

    def create(self, request, *args, **kwargs):
        position = request.data.get('position')
        if position:
            self.adjust_positions_on_create(position)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.position)
        new_position = request.data.get('position')
        print(type(new_position), new_position)
        if new_position is not None and instance.position != int(new_position):
            old_position = instance.position
            self.adjust_positions_on_update(old_position, int(new_position))
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.adjust_positions_on_delete(instance.position)
        return super().destroy(request, *args, **kwargs)

    @staticmethod
    def adjust_positions_on_create(new_position):
        advices = Advice.objects.filter(position__gte=new_position)
        for advice in advices:
            advice.position += 1
            advice.save()

    @staticmethod
    def adjust_positions_on_update(old_position, new_position):
        if old_position < new_position:
            advices = Advice.objects.filter(position__gt=old_position, position__lte=new_position)
            for advice in advices:
                advice.position -= 1
                advice.save()
        elif old_position > new_position:
            advices = Advice.objects.filter(position__lt=old_position, position__gte=new_position)
            for advice in advices:
                advice.position += 1
                advice.save()

    @staticmethod
    def adjust_positions_on_delete(deleted_position):
        advices = Advice.objects.filter(position__gt=deleted_position)
        for advice in advices:
            advice.position -= 1
            advice.save()

    @action(detail=False, methods=['get'])
    def ordered(self, request):
        queryset = Advice.objects.all()[:5].order_by('position')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
