from django import forms


class PromptFillForm(forms.Form):
    business_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "e.g. The Potting Place"}),
        label="Business Name",
    )
    business_type = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Florist, Restaurant, Gym etc"}
        ),
        label="Business Type",
    )
    business_location = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Bristol BS1, Manchester, Shoreditch"}
        ),
        label="Business Location",
    )
    target_audience = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Families, young professionals, local foodies"}
        ),
        label="Target Audience",
    )
    product_or_service = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Custom wedding bouquets, 1-to-1 coaching"}
        ),
        label="Product or Service",
    )
    service_name = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. Web Design, Dog Grooming, Yoga Class"}
        ),
        label="Service Name",
    )
    topic = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. healthy eating, digital marketing"}
        ),
        label="Topic",
    )
    industry_topic = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"placeholder": "e.g. sustainability in fashion, AI in education"}
        ),
        label="Industry Topic",
    )
    additional_info = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "e.g. Award-winning yoga studio, Open Until 11pm, Limited parking",
                "rows": 2,
            }
        ),
        label="Additional Info",
    )
