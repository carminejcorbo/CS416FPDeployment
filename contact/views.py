from django.shortcuts import render, redirect
from .forms import ContactForm


def contact(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        print(form)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            print(request.POST)
            print(form.cleaned_data['email'])
            form.save()
            # redirect to a new URL:
            return render(request, 'contact/thanks.html')
        else:
            form = ContactForm()
            context = {'form': form, 'error': 'The data entered is not valid!'}
            template = 'contact/contact.html'
            return render(request, template, context)
    else:
        form = ContactForm()
        context = {'form': form}
        template = 'contact/contact.html'
        return render(request, template, context)
