import cities_light


def filter_city_import(sender, items, **kwargs):
    if items[8] not in 'ES' or int(items[14]) < 10000:
        raise cities_light.InvalidItems()


cities_light.signals.city_items_pre_import.connect(filter_city_import)


def filter_region_import(sender, items, **kwargs):
    if items[0].split('.')[0] not in ('ES', 'FR', 'SE', 'PT', 'IT', 'NO', 'DE', 'GB', 'JP',
                                      'KR', 'CA', 'MX', 'US', 'AU', 'VE', 'EC', 'AR', 'UY',
                                      'PY', 'CL', 'BO', 'ZA', 'EG'):
        raise cities_light.InvalidItems()


cities_light.signals.region_items_pre_import.connect(filter_region_import)