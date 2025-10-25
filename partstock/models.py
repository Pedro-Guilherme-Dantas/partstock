from django.db import models
from django.utils import timezone


class Part(models.Model):
    name = models.CharField(unique=True, max_length=50)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.IntegerField( 
        default=0
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Part"
        verbose_name_plural = "Parts"
        ordering = ['name']

    def __str__(self):
        return self.name


class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('IN', 'Inbound (Purchase/Addition)'),
        ('OUT', 'Outbound (Sale/Use)'),
    ]

    movement_type = models.CharField(
        max_length=3,
        choices=MOVEMENT_TYPES,
        default='OUT'
    )
    date_recorded = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Stock Movement"
        verbose_name_plural = "Stock Movements"
        ordering = ['-date_recorded']
        indexes = [
            models.Index(fields=['-date_recorded']),
            models.Index(fields=['movement_type']),
        ]

    def __str__(self):
        return (
            f"Movement #{self.id} "
            f"({self.get_movement_type_display()}) on "
            f"{self.date_recorded.strftime('%Y-%m-%d')}"
        )

    @property
    def total_value(self):
        return sum(item.total_value for item in self.items.all())

    @property
    def total_profit(self):
        return sum(item.profit_margin for item in self.items.all())


class MovementItem(models.Model):
    movement = models.ForeignKey(
        StockMovement,
        on_delete=models.CASCADE,
        related_name='items'
    )
    part = models.ForeignKey(
        'Part', 
        on_delete=models.PROTECT, 
        related_name='movement_items'
    )
    quantity = models.IntegerField()
    unit_price_at_transaction = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True
    )
    unit_cost_at_transaction = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        blank=True
    )

    class Meta:
        verbose_name = "Movement Item"
        verbose_name_plural = "Movement Items"

    def __str__(self):
        return (
            f"{self.quantity} x {self.part.name} "
            f"@ {self.unit_price_at_transaction}"
        )

    @property
    def total_value(self):
        return self.quantity * self.unit_price_at_transaction

    @property
    def profit_margin(self):
        unit_profit = (
            self.unit_price_at_transaction
            - self.unit_cost_at_transaction
            )
        return  unit_profit * self.quantity
