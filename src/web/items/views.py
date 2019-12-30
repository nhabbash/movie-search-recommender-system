from items.forms import SearchForm
from items.forms import RecommenderForm
from django.views.generic.edit import FormView
import items.search as search
from collections import defaultdict

class SearchView(FormView):
    template_name = 'items/search.html'
    form_class = SearchForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        data = defaultdict(int, self.request.GET.dict())

        q = data["query"]
        profile = data["profile"]
        if profile:
            profile = profile.lower()
        ps = data["personalized"]
        fuzzy = data["fuzzy"]
        synonyms = data["synonyms"]
        pop = data["popularity_rel"]
        weight = data["weighted_vote_popularity"]

        items, u_interest, u_language = search.query(q, profile, ps, fuzzy, synonyms, pop, weight)
        
        context['items'] = items
        context['u_interest'] = u_interest
        context['u_language'] = u_language
        return context

class RecommenderView(FormView):
    template_name = 'items/recommender.html'
    form_class = RecommenderForm

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(RecommenderView, self).get_context_data(**kwargs)
        data = defaultdict(int, self.request.GET.dict())

        profile = data["profile"]
        filtering = data['filtering']

        if profile:
            profile = profile.lower()

        film_cf, film_cb, profile_seen, u_interest, u_language = search.recommendation(profile, filtering)

        context['film_cb'] = film_cb
        context['film_cf'] = film_cf
        context['profile_seen'] = profile_seen
        context['u_interest'] = u_interest
        context['u_language'] = u_language

        return context