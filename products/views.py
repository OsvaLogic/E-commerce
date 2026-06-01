from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from django.db import transaction
from .models import Product, Category, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer
from .tasks import send_confirmation_email

class ProductViewSet(viewsets.ModelViewSet):
    """
    Endpoint para listar, crear, actualizar y eliminar productos.
    Soporta búsqueda mediante query param: /api/products/?q=teclado
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # Solo el staff puede crear/editar productos. Cualquiera puede ver el catálogo.
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('q', None)
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        return queryset

class CheckoutAPIView(views.APIView):
    """
    Endpoint para procesar pagos y restar stock de forma segura.
    El frontend debe enviar el payload JSON: {"cart": {"id_producto": cantidad, ...}}
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = request.data.get('cart', {})
        if not cart:
            return Response({'error': 'Tu carrito está vacío.'}, status=status.HTTP_400_BAD_REQUEST)
            
        try:
            with transaction.atomic():
                order = Order.objects.create(user=request.user, total=0)
                total_price = 0
                
                valid_ids = [str(i) for i in Product.objects.filter(id__in=cart.keys()).values_list('id', flat=True)]
                
                for product_id in valid_ids:
                    quantity = cart[product_id]
                    product = Product.objects.select_for_update().get(id=product_id)
                    
                    if product.stock < quantity:
                        raise ValueError(f'Stock insuficiente para "{product.name}". Quedan {product.stock} unidades.')
                        
                    product.stock -= quantity
                    product.save()
                    
                    item_total = product.price * quantity
                    total_price += item_total
                    
                    OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
                    
                order.total = total_price
                order.save()
                
                # Disparamos la tarea asíncrona hacia Celery (Redis/SQS)
                send_confirmation_email.delay(order.id)
                
                serializer = OrderSerializer(order)
                return Response({
                    'message': '¡Compra realizada con éxito!',
                    'order': serializer.data
                }, status=status.HTTP_201_CREATED)
                
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
