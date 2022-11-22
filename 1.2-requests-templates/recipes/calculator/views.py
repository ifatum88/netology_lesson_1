from django.shortcuts import render
import copy

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

def index(request):
    
    recipes_list = DATA.keys()
    
    context = {
        'recipes_list':recipes_list
    }
    
    return render(request,'calculator\\index.html',context=context)

def recipe(request,rec_name):
    
    servings_rec = copy.deepcopy(DATA.get(rec_name,""))
    lf_not_zero = lambda x : float(x) if float(x) > 0 else 1
    servings = lf_not_zero(request.GET.get('servings',1))
    
    for ingredient in servings_rec:
        servings_rec[ingredient] = float(servings_rec[ingredient]) * servings
         
    context = {
        'recipe':servings_rec,
        'servings':servings
    }
    return render(request,'calculator\\recipe.html',context=context)

