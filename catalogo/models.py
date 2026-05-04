from django.db import models
from django.urls import reverse
from slugify import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    descripcion = models.TextField(blank=True)
    orden = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['orden', 'nombre']
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalogo:coleccion') + f'?categoria={self.slug}'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='productos',
    )
    nombre = models.CharField(max_length=240)
    slug = models.SlugField(max_length=260, unique=True, blank=True)
    referencia = models.CharField(max_length=80, blank=True)
    descripcion_corta = models.CharField(max_length=320, blank=True)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen_url = models.URLField(max_length=600, blank=True)
    disponible = models.BooleanField(default=True)
    destacado = models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['categoria__orden', 'categoria__nombre', 'nombre']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['disponible']),
            models.Index(fields=['categoria', 'disponible']),
            models.Index(fields=['destacado', 'disponible']),
        ]
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nombre)
            slug, n = base, 1
            while Producto.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f'{base}-{n}'
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('catalogo:detalle', kwargs={'slug': self.slug})

    def precio_formateado(self):
        if self.precio is None:
            return 'Consultar precio'
        return f'${self.precio:,.0f}'.replace(',', '.')

    def get_imagen_url(self):
        if self.imagen:
            return self.imagen.url
        if self.imagen_url:
            return self.imagen_url
        return None

    def __str__(self):
        return self.nombre
