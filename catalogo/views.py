from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from urllib.parse import quote
from .models import Categoria, Producto
from .forms import ProductoForm, CategoriaForm


def es_staff(user):
    return user.is_active and user.is_staff


# ── Vistas públicas ──────────────────────────────────────────────────────────

def home(request):
    categorias = Categoria.objects.prefetch_related('productos').all()
    destacados = (
        Producto.objects
        .select_related('categoria')
        .filter(disponible=True, destacado=True)[:8]
    )
    total_productos = Producto.objects.filter(disponible=True).count()
    return render(request, 'catalogo/home.html', {
        'categorias': categorias,
        'destacados': destacados,
        'total_productos': total_productos,
    })


def coleccion(request):
    categorias = Categoria.objects.all()
    categoria_slug = request.GET.get('categoria', '').strip()
    busqueda = request.GET.get('q', '').strip()

    productos = (
        Producto.objects
        .select_related('categoria')
        .filter(disponible=True)
    )

    categoria_activa = None
    if categoria_slug:
        categoria_activa = Categoria.objects.filter(slug=categoria_slug).first()
        if categoria_activa:
            productos = productos.filter(categoria=categoria_activa)

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    return render(request, 'catalogo/coleccion.html', {
        'productos': productos,
        'categorias': categorias,
        'categoria_activa': categoria_activa,
        'busqueda': busqueda,
        'total_resultados': productos.count(),
    })


def detalle(request, slug):
    producto = get_object_or_404(
        Producto.objects.select_related('categoria'),
        slug=slug,
        disponible=True,
    )
    relacionados = (
        Producto.objects
        .filter(categoria=producto.categoria, disponible=True)
        .exclude(pk=producto.pk)[:4]
    )

    # Mensaje WhatsApp con nombre, precio e imagen (si existe)
    imagen_url = producto.get_imagen_url()
    lineas = [
        f'Hola, me interesa este producto de *Premier Bodega Importadora*:',
        f'',
        f'*{producto.nombre}*',
        f'Precio: {producto.precio_formateado()}',
    ]
    if producto.referencia:
        lineas.append(f'Ref: {producto.referencia}')
    if imagen_url and imagen_url.startswith('http'):
        lineas.append(f'')
        lineas.append(f'Imagen: {imagen_url}')

    mensaje_wa = '\n'.join(lineas)
    whatsapp_url = f'https://wa.me/{settings.WHATSAPP_NUMBER}?text={quote(mensaje_wa)}'

    return render(request, 'catalogo/detalle.html', {
        'producto': producto,
        'relacionados': relacionados,
        'whatsapp_url': whatsapp_url,
    })


# ── Panel de administración ──────────────────────────────────────────────────

def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('catalogo:panel_dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', 'catalogo:panel_dashboard'))
        error = 'Usuario o contraseña incorrectos, o sin permisos de administrador.'

    return render(request, 'panel/login.html', {'error': error})


def panel_logout(request):
    logout(request)
    return redirect('catalogo:home')


@login_required(login_url='catalogo:panel_login')
@user_passes_test(es_staff, login_url='catalogo:panel_login')
def panel_dashboard(request):
    productos = (
        Producto.objects
        .select_related('categoria')
        .order_by('-creado')
    )
    categorias = Categoria.objects.all()
    busqueda = request.GET.get('q', '').strip()
    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    return render(request, 'panel/dashboard.html', {
        'productos': productos,
        'categorias': categorias,
        'total': productos.count(),
        'busqueda': busqueda,
    })


@login_required(login_url='catalogo:panel_login')
@user_passes_test(es_staff, login_url='catalogo:panel_login')
def panel_producto_nuevo(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto creado correctamente.')
        return redirect('catalogo:panel_dashboard')
    return render(request, 'panel/producto_form.html', {
        'form': form,
        'titulo': 'Nuevo Producto',
        'accion': 'Crear',
    })


@login_required(login_url='catalogo:panel_login')
@user_passes_test(es_staff, login_url='catalogo:panel_login')
def panel_producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Producto actualizado correctamente.')
        return redirect('catalogo:panel_dashboard')
    return render(request, 'panel/producto_form.html', {
        'form': form,
        'producto': producto,
        'titulo': f'Editar: {producto.nombre}',
        'accion': 'Guardar cambios',
    })


@login_required(login_url='catalogo:panel_login')
@user_passes_test(es_staff, login_url='catalogo:panel_login')
def panel_producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'"{nombre}" eliminado.')
        return redirect('catalogo:panel_dashboard')
    return render(request, 'panel/producto_confirmar_eliminar.html', {'producto': producto})


@login_required(login_url='catalogo:panel_login')
@user_passes_test(es_staff, login_url='catalogo:panel_login')
def panel_categoria_nueva(request):
    form = CategoriaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Categoría creada.')
        return redirect('catalogo:panel_dashboard')
    return render(request, 'panel/categoria_form.html', {
        'form': form,
        'titulo': 'Nueva Categoría',
    })
