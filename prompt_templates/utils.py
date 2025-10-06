def generate_prompt(template_text, user, form_data=None):
    # Define all supported placeholders
    values = {
        "business_name": None,
        "business_type": None,
        "business_location": None,
        "target_audience": None,
        "product_or_service": None,
        "service_name": None,
        "topic": None,
        "industry_topic": None,
        "additional_info": None,
    }

    # Load profile defaults if a user is logged in and has one
    if (
        user is not None
        and hasattr(user, "is_authenticated")
        and user.is_authenticated
        and hasattr(user, "profile")
    ):
        profile = user.profile
        values.update(
            {
                "business_name": getattr(profile, "business_name", None),
                "business_type": getattr(profile, "business_type", None),
                "business_location": getattr(profile, "business_location", None),
                "target_audience": getattr(profile, "target_audience", None),
            }
        )

    # Override with form input values
    if form_data:
        for k in values.keys():
            if form_data.get(k):
                values[k] = form_data.get(k).strip()

    # Replace placeholders in text
    for key, val in values.items():
        placeholder = f"[{key}]"
        if val:
            template_text = template_text.replace(placeholder, val)
        else:
            template_text = template_text.replace(placeholder, "")

    # Remove double spaces and trailing blanks
    cleaned_text = " ".join(template_text.split())
    return cleaned_text.strip()
