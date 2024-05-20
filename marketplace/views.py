from django.shortcuts import render, redirect , get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Produit , Fournisseur , Cart, CartItem
from .forms import Fournisseur , ProduitForm ,FrsForm ,UserRegistrationForm
from django.urls import reverse
from django.db.models import Q 
from django.template.loader import get_template
# from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import login, authenticate
from django.contrib import messages

# Create your views here.
@login_required
def home(request):
    context={'val':"Menu Acceuil"} 
    return render(request,'mesProduits.html',context)


@login_required
def register_product(request):
    if request.method == 'POST':
        form = ProduitForm(request.POST, request.FILES)
        if form.is_valid():
            produit = form.save(commit=False)
            if request.user.is_authenticated:  # Check if the user is authenticated
                produit.fournisseur = request.user
                produit.save()
                return redirect('marketplace/main')
            else:
                # Handle the case where the user is not authenticated
                # You may redirect the user to the login page or display an error message
                return HttpResponse("You need to be logged in to register a product.")
    else:
        form = ProduitForm()
    return render(request, 'marketplace/addProduct.html', {'form': form})

def index(request):
    query = request.GET.get('q')
    products = Produit.objects.all()

    if query:
        products = products.filter(libelle__icontains=query)

    context = {'products': products, 'query': query}
    return render(request, 'marketplace/mesProduits.html', context)
 

def IFournisseur(request):	
    template = loader.get_template('marketplace/mesFournisseur.html')
    fournisseurs= Fournisseur.objects.all()
    context={'fournisseurs':fournisseurs}  
    return render( request,'marketplace/mesProduits.html ',context )

def majProd(request):
    if request.method == "POST" : 
        form = ProduitForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect('/marketplace')
    else :
        form = ProduitForm() #créer formulaire vide
        return render(request,'marketplace/majProduits.html',{'form':form})

def indexVtr(request):
    list=Produit.objects.all()
    return render(request,'../templates/marketplace/vitrine.html',{'list':list})

def indexFrs(request): 
    if request.method == "POST" : 
        form = FrsForm(request.POST)
        if form.is_valid(): 
            nom = form.cleaned_data['nom']
            adr = form.cleaned_data['adr']
            frs=Fournisseur()
            frs.nom=nom
            frs.adresse=adr
            form.save()
    else :
        form = FrsForm()
    return render(request,'marketplace/testForm.html',{'form':form})
 
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        product = Produit.objects.get(id=product_id)
        cart, _ = Cart.objects.get_or_create()
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return redirect('cart')

    return redirect('index')

def view_cart(request):
    cart, _ = Cart.objects.get_or_create()
    cart_items = cart.cartitem_set.all()
    total_price = sum(item.subtotal() for item in cart_items)
    return render(request, 'marketplace/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def decrease_quantity(request, product_id): 
    product = get_object_or_404(Produit, id=product_id)
     
    cart, _ = Cart.objects.get_or_create()
     
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
     
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
     
    return HttpResponseRedirect(reverse('cart'))

def remove_from_cart(request, product_id): 
    product = get_object_or_404(Produit, id=product_id)
     
    cart, _ = Cart.objects.get_or_create()
     
    cart_item = get_object_or_404(CartItem, cart=cart, product=product)
    cart_item.delete()
     
    return HttpResponseRedirect(reverse('cart'))

def generate_pdf(request):
    cart_items = CartItem.objects.all()  
    
    # Render the HTML template with cart items
    template_path = 'marketplace/cart_pdf_template.html'
    context = {'cart_items': cart_items}
    template = get_template(template_path)
    html = template.render(context)
    
    # Generate PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="cart_items.pdf"'

    # # pisa_status = pisa.CreatePDF(html, dest=response)
    # if pisa_status.err:
    #     return HttpResponse('PDF creation failed')
    return response